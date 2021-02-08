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

        for val in corpus2.docs:
            self.assertEqual(isinstance(val, corpusDoc), True)

        self.assertEqual(corpus2.dic[0], "hors")
        self.assertEqual(corpus2.dic[1], "mcmaster")

        # TODO Contains Failed case
        self.assertEqual(corpus2.stemDic.get("Dog", 0), "Dog")
        self.assertEqual(corpus2.stemDic.get("cat", 0), "cat")
        self.assertEqual(corpus2.stemDic.get("horse", 0), "horse")
        self.assertEqual(corpus2.stemDic.get("mcmaster", 0), "mcmaster")

        i3 = inputCorpus()
        i3.addDoc("TestTitle", "And then I was king william james")
        corpus2 = preProcess(i3)
        for val in corpus2.docs:
            self.assertEqual(isinstance(val, corpusDoc), True)

        self.assertEqual(corpus2.stemDic.get("king", 0), "king")
        self.assertEqual(corpus2.stemDic.get("william", 0), "william")
        self.assertEqual(corpus2.stemDic.get("james", 0), "james")

        i3 = inputCorpus()
        i3.addDoc("TestTitle", "dancing running flying kicking")
        corpus2 = preProcess(i3)
        for val in corpus2.docs:
            self.assertEqual(isinstance(val, corpusDoc), True)

        self.assertEqual(corpus2.stemDic.get("danc", 0), "dancing")
        self.assertEqual(corpus2.stemDic.get("run", 0), "kicking")
        self.assertEqual(corpus2.stemDic.get("fly", 0), "flying")

    def test_preProcessSentence(self):
        # pre-process individual sentences by creating a bag of words
        i = inputCorpus()
        i.addDoc("TestTitle", "This is a test case")
        corpus = preProcess(i)
        x = preProcessSentence("This is a test case", corpus.dic)
        self.assertEqual(x, [(0, 1), (1, 1)])

    def test_jamesLemmatize(self):
        # Lemmatize and stem text
        x = jamesLemmatize("This is a test case", 3, True, False)
        # print(x)
        self.assertEqual(x["lemmatized"], ['test', 'case'])
        y = jamesLemmatize("This is a test case", 3, False, False)
        self.assertEqual(y["lemmatized"], ['test', 'case'])

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
        self.assertEqual(sentenceFilter('abc'), True)
        self.assertEqual(sentenceFilter('a'), True)
        self.assertEqual(sentenceFilter('z'), True)
        self.assertEqual(sentenceFilter('aaaaaaaa'), True)
        self.assertEqual(sentenceFilter('aaaaaaaazzzzzzz'), True)

        # Test for uppercase letters
        self.assertEqual(sentenceFilter('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), True)
        self.assertEqual(sentenceFilter('ABC'), True)
        self.assertEqual(sentenceFilter('A'), True)
        self.assertEqual(sentenceFilter('Z'), True)
        self.assertEqual(sentenceFilter('AAAAAAAAAAAAAA'), True)
        self.assertEqual(sentenceFilter('ZZZZZZZZZZZZZZZZZZZZ'), True)

        self.assertEqual(sentenceFilter(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'), True)

        # Test for numbers and letters
        self.assertEqual(sentenceFilter('123456789ABCD'), True)
        self.assertEqual(sentenceFilter('123456789ABCDefgh'), True)
        self.assertEqual(sentenceFilter('aaaaa11111'), True)
        self.assertEqual(sentenceFilter('1111111a'), True)
        self.assertEqual(sentenceFilter('aaaaaaaaaa1231'), True)
        self.assertEqual(sentenceFilter('    1 223aaa'), True)
        self.assertEqual(sentenceFilter('???223aaa'), True)

        # Test for a single character
        self.assertEqual(sentenceFilter('T'), True)
        self.assertEqual(sentenceFilter('Z'), True)
        self.assertEqual(sentenceFilter(' Z'), True)
        self.assertEqual(sentenceFilter('             Z'), True)

        # Test for numbers
        self.assertEqual(sentenceFilter('123456789'), False)
        self.assertEqual(sentenceFilter(
            '123456789123456789123456789123456789'), False)
        self.assertEqual(sentenceFilter('               123456789'), False)
        self.assertEqual(sentenceFilter(
            '             123456789            '), False)

        # Test for empty string
        self.assertEqual(sentenceFilter(''), False)

        # Test for special characters
        self.assertEqual(sentenceFilter('!@#$%^&*'), False)
        self.assertEqual(sentenceFilter('        '), False)

        # Test for invalid inputs
        with self.assertRaises(TypeError):
            sentenceFilter(12)
        with self.assertRaises(TypeError):
            sentenceFilter(99999999)
        with self.assertRaises(TypeError):
            sentenceFilter(3.14)
        # pass


if __name__ == '__main__':
    unittest.main()
