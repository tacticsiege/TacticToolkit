import unittest
import numpy as np

from ttk.preprocessing import Seq2WordVecTransformer

class Seq2WordVecTransformerTests(unittest.TestCase):

    def setUp(self):
        self.example_X = [
            ['sentence', 'one', 'has', 'words'],
            ['one', 'more', 'sentence', 'which', 'has', 'words'],
            ['additional', 'sentence', 'has', 'a', 'few', 'words'],
        ]


    def test_fit_transform(self):
        transformer = Seq2WordVecTransformer()
        self.assertFalse(transformer._fit)

        transformed = transformer.fit_transform(self.example_X)
        self.assertEqual(len(self.example_X), len(transformed))
        for i in range(len(transformed)):
            self.assertEqual(len(self.example_X[i]), len(transformed[i]))
            # every element is a word vector
            for wv in transformed[i]:
                self.assertEqual(type(np.ndarray(1)), type(wv))

        self.assertTrue(transformer._fit)

    def test_inverse_tranform(self):
        transformer = Seq2WordVecTransformer()
        transformed = transformer.fit_transform(self.example_X)
        inversed = transformer.inverse_transform(transformed)
        for i in range(len(inversed)):
            self.assertEqual(self.example_X[i], inversed[i])

if __name__ == '__main__':
    unittest.main()
