import unittest

from ttk.preprocessing import Seq2IndexVectorizer

class SequenceTests(unittest.TestCase):

    def setUp(self):
        self.vectorizer = Seq2IndexVectorizer()

    def test_fit_transform(self):

        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]
        self.assertFalse(self.vectorizer._fit)
        self.vectorizer, indexed_sentences = self.vectorizer.fit_transform(X)
        self.assertIsNotNone(self.vectorizer)
        self.assertIsNotNone(indexed_sentences)

        self.assertTrue(self.vectorizer._fit)

        self.assertEqual(len(X), len(indexed_sentences))
        # 0:start, 1:end
        # 2:I, 3:love, 4:dogs, 5:cats, 6:only, 7:like

        self.assertEqual([0, 2, 3, 4, 1,], indexed_sentences[0])
        self.assertEqual([0, 2, 3, 5, 1], indexed_sentences[1])
        self.assertEqual([0, 2, 6, 7, 5, 1], indexed_sentences[2])

    def test_fit(self):

        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]
        self.assertFalse(self.vectorizer._fit)
        self.vectorizer = self.vectorizer.fit(X)
        self.assertIsNotNone(self.vectorizer)
        self.assertTrue(self.vectorizer._fit)

        # 0:start, 1:end
        # 2:I, 3:love, 4:dogs, 5:cats, 6:only, 7:like
        self.assertEqual([0, 2, 3, 4, 1,], self.vectorizer.transform([['I', 'love', 'dogs']])[0])
        self.assertEqual([0, 2, 7, 5, 1], self.vectorizer.transform([['I', 'like', 'cats']])[0])


    def test_partial_fit(self):

        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            #['I', 'only', 'like', 'cats'],
        ]
        self.assertFalse(self.vectorizer._fit)
        self.vectorizer = self.vectorizer.partial_fit(X)
        self.assertIsNotNone(self.vectorizer)
        self.assertTrue(self.vectorizer._fit)

        # 0:start, 1:end
        # 2:I, 3:love, 4:dogs, 5:cats, !(6:only, 7:like)
        self.assertEqual([0, 2, 3, 4, 1,], self.vectorizer.transform([['I', 'love', 'dogs']])[0])
        self.assertEqual(6, len(self.vectorizer.idx2obj))

        self.vectorizer = self.vectorizer.partial_fit([['I', 'only', 'like', 'cats']])
        # includes 6:only, 7:like
        self.assertEqual(8, len(self.vectorizer.idx2obj))
        self.assertEqual([0, 2, 7, 6, 4, 1], self.vectorizer.transform([['I', 'like', 'only', 'dogs']])[0])


    def test_transform(self):

        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]
        self.assertFalse(self.vectorizer._fit)
        self.vectorizer = self.vectorizer.fit(X)
        self.assertIsNotNone(self.vectorizer)
        self.assertTrue(self.vectorizer._fit)
        
        indexed_sentences = self.vectorizer.transform(X)
        self.assertIsNotNone(indexed_sentences)        

        self.assertEqual(len(X), len(indexed_sentences))
        # 0:start, 1:end
        # 2:I, 3:love, 4:dogs, 5:cats, 6:only, 7:like

        self.assertEqual([0, 2, 3, 4, 1,], indexed_sentences[0])
        self.assertEqual([0, 2, 3, 5, 1], indexed_sentences[1])
        self.assertEqual([0, 2, 6, 7, 5, 1], indexed_sentences[2])


    def test_inverse_transform(self):
        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]
        self.assertFalse(self.vectorizer._fit)
        self.vectorizer = self.vectorizer.fit(X)
        self.assertIsNotNone(self.vectorizer)
        self.assertTrue(self.vectorizer._fit)

        x1 = [0, 2, 3, 4, 1]
        x2 = [0, 2, 3, 5, 1]
        x3 = [0, 2, 6, 7, 5, 1]
                
        self.assertEqual(X[0], self.vectorizer.inverse_transform([x1])[0][1:-1])
        self.assertEqual(X[1], self.vectorizer.inverse_transform([x2])[0][1:-1])
        self.assertEqual(X[2], self.vectorizer.inverse_transform([x3])[0][1:-1])


if __name__ == '__main__':
    unittest.main()
