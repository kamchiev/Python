import time, sys
import importlib
import stopit
import unittest, unittest.mock
from contextlib import contextmanager
import tempfile, os, os.path
#from hashlib import sha1

DEBUG=True
DEBUG=False

class ForbiddenError(Exception):
    pass

class TimeoutError(Exception):
    pass

class TestCase(unittest.TestCase):
    __orig_import = __builtins__['__import__']
    __orig_open   = __builtins__['open']

    def _raise_forbidden(self, forbidden):
        # Lamdable method that throws an exception
        raise ForbiddenError(f"The usage of the '{forbidden}' function/method is forbidden!")

    def forbidden_function(self, target='os.walk'):
        # Return a 'with' context to forbid using a target function: by default 'os.walk'
        return unittest.mock.patch(target, new=lambda *x, **k: self._raise_forbidden( target ))

    def check_imports(self, allowed=None, forbidden=None):
        if allowed   is None: allowed   = []
        if forbidden is None: forbidden = []
        # Return a 'with' context to forbid imports not listed in 'allowed' or listed in 'forbidden'
        def _check_import(*args, **kargs):
            name, *rest = args
            if name in forbidden or (not forbidden and name not in allowed):
                print(f"Importing {name} (globals, locals, {rest[-2:]}) (not allowed)")
                raise ForbiddenError(f"The import of '{name}' is forbidden")
            else:
                return self.__orig_import(*args, **kargs)
        return unittest.mock.patch('builtins.__import__', new=_check_import)

    def check_open(self, allowed_filenames_modes=None):
        if not allowed_filenames_modes:
            allowed_filenames_modes = {}
        def _check_open(*args, **kargs):
            if len(args) > 1:
                mode = args[1]
            else:
                mode = kargs.get('mode', 'r')
            filename = args[0]
            # print(f"checking {filename} ({args}, {kargs}) against {allowed_filenames_modes}")
            if filename not in allowed_filenames_modes:
                print(f"Opening file '{filename}' is not allowed!")
                raise ForbiddenError(f"It's forbidden to open file '{filename}'")
            if mode not in allowed_filenames_modes[filename]:
                print(f"Opening file '{filename}' with mode '{mode}' is not allowed!")
                raise ForbiddenError(f"Opening file '{filename}' with mode='{mode}' is forbidden!")
            # print(f"Opening file {filename} with mode {mode} (allowed)")
            return self.__orig_open(*args, **kargs)
        return unittest.mock.patch('builtins.open', new=_check_open)

    def ignored_function(self, target='builtins.print'):
        # Return a 'with' context that ignores a target function: by default 'builtins.print'
        return unittest.mock.patch(target, new=lambda *x, **k: None)

    @contextmanager
    def timer(self, timeout):
        '''Return a context in which the execution time is measured and, if necessary, a time-out exception is thrown.
        This way, the timeout is detected even if the timeout signal is captured. (yield version)'''
        start = time.time()
        try:
            yield start
        finally:
            wallclock_time = round(time.time() - start, 3)
            if wallclock_time > timeout:
                raise TimeoutError(f'Timeout! ({wallclock_time} > {timeout})')

    def timeout(self, sec):
        '''Return a 'with' context to stop the code when the timeout expires.'''
        return stopit.ThreadingTimeout(sec, swallow_exc=False)
        #return stopit.SignalTimeout(sec, swallow_exc=False)

    @contextmanager
    def assertIsRecursive(self, module):
        '''Return a 'with' context to check for recursion.'''
        import isrecursive
        with    self.imported(module) as program01, \
                self.decorated(program01) as program, \
                self.assertRaises( isrecursive.RecursionDetectedError ):
            yield program

    @contextmanager
    def decorated(self, module):
        '''Return a 'with' context decorating all functions/methods to raise RecursionDetectedError if recursive.'''
        import isrecursive
        isrecursive.decorate_module(module)
        try:
            yield module
        finally:
            isrecursive.undecorate_module(module)
        
    @contextmanager
    def imported(self, module):
        '''Return a 'with' context to import/unimport the module'''
        program = importlib.import_module(module)
        try:
            yield program
        finally:
            del program
            del sys.modules[module]

    @contextmanager
    def randomized_symbol(self, module, symbol):
        '''Renames randomly a symbol in a module'''
        import random, string
        random_name = ''.join(random.choices(string.ascii_letters, k=20))
        if DEBUG: print(module, symbol, ' -> ', random_name)
        value = getattr(module, symbol)
        setattr(module, random_name, value)
        delattr(module, symbol)
        try:
            yield random_name
        finally:
            if DEBUG: print(module, random_name, ' -> ', symbol)
            setattr(module, symbol, value)
            delattr(module, random_name)

    @contextmanager
    def randomized_filename(self, filename):
        '''Return a 'with' context to randomize a filename before using it. (yield version)'''
        import tempfile, os, os.path
        name, ext = filename.split('.')                                                                                             
        randomized = next(tempfile._get_candidate_names()) + '.' + ext                                                         
        if os.path.isfile(filename):
            if DEBUG: print(filename, ' -> ', randomized)
            os.rename(filename, randomized)
            try:
                yield
            finally:
                if DEBUG: print(self.filename, ' <- ', self.randomized)
                os.rename(self.randomized, self.filename)

    def check(self, value, expected, params=None, explanation=''):
        # TODO: add deepcopy of value to avoid side effects
        msg = ''
        if params:
            msg += '\twhen input={} '.format(params)
        msg += '\n\t\t%r != %r' % (value, expected)
        if explanation:
            msg += "\t<- " + explanation
        self.assertEqual(value, expected, msg)

    def check_text_file(self,a,b):
        with open(a, encoding='utf8') as f: txt_a = f.read()
        with open(b, encoding='utf8') as f: txt_b = f.read()
        lines_a = [l.strip() for l in txt_a.splitlines()]
        lines_b = [l.strip() for l in txt_b.splitlines()]
        # TODO: usare una diff
        msg = 'The texts differ: ' + a + ' ' + b
        self.assertEqual(lines_a, lines_b, msg)

    def __image_load(self, filename):
        '''Load the PNG image from the PNG file under 'filename',
            convert it into tuple-matrix format and return it'''
        import png
        with open(filename,'rb') as f:
            # the file is read as a 256-colour RGB (without transparency)
            reader = png.Reader(file=f)
            w, h, png_img, _ = reader.asRGB8()
            # the list of lists is converted to tuples
            # the PNG colors are 3 consecutive values of the png_img array
            w *= 3
            return [ [ (line[i],line[i+1],line[i+2]) 
                       for i in range(0, w, 3) ]
                     for line in png_img ]

    def check_img_file(self, a,b):
        f = open(a, "rb")
        g = open(b, "rb")
        #if sha1(f.read()).hexdigest() !=  sha1(g.read()).hexdigest():
        if f.read() !=  g.read():
            img_a = self.__image_load(a)
            img_b = self.__image_load(b)
            wa, ha = len(img_a[0]),len(img_a)
            wb, hb = len(img_b[0]),len(img_b)
            self.assertEqual(wa, wb, f"Images have different widths ({wa} != {wb})")
            self.assertEqual(ha, hb, f"Images have different heights ({ha} != {hb})")
            for y in range(ha):
                for x in range(wa):
                    ca, cb = img_a[y][x], img_b[y][x] 
                    msg = 'Images differ, starting at coordinates {},{} (colors: {} != {})'.format(x, y, ca, cb)
                    self.assertEqual(ca, cb, msg)

    def check_json_file(self, a, b, msg='The JSON files contain different structures'):
        import json
        with open(a,'r', encoding='utf8') as f1:
            A = json.load(f1)
        with open(b,'r', encoding='utf8') as f2:
            B = json.load(f2)
        self.assertEqual(A, B, msg)

    @classmethod
    def main(cls):
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(cls))
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
        result = runner.run(suite)
        failed = len(result.failures)
        passed = result.testsRun-failed
        print("{} test passed, {} tests failed".format(passed, failed))  

