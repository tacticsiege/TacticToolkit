import unittest

from ttk.preprocessing import SeqPaddingTransformer

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

if __name__ == '__main__':
    unittest.main()
