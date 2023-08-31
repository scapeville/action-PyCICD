import unittest

from engine.check_commit_msg import parser

from engine.constants import UPDATE_VER_MSG


class Test__parser(unittest.TestCase):

    def test_no_match(self):

        result = parser('')
        self.assertEqual(result, None)

        result = parser('abc')
        self.assertEqual(result, None)

        result = parser('abc xyz #123')
        self.assertEqual(result, None)

        result = parser('abc#xyz')
        self.assertEqual(result, None)

        result = parser('abc#1.1.1')
        self.assertEqual(result, None)

        result = parser('abc 1.1.1')
        self.assertEqual(result, None)

        result = parser('#t 1.0.0 foo')
        self.assertEqual(result, None)

        result = parser('#r 1.0.0 foo')
        self.assertEqual(result, None)

        result = parser('foo #r 1.0.0b3 foo')
        self.assertEqual(result, None)

    def test_call_commit(self):

        ## Fails

        with self.assertRaises(AssertionError) as ctx: parser('foo #r1.0.0b')
        self.assertEqual(str(ctx.exception), "The release version '1.0.0b' cannot be labeled as 'beta'.")

        with self.assertRaises(AssertionError) as ctx: parser('foo #t 1.0.0')
        self.assertEqual(str(ctx.exception), "The testing version '1.0.0' must carry the label 'beta'.")

        ## Passes

        result = parser('foo #r1.0.0')
        expected = ('call', ['r', '1.0.0', 'foo'])
        self.assertEqual(result, expected)

        result = parser('foo #bar baz #r 1.3.5')
        expected = ('call', ['r', '1.3.5', 'foo #bar baz'])
        self.assertEqual(result, expected)

        result = parser('foo#t0.1.0b')
        expected = ('call', ['t', '0.1.0b', 'foo'])
        self.assertEqual(result, expected)

        result = parser('foo #52 bar   #t1.0.0 ')
        expected = ('call', ['t', '1.0.0', 'foo #52 bar'])
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()