import testlib
import random
from ddt import file_data, ddt, data, unpack

# TODO TBD

# change this variable to True to disable timeout and enable print
DEBUG=True
DEBUG=False

@ddt
class Test(testlib.TestCase):
    def do_test(self, acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log, expected):
        """Test implementation
        - acn1, acn2, acn3:   account numbers of player 1, 2 and 3
        - imd_acn1, imd_acn2: account numbers of intermediaries 1 and 2
        - init_amount:        initial amount in the players’ accounts
        - transact_log:       a list of transactions
        - expected:           expected result
        TIMEOUT: 2 seconds for each test
        """
        if DEBUG:
                import program01 as program
                result = program.ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log)
        else:
            with    self.ignored_function('builtins.print'), \
                    self.ignored_function('pprint.pprint'), \
                    self.forbidden_function('builtins.input'), \
                    self.forbidden_function('builtins.eval'), \
                    self.forbidden_function('builtins.open'), \
                    self.check_imports(allowed=['program01','_io']), \
                    self.timeout(2), \
                    self.timer(2):
                import program01 as program
                result = program.ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log)
        self.assertEqual(type(result), tuple,
                         ('The output type should be: list\n'
                          '[Il tipo di dato in output deve essere: list]'))
        self.assertEqual(type(result[0]), list,
                         ('The first element of the output should be: a '
                          'list\n'
                          '[Il primo elemento in output deve essere: una '
                          'list]'))
        self.assertEqual(len(result[0]), 3,
                         ('The first element of the output should be: a '
                          'list of length 3\n'
                          '[Il primo elemento in output deve essere: una '
                          'list di lunghezza 3]'))
        self.assertEqual(type(result[1]), list,
                         ('The second element of the output should be: a '
                          'list\n'
                          '[Il secondo elemento in output deve essere: una '
                          'list]'))
        self.assertEqual(len(result[1]), 2,
                         ('The second element of the output should be: a '
                          'list of length 2\n'
                          '[Il secondo elemento in output deve essere: una '
                          'list di lunghezza 2]'))
        self.assertEqual(type(result[2]), list,
                         ('The third element of the output should be: a '
                          'list\n'
                          '[Il terzo elemento in output deve essere: una '
                          'list]'))
        self.assertEqual(len(result[2]), 2,
                         ('The third element of the output should be: a '
                          'list of length 2\n'
                          '[Il terzo elemento in output deve essere: una '
                          'list di lunghezza 2]'))
        self.assertEqual(type(result[2][0]), list,
                         ('The third element of the output should be: a '
                          'list of lists\n'
                          '[Il terzo elemento in output deve essere: una '
                          'lista di list]'))
        self.assertEqual(len(result[2][0]), 3,
                         ('The third element of the output should be: a '
                          'list of lists, each of length 3\n'
                          '[Il terzo elemento in output deve essere: una '
                          'lista di list, ognuna di lunghezza 3]'))
        self.assertEqual(result, tuple(expected),
                         ('The return value is incorrect\n'
                          '[Il valore di ritorno è errato]'))
        return 1

    def test_example1(self):
        acn1 = 0x5B23
        acn2 = 0xC78D
        acn3 = 0x44AE
        imd_acn1 = 0x1612
        imd_acn2 = 0x90FF
        init_amount = 1000
        transact_log = \
            [((0x44AE, 0x5B23), 800, 0x1612, 4),
             ((0x44AE, 0xC78D), 800, 0x90FF, 10),
             ((0xC78D, 0x5B23), 400, 0x1612, 8),
             ((0x44AE, 0xC78D), 1800, 0x90FF, 12),
             ((0x5B23, 0x44AE), 100, 0x1612, 2)]
        expected = [[2098, 568, 0], [66, 268], [[0, 0, 0], [0, 0, -28]]]
        return self.do_test(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log, expected)

    def test_example2(self):
        acn1 = 0xA1
        acn2 = 0xD0
        acn3 = 0x52F
        imd_acn1 = 0x108
        imd_acn2 = 0x2A9
        init_amount = 2000
        transact_log = \
            [((0xA1, 0xD0), 2000, 0x108, 0),
             ((0xA1, 0xD0), 1800, 0x108, 12),
             ((0xA1, 0xD0), 1800, 0x2A9, 12),
             ((0xD0, 0x52F), 200, 0x2A9, 0),
             ((0xD0, 0x52F), 200, 0x2A9, 0)]
        expected = [[0, 3600, 2400], [0, 0], [[-216, 0, 0], [-216, 0, 0]]]
        return self.do_test(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log, expected)

    @file_data("test_init-1000_txs-10.json")
    def test_json1(self, acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected):
        return self.do_test(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected)

    @file_data("test_init-2000_txs-100.json")
    def test_json2(self, acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected):
        return self.do_test(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                            transact_log, expected)

    @file_data("test_init-3000_txs-1000.json")
    def test_json3(self, acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected):
        return self.do_test(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected)

    @file_data("test_init-4000_txs-10000.json")
    def test_json4(self, acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected):
        return self.do_test(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                            transact_log, expected)

    @file_data("test_init-5000_txs-100000.json")
    def test_json5(self, acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected):
        return self.do_test(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected)

    @file_data("test_init-6000_txs-1000000.json")
    def test_json6(self, acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                   transact_log, expected):
        return self.do_test(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount,
                            transact_log, expected)


if __name__ == '__main__':
    Test.main()


