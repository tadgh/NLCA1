import unittest
import twtt

class TWTTTests(unittest.TestCase):
    def setUp(self):
        self.abbrevs = twtt.init_abbreviations()

    def test_posessive_clitic_is_split(self):
        tweet_sentence = "gary's is not peoples'"
        result = twtt.split_into_tokens(tweet_sentence)
        correct = ['gary', "'s", 'is', 'not', 'peoples', "'"]
        self.assertListEqual(result, correct)

    def test_splitting_into_sentences_unterminated(self):
        tweet = "Hello jonathan... Why do you hate me?is it because I can't punctuate...who knows. My name is gary?!?! This is my sentence...i think"
        result = twtt.split_into_sentences(tweet, self.abbrevs)
        answer = ['Hello jonathan...', 'Why do you hate me?', "is it because I can't punctuate...who knows.", 'My name is gary?!?!', 'This is my sentence...i think']
        self.assertListEqual(result, answer)

    def test_splitting_single_sentence(self):
        tweet = "Hello jonathan...what's up?"
        result = twtt.split_into_sentences(tweet, self.abbrevs)
        answer = ["Hello jonathan...what's up?"]
        self.assertListEqual(result, answer)


    def test_splitting_into_sentences_terminated(self):
        tweet = "Hello jonathan... Why do you hate me?is it because I can't punctuate...who knows. My name is gary?!?! This is my sentence...i think."
        result = twtt.split_into_sentences(tweet, self.abbrevs)
        answer = ['Hello jonathan...', 'Why do you hate me?', "is it because I can't punctuate...who knows.", 'My name is gary?!?!', 'This is my sentence...i think.']
        self.assertListEqual(result, answer)

    def test_splitting_into_sentences_with_abbreviations(self):
        tweet = "Hello Dr. Houston...how are st. you?"
        result = twtt.split_into_sentences(tweet, self.abbrevs)
        answer = ['Hello DR. Houston...how are ST. you?']
        self.assertListEqual(result, answer)

    def test_splitting_tweet_into_tokens(self):
        sentences = ['Hello jonathan...', 'Why do you hate me?', "is it because I can't punctuate...who knows.", 'My name is gary?!?!', 'This is my sentence...i think']
        result = twtt.split_all_sentences_into_tokens(sentences)
        answer = [['Hello', 'jonathan', '...'],
                  ['Why', 'do', 'you', 'hate', 'me', '?'],
                  ['is', 'it', 'because', 'I', 'ca', "n't", 'punctuate', '...', 'who', 'knows', '.'],
                  ['My', 'name', 'is', 'gary', '?', '!', '?', '!'], ['This', 'is', 'my', 'sentence', '...', 'i', 'think']]
        self.assertListEqual(result, answer)

    def test_stripping_urls_from_tweet(self):
        tweet = "www.obama.com http://www.whatever.nz obama.com bit.ly/asda"
        result = twtt.remove_urls(tweet).strip()
        answer = ''
        self.assertEqual(result, answer)