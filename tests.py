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

    
    def test_conjunctions_feature(self):
        tweet = ["here/ is/ my/ tweet/ and/CC I/ think/ it/ is/ ok/ ,/ but/CC .../C",
                 "I/ think/ i/ could/ improve/ it/ with/CC" ,
                 "more/ coordinating/ conjunctions/ and/CC things/ like/ that/"]
        result = self.f4.get_score(tweet)
        answer = 4
        self.assertEqual(result, answer)

    def test_pasttense_feature(self):
        tweet = ["here/ is/ my/ tweet/VBN and/CC I/ think/ it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/ improve/ it/ with/CC" ,
                 "more/ coordinating/ conjunctions/ and/CC things/VBN like/VBR that/"]
        result = self.f5.get_score(tweet)
        answer = 4
        self.assertEqual(result, answer)

    def test_future_tense_feature(self):
        tweet = ["here/ we/ 'll/whateva tweet/VBN ,/ and/CC I/ think/ it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD going/ to/ imrpove/VB  ,,,/ with/CC",
                 "more/ coordinating/ ,/ conjunctions/ will/CC help/VBN like/VBR that/"]
        result = self.f6.get_score(tweet)
        answer = 3
        self.assertEqual(result, answer)

    def test_comma_feature(self):
        tweet = ["here/ is/ my/ tweet/VBN and/CC I/ think/ it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/ improve/ it/ ,,,/ with/CC" ,
                 "more/ coordinating/ ,/ ,/ conjunctions/ ,/ and/CC things/VBN like/VBR that/"]
        result = self.f7.get_score(tweet)
        answer = 4
        self.assertEqual(result, answer)

    def test_colon_feature(self):
        tweet = ["here/ is/ my/ tweet/VBN and/CC :/: I/ think/ it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/ ;/: improve/ it/ with/CC" ,
                 "more/ :/: ;/: coordinating/ conjunctions/ and/CC things/VBN like/VBR that/"]
        result = self.f8.get_score(tweet)
        answer = 4
        self.assertEqual(result, answer)


    def test_dash_feature(self):
        tweet = ["here/ is/ my/ -/- tweet/VBN and/CC I/ think/ it/ is/  -/- ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/ improve/ it/ with/CC" ,
                 "more/ coordinating/ -/- conjunctions/ and/CC things/VBN -/- like/VBR that/"]
        result = self.f9.get_score(tweet)
        answer = 4
        self.assertEqual(result, answer)

    def test_paren_feature(self):
        tweet = ["here/ is/ my/ (/( tweet/VBN and/CC I/ think/ it/ )/(is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/ (/( improve/ it/ with/CC" ,
                 "more/ coordinating/ conjunctions/ and/CC things/VBN (/) like/VBR that/"]
        result = self.f10.get_score(tweet)
        answer = 4
        self.assertEqual(result, answer)


    def test_ellipses_feature(self):
        tweet = ["here/ is/ my/ ../ tweet/VBN .../ and/CC I/ think/ it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/  ......../ improve/ it/ with/CC" ,
                 "more/ coordinating/ ./. conjunctions/ ........../ and/CC things/VBN like/VBR that/"]
        result = self.f11.get_score(tweet)
        answer = 5
        self.assertEqual(result, answer)

    def test_common_nouns_feature(self):
        tweet = ["here/NN is/ my/ tweet/VBN and/CC I/ think/ it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/N improve/ it/ with/CC" ,
                 "more/NN coordinating/ conjunctions/NNS and/CC things/NNS like/VBR that/"]
        result = self.f12.get_score(tweet)
        answer = 4
        self.assertEqual(result, answer)

    def test_proper_nouns_feature(self):
        tweet = ["Gary/NNP is/ my/ tweet/VBN and/CC I/ think/ it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/NNPS improve/ it/ with/CC" ,
                 "more/ coordinating/ conjunctions/ and/NNP things/VBN like/VBR that/"]
        result = self.f13.get_score(tweet)
        answer = 3
        self.assertEqual(result, answer)

    def test_adverbs_feature(self):
        tweet = ["here/ is/ my/ tweet/RBS and/CC I/ think/RBRS it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD could/ improve/RB it/ with/CC" ,
                 "more/ coordinating/ conjunctions/RBR and/CC things/VBN like/VBR that/"]
        result = self.f14.get_score(tweet)
        answer = 3
        self.assertEqual(result, answer)


    def test_wh_words_feature(self):
        tweet = ["here/ is/ my/WP tweet/VBN and/CC I/ think/ it/ is/ ok/ ,/ but/CC .../VBN",
                 "I/ think/ i/VBD co/WP$   uld/ improve/ it/ with/CC" ,
                 "more/ coordinating/ conjunctions/ and/WDT things/VBN like/WRB that/"]
        result = self.f15.get_score(tweet)
        answer = 4
        self.assertEqual(result, answer)

    def test_modern_slang_feature(self):
        tweet = ["smh/ at dis sob/ ./ lmao mah fwb is ez imo, so ur sol"]
        result = self.f16.get_score(tweet)
        answer = 8
        self.assertEqual(result, answer)

    def test_ALL_CAPS_feature(self):
        tweet = ["HEY/ BRETT ,/ I/ WROTE/ YOU/ A/ SONG/"]
        result = self.f17.get_score(tweet)
        answer = 5
        self.assertEqual(result, answer)

    def test_average_sentence_length_feature(self):
        tweet = ["Sellmecandy09/NN by/IN God/NNP 's/POS grace/NN ,/, we/PRP 'll/MD have/VBP both/DT"]
        result = self.f18.get_score(tweet)
        answer = 10
        #floating the answer as i return it as a string.
        self.assertEqual(float(result), answer)

    #38 char

    def test_average_sentence_length_with_multiple_sentencesfeature(self):
        tweet = ["Sellmecandy09/NN by/IN God/NNP 's/POS grace/NN ,/, we/PRP 'll/MD have/VBP both/DT",
                 "Sellmecandy09/NN by/IN God/NNP 's/POS grace/NN"]
        result = self.f18.get_score(tweet)
        answer = 7.5
        #floating the answer as i return it as a string.
        self.assertEqual(float(result), answer)

    def test_average_token_length_feature(self):
        tweet = ["Sellmecandy09/NN by/IN God/NNP 's/POS grace/NN ,/, we/PRP 'll/MD have/VBP both/DT"]
        result = self.f19.get_score(tweet)
        answer = 4.222
        #floating the answer as i return it as a string.
        self.assertEqual(float(result), answer)

    def test_average_token_length_multiline_feature(self):
        tweet = ["Sellmecandy09/NN by/IN God/NNP 's/POS grace/NN ,/, we/PRP 'll/MD have/VBP both/DT",
                 "Sellmecandy09/NN by/IN God/NNP ,/, ,/,"]
        result = self.f19.get_score(tweet)
        answer = 4.667
        #floating the answer as i return it as a string.
        self.assertEqual(float(result), answer)

    def test_sentence_count_feature(self):
        tweet = ["1", "2", "3"]
        result = self.f20.get_score(tweet)
        answer = 3
        self.assertEqual(result, answer)








