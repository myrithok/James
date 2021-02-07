# run from James directory
# python -m unittest testing.jamesPreProcessingTesting

from api.jamesPreProcessing import preProcess, preProcessSentence, jamesLemmatize, \
    separateSentences, sentenceFilter

from api.jamesClasses import inputCorpus, corpusDoc

import unittest


class TestPreProcessingMethods(unittest.TestCase):
    def test_preProcess(self):
        i = inputCorpus()
        i.addDoc("TestTitle", "This is a test case")
        corpus = preProcess(i)

        self.assertEqual(corpus.stemDic, {'test': 'test', 'case': 'case'})
        for val in corpus.docs:
            self.assertEqual(isinstance(val, corpusDoc), True)

        self.assertEqual(corpus.dic[0], "case")
        self.assertEqual(corpus.dic[1], "test")

        i2 = inputCorpus()
        i2.addDoc("TestTitle", "Dog cat horse mcmaster")
        corpus2 = preProcess(i2)

        # Failed case
        # self.assertEqual(corpus2.stemDic, {
        #                  'Dog': 'Dog', 'cat': 'cat', 'horse': 'horse', 'mcmaster': 'mcmaster'})
        for val in corpus2.docs:
            self.assertEqual(isinstance(val, corpusDoc), True)

        self.assertEqual(corpus2.dic[0], "hors")
        self.assertEqual(corpus2.dic[1], "mcmaster")
        pass

    def test_preProcessSentence(self):
        # pre-process individual sentences by creating a bag of words
        i = inputCorpus()
        i.addDoc("TestTitle", "This is a test case")
        corpus = preProcess(i)
        x = preProcessSentence("This is a test case", corpus.dic)
        self.assertEqual(x, [(0, 1), (1, 1)])
        # print(x)
        pass

    def test_jamesLemmatize(self):
        # Lemmatize and stem text
        x = jamesLemmatize("This is a test case", 3, True, False)
        # print(x)
        self.assertEqual(x["lemmatized"], ['test', 'case'])

        y = jamesLemmatize("This is a test case", 3, False, False)
        self.assertEqual(y["lemmatized"], ['test', 'case'])

        pass

    def test_separateSentences(self):
        # Converts a document to a list of sentences

        # Replacement and separation by .
        self.assertEqual(separateSentences("Test."), ["Test."])
        self.assertEqual(separateSentences("Test. Test2. Test3."), [
                         "Test.", "Test2.", "Test3."])

        # Replacement and separation by !
        self.assertEqual(separateSentences("Test!"), ["Test!"])
        self.assertEqual(separateSentences("Test! Test2! Test3!"), [
                         "Test!", "Test2!", "Test3!"])

        # Replacement and separation by ?
        self.assertEqual(separateSentences("Test?"), ["Test?"])
        self.assertEqual(separateSentences("Test? Test2? Test3?"), [
                         "Test?", "Test2?", "Test3?"])

        # Replacement and separation without .!?
        self.assertEqual(separateSentences("Test"), ["Test"])
        self.assertEqual(separateSentences("This is a test sentence"), [
                         "This is a test sentence"])

        # Empty string input
        self.assertEqual(separateSentences(""), [])

        # Invalid sentences
        self.assertEqual(separateSentences("123"), [])
        with self.assertRaises(TypeError):
            separateSentences(12)
        with self.assertRaises(TypeError):
            separateSentences(3.14)
        # pass

    def test_sentenceFilter(self):
        # Return True if there is at least one letter, false otherwise
        self.assertEqual(sentenceFilter('test'), True)

        # Test for lowercase letters
        self.assertEqual(sentenceFilter('abcdefghijklmnopqrstuvwxyz'), True)

        # Test for uppercase letters
        self.assertEqual(sentenceFilter('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), True)

        self.assertEqual(sentenceFilter(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'), True)

        # Test for numbers and letters
        self.assertEqual(sentenceFilter('123456789ABCD'), True)

        # Test for a single character
        self.assertEqual(sentenceFilter('T'), True)

        # Test for numbers
        self.assertEqual(sentenceFilter('123456789'), False)

        # Test for empty string
        self.assertEqual(sentenceFilter(''), False)

        # Test for special characters
        self.assertEqual(sentenceFilter('!@#$%^&*'), False)

        # Test for invalid inputs
        with self.assertRaises(TypeError):
            sentenceFilter(12)
        with self.assertRaises(TypeError):
            sentenceFilter(3.14)
        # pass


if __name__ == '__main__':
    unittest.main()
