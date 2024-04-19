import testlib, os
from ddt import file_data, ddt, data, unpack

# change this variable to True to disable timeout and enable print
DEBUG=True
DEBUG=False

WARP = 2   # test VM
WARP = 1   # your PC

files = ['students.json', 'courses.json', 'exams.json', 'teachers.json']
sizes = ['small', 'medium', 'large']
open_allowed = {dbsize+'_'+f:'trt' for f in files for dbsize in sizes}
open_allowed['.txt'] = 'w'
exdir = 'expfiles/'
@ddt
class Test(testlib.TestCase):
    allowed = open_allowed
    def do_test(self, func, params, expected, timeout, fout=None, fexpected=None):
        """Test implementation
        - func:     function to test
        - params:   parameters for the function
        - expected: expected return value
        - timeout:  variable timeout depending on test
        """
        TIMEOUT = timeout * WARP   # warp factor
        if DEBUG:
                result = func(*params)
        else:
            with    self.ignored_function('pprint.pprint'), \
                    self.forbidden_function('builtins.input'), \
                    self.forbidden_function('builtins.eval'), \
                    self.check_open( Test.allowed ), \
                    self.check_imports(allowed=['program01', '_io', 'encodings.utf_8', 'json']), \
                    self.timeout(TIMEOUT), \
                    self.timer(TIMEOUT):
                result = func(*params)
        self.assertEqual(type(result), type(expected),
                         ('The output type should be: float\n'
                          '[Il tipo di dato in output deve essere: float]'))
        self.assertEqual(result, expected,
                         ('The return value is incorrect\n'
                          '[Il valore di ritorno è errato]'))
        if fexpected:
            self.check_text_file(fexpected, fout, ('The content of the file is incorrect\n'
                          '[Il contenuto del file generato è inesatto]'))
            os.remove(fout)
        return 1
    ############# STUDENT AVERAGE ###########
    @data(  # test-id    params        expected           timeout
            ( 'sa1_s',   ('1838026', 'small'),    23.75,    0.5),
            ( 'sa1_m',   ('1662230', 'medium'),   27.0,     0.5),
            ( 'sa1_l',   ('1970461', 'large'),    28.0,     0.5),
            )
    @unpack
    def test_student_average(self, test, params, expected, timeout):
        try:
            from program01 import student_average as f
        except ImportError:
            from program01 import media_studente as f
        return self.do_test(f, params, expected, timeout)

    ############# COURSE AVERAGE ###########
    @data(  # test-id    params        expected           timeout
            ( 'ca1_s',   ('TIPAPFC0xa0bb4a', 'small'), 24.56,    0.5),
            ( 'ca1_m',   ('CELE0xc62458', 'medium'),   23.21,     0.5),
            ( 'ca1_l',   ('MASP0x6f69a0', 'large'),    23.42,     0.5),
            )
    @unpack
    def test_course_average(self, test, params, expected, timeout):
        try:
            from program01 import course_average as f
        except ImportError:
            from program01 import media_corso as f
        return self.do_test(f, params, expected, timeout)


    ############# TEACHER AVERAGE ###########
    @data(  # test-id    params        expected           timeout
            ( 'ta1_s',   ('003', 'small'),   24.64,    0.5),
            ( 'ta1_m',   ('0023', 'medium'), 24.14,     0.5),
            ( 'ta1_l',   ('00059', 'large'), 24.14,     0.5),
            )
    @unpack
    def test_teacher_average(self, test, params, expected, timeout):
        try:
            from program01 import teacher_average as f
        except ImportError:
            from program01 import media_docente as f
        return self.do_test(f, params, expected, timeout)

    ############# TOP STUDENTs ###########
    @data(  # test-id    params    expected  timeout
            ( 'ts1_s',   ('small',),  ['1324812', '1882282', '1659373', '1675598'],   2),
            ( 'ts1_m',   ('medium',), ['1720392', '1694135', '1468470', '1517980', '1341550', '1595788', '1270093', '1605040', '1441484', '1744923', '1818375', '1235494', '1550419', '1686446', '1545592', '1517364', '1630594', '1543995', '1870113', '1907578', '1512987', '1878395', '1532154', '1845528', '1320971', '1645512', '1575805', '1932828', '1877490', '1829148', '1531581', '1454027', '1346065', '1805812', '1993350', '1288356'],   3),
            ( 'ts1_l',   ('large',),  ['1516973', '1378631', '1988517', '1326300', '1436970', '1482842', '1538091', '1592110', '1868602', '1317644', '1395456', '1611570', '1759846', '1589681', '1890003', '1566789', '1571440', '1532361', '1508007', '1367077', '1414035', '1654889', '1858804', '1425529', '1560128', '1748515', '1322891', '1247833', '1756575', '1528621', '1249743', '1617249', '1567501', '1675793', '1901198', '1826231', '1778183', '1968969', '1571163', '1460335', '1863275', '1411120', '1509915', '1659098', '1283397', '1485640', '1643763', '1839407', '1346996', '1805334', '1800103', '1517901', '1843223', '1843224', '1851787', '1632376', '1922417', '1737557', '1497197', '1239597', '1480056', '1749780', '1747280', '1313273', '1790081', '1881978', '1238022', '1854017', '1545662', '1728926', '1812601', '1367499', '1820545', '1796051', '1509254', '1281525', '1549168', '1764862', '1910532', '1626006', '1600480', '1566983', '1893339', '1650859', '1890360', '1235060', '1728506', '1694063', '1384876', '1859940', '1986254', '1970461', '1976236'],   4),
            )
    @unpack
    def test_top_students(self, test, params, expected, timeout):
        try:
            from program01 import top_students as f
        except ImportError:
            from program01 import studenti_brillanti as f
        return self.do_test(f, params, expected, timeout)


    ############# PRINT RECORDED EXAMS ###########
    @data(  # test-id    params        expected           timeout
            ( 'pre1_s', ('1838026', 'small', 'test_pre1_s.txt'),  4,  0.5, 'test_pre1_s.txt', (exdir+'pre1_s.expit.txt', exdir+'pre1_s.expen.txt')),
            ( 'pre1_m', ("1662230", 'medium', 'test_pre1_m.txt'), 15, 0.5, 'test_pre1_m.txt', (exdir+'pre1_m.expit.txt', exdir+'pre1_m.expen.txt')),
            ( 'pre1_l', ('1970461', 'large', 'test_pre1_l.txt'),  4,  0.5, 'test_pre1_l.txt', (exdir+'pre1_l.expit.txt', exdir+'pre1_l.expen.txt'))
            )
    @unpack
    def test_print_recorded_exams(self, test, params, expected, timeout, fout, fexp):
        try:
            from program01 import print_recorded_exams as f
            fexp = fexp[1]
        except ImportError:
            from program01 import stampa_esami_sostenuti as f
            fexp = fexp[0]
        print(f'Using {fexp}')
        return self.do_test(f, params, expected, timeout, fout, fexp)


    ############# PRINT TOP STUDENTS ###########
    @data(  # test-id    params        expected           timeout
            ( 'pts1_s', ('small', 'test_pts1_s.txt'),  4,  2, 'test_pts1_s.txt', exdir+'pts1_s.expit.txt'),
            ( 'pts1_m', ('medium', 'test_pts1_m.txt'), 36, 3, 'test_pts1_m.txt', exdir+'pts1_m.expit.txt'),
            ( 'pts1_l', ('large', 'test_pts1_l.txt'),  93, 4, 'test_pts1_l.txt', exdir+'pts1_l.expit.txt'),
            )
    @unpack
    def test_print_top_students(self, test, params, expected, timeout, fout, fexp):
        try:
            from program01 import print_top_students as f
        except ImportError:
            from program01 import stampa_studenti_brillanti as f
        return self.do_test(f, params, expected, timeout, fout, fexp)


    ############# PRINT EXAM RECORD ###########
    @data(  # test-id    params        expected           timeout
            ( 'per1_s', (447, 'small', 'test_per1_s.txt'),   18,  0.5, 'test_per1_s.txt', (exdir+'per1_s.expit.txt', exdir+'per1_s.expen.txt')),
            ( 'per1_m', (2824, 'medium', 'test_per1_m.txt'),  19, 0.5, 'test_per1_m.txt', (exdir+'per1_m.expit.txt', exdir+'per1_m.expen.txt')),
            ( 'per1_l', (4265, 'large', 'test_per1_l.txt'),  21,  0.5, 'test_per1_l.txt', (exdir+'per1_l.expit.txt', exdir+'per1_l.expen.txt'))
            )
    @unpack
    def test_print_exam_record(self, test, params, expected, timeout, fout, fexp):
        try:
            from program01 import print_exam_record as f
            fexp=fexp[1]
        except ImportError:
            from program01 import stampa_verbale as f
            fexp=fexp[0]
        return self.do_test(f, params, expected, timeout, fout, fexp)
    ######################### SECRET TESTS START HERE! #########################


if __name__ == '__main__':
    Test.main()

