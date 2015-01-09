import argparse

__author__ = 'tadgh'

feature_list = []

class UserClass(object):
    """
    Holds information concerning the name of the class, and the appropriate member .twt files 
    that are needed to generate the arf. 
    """
    tweet_count = 0
        
    def __init__(self, name, file_list):
        self._name = name
        self._files = file_list

    def generate_arff_data(self):
        for infile in self._files:
            with open(infile, 'r') as file:
                line = file.readline()
                if line == "|\n":
                    while line != "":
                        tweet_lines = []
                        line = file.readline()
                        while line != "|\n":
                            tweet_lines.append(line)
                            line = file.readline()
                        self.analyze_tweet(tweet_lines)            

    def __str__(self):
        return self._name + " -- " + str(self._files)

    def analyze_tweet(self, tweet_lines):
        feature_scores = []
        for feature in feature_list:
            feature_scores.append(0)
            for line in tweet_lines:
                feature_scores[-1] += feature.get_score(line)
        print feature_scores



class Feature(object):
    def __init__(self, name):
        self._name = name

    def get_score(self, string):
        raise NotImplementedError("You need to implement this in a subclass!")

class FirstPersonFeature(Feature):

    def __init__(self):
        super(FirstPersonFeature, self).__init__("First Person")
        self._membership_set = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']

    def get_score(self, string):

        count = 0
        for token in string.split():
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count



class SecondPersonFeature(Feature):

    def __init__(self):
        super(SecondPersonFeature, self).__init__("Second Person")
        self._membership_set = ['you', 'your', 'yours', 'u', 'ur', 'urs']

    def get_score(self, string):

        count = 0
        for token in string.split():
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count



class ThirdPersonFeature(Feature):

    def __init__(self):
        super(ThirdPersonFeature, self).__init__("Third Person")
        self._membership_set = ['he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs']

    def get_score(self, string):

        count = 0
        for token in string.split():
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count


class CoordinatingConjunctionsFeature(Feature):

    def __init__(self):
        super(CoordinatingConjunctionsFeature, self).__init__("Coordinating Conjunctions")
        self._membership_set = ['CC']

    def get_score(self, string):
        count = 0
        for token in string.split():
            print "token is", token
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count


class PastTenseFeature(Feature):

    def __init__(self):
        super(PastTenseFeature, self).__init__("Past Tense")
        self._membership_set = ['VBD']

    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count

class FutureTenseFeature(Feature):

    def __init__(self):
        super(FutureTenseFeature, self).__init__("Future Tense")
        self._membership_set = ["'ll", "will", "gonna"]

    def get_score(self, string):
        count = 0
        split_string = string.split()
        for i in xrange(len(split_string)):
            if split_string[i].split('/')[0].lower() in self._membership_set:
                count += 1
            elif split_string[i].split("/")[0] == "going":
                if split_string[i + 1].split("/")[0] == "to":
                    if split_string[i + 2].split("/")[1] == "VB":
                        count += 1
        return count

class CommaFeature(Feature):

    def __init__(self):
        super(CommaFeature, self).__init__("Commas")
        self._membership_set = [',']

    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class ColonFeature(Feature):

    def __init__(self):
        super(ColonFeature, self).__init__("Colons and Semi-Colons")
        self._membership_set = [":", ";"]
    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class DashFeature(Feature):

    def __init__(self):
        super(DashFeature, self).__init__("Dashes")
        self._membership_set = ["-"]
    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class ParenFeature(Feature):

    def __init__(self):
        super(ParenFeature, self).__init__("Parentheses")
        self._membership_set = ["(", ")"]
    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class EllipsesFeature(Feature):

    def __init__(self):
        super(EllipsesFeature, self).__init__("Ellipses")
        

    def get_score(self, string):
        count = 0
        for token in string.split():
            if len(token) > 1 and all([letter == "." for letter in token]):
                count += 1
        return count


class CommonNounsFeature(Feature):

    def __init__(self):
        super(CommonNounsFeature, self).__init__("Common Nouns")
        self._membership_set = ["NN", "NNS"]
    
    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count



class ProperNounsFeature(Feature):

    def __init__(self):
        super(ProperNounsFeature, self).__init__("Proper Nouns")
        self._membership_set = ["NNP", "NNPS"]

    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count



class AdverbsFeature(Feature):
    
    def __init__(self):
        super(AdverbsFeature, self).__init__("Adverbs")
        self._membership_set = ["RB", "RBR", "RBS"]
    
    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count




class WHWordsFeature(Feature):

    def __init__(self):
        super(WHWordsFeature, self).__init__("'wh-words")
        self._membership_set = ["WDT", "WP", "WP$", "WRB"]

    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count



class ModernSlangFeature(Feature):

    def __init__(self):
        super(ModernSlangFeature, self).__init__("Modern Slang")
        self._membership_set = ["smh", "fwb", "lmfao", "lmao", "lms", "tbh", "rofl", "wtf", "bff", "wyd", "lylc", "brb", "atm", "imao", "sml", "btw", "bw", "imho", "fyi", "ppl", "sob", "ttyl", "imo", "ltr", "thx", "kk", "omg", "ttys", "afn", "bbs", "cya", "ez", "f2f", "gtr", "ic", "jk", "k", "ly", "ya", "nm", "np", "plz", "ru", "so", "tc", "tmi", "ym", "ur", "u", "sol"]
    
    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count


class AllCapsFeature(Feature):
    def __init__(self):
        super(AllCapsFeature, self).__init__("All Caps")

    def get_score(self, string):
        count = 0
        for token in string.split():
            if token.isupper():
                count += 1
        return count
class AverageTokenFeature(Feature):
    def get_score(self, string):
        return len(string)

    def __init__(self, name):
        super(AverageTokenFeature, self).__init__(name)
        


def extract_classes_from_list(class_list):
    """
    Takes a list of CLI args indicating twitter classes and their respective twt files. Returns a 
    list of UserClass objects for each unique twitter user class defined. 
    """
    classes = []
    for user_class in class_list:
        split_class = user_class.split(":")
        if len(split_class) == 2:
            class_name = split_class[0]
            class_members = [user for user in split_class[1].split("+")]
        elif len(split_class) == 1:
            class_members = [user for user in split_class[0].split("+")]
            class_name = "".join([filename.rstrip(".twt") for filename in class_members])

        twitter_class = UserClass(class_name, class_members)
        classes.append(twitter_class)

    for user in classes:
        print(user)

    return classes

def build_count_feature_set():
    global feature_list
    f1 = FirstPersonFeature()
    f2 = SecondPersonFeature()
    f3 = ThirdPersonFeature()
    f4 = CoordinatingConjunctionsFeature()
    f5 = PastTenseFeature()
    f6 = FutureTenseFeature()
    f7 = CommaFeature()
    f8 = ColonFeature()
    f9 = DashFeature()
    f10 = ParenFeature()
    f11 = EllipsesFeature()
    f12 = CommonNounsFeature()
    f13 = ProperNounsFeature()
    f14 = AdverbsFeature()
    f15 = WHWordsFeature()
    f16 = ModernSlangFeature()
    f17 = AllCapsFeature()
    feature_list = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17]


def main():
    parser = argparse.ArgumentParser(description="Build ARRF files from tokenized and tagged tweets")
    parser.add_argument("-n", metavar="NumberOfTweets", type=int, required=False, default=0)
    parser.add_argument("class_names", metavar="ClassNames", type=str, nargs='+')
    parser.add_argument("output_file", metavar="OutputFile", type=str, nargs=1)
    args = parser.parse_args()
    user_classes = extract_classes_from_list(args.class_names)
    build_count_feature_set() 
    for user_class in user_classes:
        user_class.generate_arff_data()
if __name__=="__main__":
    main()
