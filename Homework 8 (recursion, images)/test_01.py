import testlib
from ddt import ddt, data, unpack
import images   # preload

# change DEBUG to True to disable timeout and checks
DEBUG=True
DEBUG=False
dir_puzzle = 'puzzles'
TIMEOUT = 2 * 2  # in seconds


@ddt
class Test(testlib.TestCase):

    def do_test(self, input_file, output_file,
                groundtruth_file, num_black_rects_gt,
                doRecursionTest=True):
        '''Test implementation:
            - input_file:          name of the PNG file containing the partitioned image
            - output_file:         name of the PNG file to be returned from the program interpreting input_file
            - groundtruth_file:    name of the PNG file containing the ground-truth result
            - num_black_rects_gt:  the ground-truth value of numer of black partitions
            TIMEOUT: global for all test
        '''
        if DEBUG:
            import program01 as program
            result = program.ex1(input_file, output_file)
        else:
            # first check for recursion
            if doRecursionTest:
                with self.assertIsRecursive('program01') as program:
                    program.ex1(input_file, output_file)
                del program
            with self.ignored_function('builtins.print'), \
                 self.ignored_function('pprint.pprint'), \
                 self.forbidden_function('builtins.input'), \
                 self.forbidden_function('builtins.eval'), \
                 self.check_open(
                     allowed_filenames_modes={input_file: ['rb'],
                                              output_file: ['wb']
                                              }), \
                 self.check_imports(allowed=['program01', '_io', 'images']), \
                 self.imported('program01') as program, \
                 self.timeout(TIMEOUT), \
                 self.timer(TIMEOUT):
                result   = program.ex1(input_file, output_file)
        self.assertEqual(type(result),  int,     
                         'il risultato prodotto deve essere un int / '
                         f' the expected result should be an int ({result})')
        self.assertEqual(result,        num_black_rects_gt, 
                         'il valore restituito non e\' corretto / '
                         f'the expected result is incorrect ({result})')
        self.check_img_file(output_file, groundtruth_file)
        return 1
    
    #   input_image,  num_black_rects_gt
    @data(
	('empty02',
	 (1), # rect
	 (False), # ck rec
	 ),
	('empty04',
	 (1), # rect
	 (False), # ck rec
	 ),
	('empty09',
	 (1), # rect
	 (False), # ck rec
	 ),
	('small01',
	 (16), # rect
	 (True), # ck rec
	 ),
	('small02',
	 (34), # rect
	 (True), # ck rec
	 ),
	('small03',
	 (10), # rect
	 (True), # ck rec
	 ),
	('fullcase01',
	 (64), # rect
	 (True), # ck rec
	 ),
	('fullcase02',
	 (256), # rect
	 (True), # ck rec
	 ),
	('fullcase03',
	 (1024), # rect
	 (True), # ck rec
	 ),
	('fullcase04',
	 (4096), # rect
	 (True), # ck rec
	 ),
	('fullcase05',
	 (16384), # rect
	 (True), # ck rec
	 ),
	('medium01',
	 (1279), # rect
	 (True), # ck rec
	 ),
	('medium02',
	 (52), # rect
	 (True), # ck rec
	 ),
	('medium03',
	 (2377), # rect
	 (True), # ck rec
	 ),
	('hard01',
	 (151), # rect
	 (True), # ck rec
	 ),
	('hard02',
	 (10), # rect
	 (True), # ck rec
	 ),
	('hard03',
	 (691), # rect
	 (True), # ck rec
	 ),
	('rect01',
	 (103), # rect
	 (True), # ck rec
	 ),
	('rect02',
	 (1051), # rect
	 (True), # ck rec
	 ),
	('rect03',
	 (88), # rect
	 (True), # ck rec
	 ),
	('rect04',
	 (358), # rect
	 (True), # ck rec
	 ),
	('rect05',
	 (2167), # rect
	 (True), # ck rec
	 ),
    ('rect06',
	 (214), # rect
	 (True), # ck rec
	 ),
    )
    @unpack
    def test_data(self, ID, num_black_rects_gt, check_rec):
        input_file = f"puzzles/{ID}.in.png"
        output_file    = f"test_{ID}.out.png"
        groundtruth_file    = f"puzzles/{ID}.gt.png"
        return self.do_test(input_file, output_file,
                            groundtruth_file, num_black_rects_gt,
                            doRecursionTest=check_rec)


if __name__ == '__main__':
    Test.main()

