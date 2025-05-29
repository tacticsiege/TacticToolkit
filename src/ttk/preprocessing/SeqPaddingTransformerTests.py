import unittest
import importlib.util
import os

# Import SeqPaddingTransformer without loading additional preprocessing modules
module_path = os.path.join(os.path.dirname(__file__), 'SeqPaddingTransformer.py')
spec = importlib.util.spec_from_file_location('SeqPaddingTransformer', module_path)
_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_module)
SeqPaddingTransformer = _module.SeqPaddingTransformer

class SeqPaddingTransformerTests(unittest.TestCase):
    
    
    def setUp(self):
        self.example_X = [
            ['Two', 'Words'] ,
            ['Four', 'Words', 'In', 'This'],
            ['Three', 'Words', 'now'],
        ]
    
    def test_fit_transform(self):
        transformer = SeqPaddingTransformer()
        self.assertFalse(transformer._fit)

        X = transformer.fit_transform(self.example_X)
        for x in X:
            self.assertEqual(4, len(x))

        self.assertEqual(['Two', 'Words', 0.0, 0.0], X[0])
        self.assertEqual(['Four', 'Words', 'In', 'This'], X[1])
        self.assertEqual(['Three', 'Words', 'now', 0.0], X[2])

        self.assertTrue(transformer._fit)

    def test_inverse_transform(self):
        transformer = SeqPaddingTransformer()

        # doesn't even need fitting
        y = [
            ['Two', 'Words', 0.0, 0.0],
            ['Four', 'Words', 'In', 'This'],
            ['Three', 'Words', 'now', 0.0],
        ]

        tranformed = transformer.inverse_transform(y)
        self.assertEqual(3, len(tranformed))
        self.assertEqual(self.example_X[0], tranformed[0])
        self.assertEqual(self.example_X[1], tranformed[1])
        self.assertEqual(self.example_X[2], tranformed[2])

    def test_fit_transform_vectors(self):
        import numpy as np

        seqs = [
            [np.array([1.0, 2.0])],
            [np.array([3.0, 4.0]), np.array([5.0, 6.0])]
        ]

        transformer = SeqPaddingTransformer()
        padded = transformer.fit_transform(seqs)

        # Expect shape (2, max_len) where max_len == 2
        self.assertEqual(2, len(padded))
        for p in padded:
            self.assertEqual(2, len(p))

        # Padding should be zero vectors
        self.assertEqual([0.0, 0.0], padded[0][1])

        # Inverse transform should recover original sequences
        inv = transformer.inverse_transform(padded)
        self.assertEqual(seqs[0][0], inv[0][0])
        self.assertEqual(seqs[1][0], inv[1][0])
        self.assertEqual(seqs[1][1], inv[1][1])

if __name__ == '__main__':
    unittest.main()
