import unittest

from ttk.preprocessing import Seq2IndexTransformer

class Seq2IndexTransformerTests(unittest.TestCase):

    def setUp(self):
        self.transformer = Seq2IndexTransformer()
        pass

    def test_fit_transform(self):

        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]
        self.assertFalse(self.transformer._fit)
        self.transformer, indexed_sentences = self.transformer.fit_transform(X)
        self.assertIsNotNone(self.transformer)
        self.assertIsNotNone(indexed_sentences)

        self.assertTrue(self.transformer._fit)

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
        self.assertFalse(self.transformer._fit)
        self.transformer = self.transformer.fit(X)
        self.assertIsNotNone(self.transformer)
        self.assertTrue(self.transformer._fit)

        # 0:start, 1:end
        # 2:I, 3:love, 4:dogs, 5:cats, 6:only, 7:like
        self.assertEqual([0, 2, 3, 4, 1], self.transformer.transform([['I', 'love', 'dogs']])[0])
        self.assertEqual([0, 2, 7, 5, 1], self.transformer.transform([['I', 'like', 'cats']])[0])


    def test_partial_fit(self):

        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            #['I', 'only', 'like', 'cats'],
        ]
        self.assertFalse(self.transformer._fit)
        self.transformer = self.transformer.partial_fit(X)
        self.assertIsNotNone(self.transformer)
        self.assertTrue(self.transformer._fit)

        # 0:start, 1:end
        # 2:I, 3:love, 4:dogs, 5:cats, !(6:only, 7:like)
        self.assertEqual([0, 2, 3, 4, 1,], self.transformer.transform([['I', 'love', 'dogs']])[0])
        self.assertEqual(6, len(self.transformer.idx2obj))

        self.transformer = self.transformer.partial_fit([['I', 'only', 'like', 'cats']])
        # includes 6:only, 7:like
        self.assertEqual(8, len(self.transformer.idx2obj))
        self.assertEqual([0, 2, 7, 6, 4, 1], self.transformer.transform([['I', 'like', 'only', 'dogs']])[0])


    def test_transform(self):

        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]
        self.assertFalse(self.transformer._fit)
        self.transformer = self.transformer.fit(X)
        self.assertIsNotNone(self.transformer)
        self.assertTrue(self.transformer._fit)
        
        indexed_sentences = self.transformer.transform(X)
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
        self.assertFalse(self.transformer._fit)
        self.transformer = self.transformer.fit(X)
        self.assertIsNotNone(self.transformer)
        self.assertTrue(self.transformer._fit)

        x1 = [0, 2, 3, 4, 1]
        x2 = [0, 2, 3, 5, 1]
        x3 = [0, 2, 6, 7, 5, 1]
                
        self.assertEqual(X[0], self.transformer.inverse_transform([x1])[0][1:-1])
        self.assertEqual(X[1], self.transformer.inverse_transform([x2])[0][1:-1])
        self.assertEqual(X[2], self.transformer.inverse_transform([x3])[0][1:-1])


    def test_mapping_func_provided(self):
        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],            
        ]

        def token_len(t, s):
            print ('len:', t, 'for:', s)
            return len(t)

        transformer = Seq2IndexTransformer(token_mapping_func=token_len)
        self.assertFalse(transformer._fit)
        transformer, indexed_sentences = transformer.fit_transform(X)
        self.assertIsNotNone(transformer)
        self.assertIsNotNone(indexed_sentences)

        self.assertTrue(transformer._fit)

        self.assertEqual(len(X), len(indexed_sentences))
        print ('i0:', indexed_sentences[0])
        self.assertEqual(['START', 1, 4, 4, 'END'], transformer.inverse_transform([indexed_sentences[0]])[0])
        self.assertEqual(['START', 1, 4, 4, 'END'], transformer.inverse_transform([indexed_sentences[1]])[0])
        self.assertEqual(['START', 1, 4, 4, 4, 'END'], transformer.inverse_transform([indexed_sentences[2]])[0])

        # works on set
        untransformed = transformer.inverse_transform(indexed_sentences)
        self.assertEqual(['START', 1, 4, 4, 'END'], untransformed[0])
        self.assertEqual(['START', 1, 4, 4, 'END'], untransformed[1])
        self.assertEqual(['START', 1, 4, 4, 4, 'END'], untransformed[2])

    def test_filter_func_provided(self):
        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]
        
        def filter_func(t, s):
            if len(t) > 2:
                return True
            return False

        transformer = Seq2IndexTransformer(token_filter_func=filter_func)
        self.assertFalse(transformer._fit)
        transformer, indexed_sentences = transformer.fit_transform(X)
        self.assertIsNotNone(transformer)
        self.assertIsNotNone(indexed_sentences)

        self.assertTrue(transformer._fit)
        self.assertEqual(len(X), len(indexed_sentences))

        # 0:start, 1:end
        # 2:love, 3:dogs, 4:cats, 5:only, 6:like
        x1 = [0, 2, 3, 1]
        x2 = [0, 2, 4, 1]
        x3 = [0, 5, 6, 4, 1]
                
        self.assertEqual(['love', 'dogs'], transformer.inverse_transform([x1])[0][1:-1])
        self.assertEqual(['love', 'cats'], transformer.inverse_transform([x2])[0][1:-1])
        self.assertEqual(['only', 'like', 'cats'], transformer.inverse_transform([x3])[0][1:-1])

    def test_one_hot_encoded(self):
        X = [['Word', 'Another'],
             ['Word', 'Different']]
        transformer = Seq2IndexTransformer(one_hot=True)
        transformer, indexed_sentences = transformer.fit_transform(X)
        self.assertIsNotNone(transformer)
        self.assertIsNotNone(indexed_sentences)
        print ('Indexed_sentences:', indexed_sentences)
        print ('i0:', indexed_sentences[0])
        print ('i1:', indexed_sentences[1])

        x0 = indexed_sentences[0][1:-1]
        x1 = indexed_sentences[1][1:-1]

        print ('x0:',type(x0))
        print ('x0[0]', x0[0])
        print ('x0[0]', type(x0[0]))
        
        self.assertEqual([[0, 0, 1, 0, 0], [0, 0, 0, 1, 0]], x0)
        self.assertEqual([[0, 0, 1, 0, 0], [0, 0, 0, 0, 1]], x1)
        

    def test_fit_transform_no_delimiters(self):
        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]

        transformer = Seq2IndexTransformer(add_delimiters=False)
        self.assertFalse(transformer._fit)
        transformer, indexed_sentences = transformer.fit_transform(X)
        self.assertIsNotNone(transformer)
        self.assertIsNotNone(indexed_sentences)

        self.assertTrue(transformer._fit)

        self.assertEqual(len(X), len(indexed_sentences))
        # 0:start, 1:end
        # 2:I, 3:love, 4:dogs, 5:cats, 6:only, 7:like

        self.assertEqual([2, 3, 4,], indexed_sentences[0])
        self.assertEqual([2, 3, 5,], indexed_sentences[1])
        self.assertEqual([2, 6, 7, 5,], indexed_sentences[2])


    def test_fit_transform_no_delimiters_one_hot(self):
        X = [
            ['I', 'love', 'dogs'],
            ['I', 'love', 'cats'],
            ['I', 'only', 'like', 'cats'],
        ]

        transformer = Seq2IndexTransformer(add_delimiters=False)
        self.assertFalse(transformer._fit)
        transformer, indexed_sentences = transformer.fit_transform(X)
        self.assertIsNotNone(transformer)
        self.assertIsNotNone(indexed_sentences)

        self.assertTrue(transformer._fit)

        self.assertEqual(len(X), len(indexed_sentences))
        # 0:start, 1:end
        # 2:I, 3:love, 4:dogs, 5:cats, 6:only, 7:like

        self.assertEqual([2, 3, 4,], indexed_sentences[0])
        self.assertEqual([2, 3, 5,], indexed_sentences[1])
        self.assertEqual([2, 6, 7, 5,], indexed_sentences[2])


if __name__ == '__main__':
    unittest.main()
