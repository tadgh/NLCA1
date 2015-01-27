"""
In order to add new features, subclass the feature class. 

1. Impleent get_line_score(). 
2. Override get_score().

only override get_score() if you need a different overall score calculator. By 
default, it sums up all the line scores. If you need an average or something, implement it in
get_score().

"""
import string

class Feature(object):
    def __init__(self, name):
        self._name = name

    def get_score(self, tweet):
        """
        Retrieves the score for the entire tweet. Override if you need to do something other than summation.
        """
        score = sum([self.get_line_score(line) for line in tweet])
        return score

    def get_line_score(self, string):
        """
        Retrieves the score for a single line of a tweet. 
        """
        raise NotImplementedError("You need to implement this in a subclass!")

    def get_name(self):
        """
        Return the name of the feature, ready to be written to the arff file. 
        """
        return self._name


class FirstPersonFeature(Feature):

    def __init__(self):
        super(FirstPersonFeature, self).__init__("firstperson")
        self._membership_set = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count



class SecondPersonFeature(Feature):

    def __init__(self):
        super(SecondPersonFeature, self).__init__("secondperson")
        self._membership_set = ['you', 'your', 'yours', 'u', 'ur', 'urs']

    def get_line_score(self, string):

        count = 0
        for token in string.split():
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count



class ThirdPersonFeature(Feature):

    def __init__(self):
        super(ThirdPersonFeature, self).__init__("thirdperson")
        self._membership_set = ['he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs']

    def get_line_score(self, string):

        count = 0
        for token in string.split():
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count


class CoordinatingConjunctionsFeature(Feature):

    def __init__(self):
        super(CoordinatingConjunctionsFeature, self).__init__("conjunctions")
        self._membership_set = ['CC']

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count


class PastTenseFeature(Feature):

    def __init__(self):
        super(PastTenseFeature, self).__init__("pasttense")
        self._membership_set = ['VBD', 'VBN']

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count

def token_content(token):
    return token.split('/')[0]

def token_type(token):
    return token.split('/')[1]

class FutureTenseFeature(Feature):

    def __init__(self):
        super(FutureTenseFeature, self).__init__("futuretense")
        self._membership_set = ["'ll", "will", "gonna"]

    def get_line_score(self, string):
        count = 0
        split_string = string.split()
        for i in xrange(len(split_string)):
            if split_string[i].split('/')[0].lower() in self._membership_set:
                count += 1
            elif split_string[i].split("/")[0].lower() == "going" and i + 2 < len(split_string):
                if split_string[i + 1].split("/")[0].lower() == "to":
                    if split_string[i + 2].split("/")[1] == "VB":
                        count += 1
        return count

class CommaFeature(Feature):

    def __init__(self):
        super(CommaFeature, self).__init__("commas")
        self._membership_set = [',']

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class ColonFeature(Feature):

    def __init__(self):
        super(ColonFeature, self).__init__("colonssemis")
        self._membership_set = [":", ";"]
    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class DashFeature(Feature):

    def __init__(self):
        super(DashFeature, self).__init__("dashes")
        self._membership_set = ["-"]
    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class ParenFeature(Feature):

    def __init__(self):
        super(ParenFeature, self).__init__("parentheses")
        self._membership_set = ["(", ")"]
    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class EllipsesFeature(Feature):

    def __init__(self):
        super(EllipsesFeature, self).__init__("ellipses")
        

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            content = token.split("/")[0]
            if len(content) > 1 and all([letter == "." for letter in content]):
                count += 1
        return count


class CommonNounsFeature(Feature):

    def __init__(self):
        super(CommonNounsFeature, self).__init__("commonnouns")
        self._membership_set = ["NN", "NNS"]
    
    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count



class ProperNounsFeature(Feature):

    def __init__(self):
        super(ProperNounsFeature, self).__init__("propernouns")
        self._membership_set = ["NNP", "NNPS"]

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count



class AdverbsFeature(Feature):
    
    def __init__(self):
        super(AdverbsFeature, self).__init__("averbs")
        self._membership_set = ["RB", "RBR", "RBS"]
    
    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count




class WHWordsFeature(Feature):

    def __init__(self):
        super(WHWordsFeature, self).__init__("wh-words")
        self._membership_set = ["WDT", "WP", "WP$", "WRB"]

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count



class ModernSlangFeature(Feature):

    def __init__(self):
        super(ModernSlangFeature, self).__init__("modernslang")
        self._membership_set = ["smh", "fwb", "lmfao", "lmao", "lms", "tbh", "rofl", "wtf", "bff", "wyd", "lylc", "brb", "atm", "imao", "sml", "btw", "bw", "imho", "fyi", "ppl", "sob", "ttyl", "imo", "ltr", "thx", "kk", "omg", "ttys", "afn", "bbs", "cya", "ez", "f2f", "gtr", "ic", "jk", "k", "ly", "ya", "nm", "np", "plz", "ru", "so", "tc", "tmi", "ym", "ur", "u", "sol"]
    
    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count


class AllCapsFeature(Feature):
    def __init__(self):
        super(AllCapsFeature, self).__init__("all-caps")

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            content = token.split("/")[0]
            if content.isupper() and len(content) > 1:
                count += 1
        return count

class AverageSentenceLengthFeature(Feature):
    def __init__(self):
        super (AverageSentenceLengthFeature, self).__init__("avg-sent-len")

    def get_score(self, tweet):
        line_count = len(tweet)
        token_count = 0
        for line in tweet:
            token_count += len(line.split())
        avg_tokens = float(token_count) / line_count

        return "{0:.3f}".format(avg_tokens)

class AverageTokenLengthFeature(Feature):
    def __init__(self):
        super (AverageTokenLengthFeature, self).__init__("avg-token-len")
        self._punctuation_set = tuple(string.punctuation)

    def get_score(self, tweet):
        token_count = 0
        total_token_length = 0
        for line in tweet:
            split_line = line.split()
            non_punc_tokens = [token.split("/")[0] for token in split_line if token.split("/")[0] not in self._punctuation_set]
            token_count += len(non_punc_tokens)
            total_token_length += sum([len(token.split("/")[0]) for token in non_punc_tokens])
        try:
            avg_token_length = float(total_token_length) / token_count
        except ZeroDivisionError:
            avg_token_length = 0
        return "{0:.3f}".format(avg_token_length)


            
class SentenceCountFeature(Feature):
    def __init__(self):
        super(SentenceCountFeature, self).__init__("sentencecount")
   
    def get_score(self, tweet):
        return len(tweet)


