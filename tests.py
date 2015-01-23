import unittest
import twtt
import features

class TWTTTests(unittest.TestCase):
    def setUp(self):
        self.abbrevs = twtt.init_abbreviations()

    def test_posessive_clitic_is_split(self):
        tweet_sentence = "No major differences between' Tea can't won't we'll help don't Party agenda and GOP candidates' policies"
        result = twtt.split_into_tokens(tweet_sentence)
        correct =['No', 'major', 'differences',
                  'between', "'", 'Tea', 'ca', "n't",
                  'wo', "n't", 'we', "'ll", 'help',
                  'do', "n't", 'Party', 'agenda',
                  'and', 'GOP', 'candidates', "'",
                  'policies']

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

        


class FeatureTests(unittest.TestCase):
    def setUp(self):
        self.f1 = features.FirstPersonFeature()
        self.f2 = features.SecondPersonFeature()
        self.f3 = features.ThirdPersonFeature()
        self.f4 = features.CoordinatingConjunctionsFeature()
        self.f5 = features.PastTenseFeature()
        self.f6 = features.FutureTenseFeature()
        self.f7 = features.CommaFeature()
        self.f8 = features.ColonFeature()
        self.f9 = features.DashFeature()
        self.f10 = features.ParenFeature()
        self.f11 = features.EllipsesFeature()
        self.f12 = features.CommonNounsFeature()
        self.f13 = features.ProperNounsFeature()
        self.f14 = features.AdverbsFeature()
        self.f15 = features.WHWordsFeature()
        self.f16 = features.ModernSlangFeature()
        self.f17 = features.AllCapsFeature()
        self.f18 = features.AverageSentenceLengthFeature()
        self.f19 = features.AverageTokenLengthFeature()
        self.f20 = features.SentenceCountFeature()

    def test_first_person_features(self):
        tweet = ["This is my first line, I like it a lot",
                 "wow, our lucky day. Another line for our collection",
                 "We enjoy OUR lines. Mine."]
        result = self.f1.get_score(tweet)
        answer = 6
        self.assertEqual(result, answer)

    def test_second_person_feature(self):   
        tweet = ["This is your/NN first line, you like it a lot u do",
                 "wow, your lucky day. Another line for yours/ collection",
                 "urs enjoy ur lines. Mine."]
        result = self.f2.get_score(tweet)
        answer = 7
        self.assertEqual(result, answer)

    def test_third_person_feature(self):
        tweet = ["His friend is her friend. Their friends are also his and hers/NN .",
                 "its so tired it can't even stand.",
                 "they want to stop but they wont let them/NN ."]
        result = self.f3.get_score(tweet)
        answer = 10
        self.assertEqual(result, answer)


























