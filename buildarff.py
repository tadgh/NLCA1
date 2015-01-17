import argparse
import string
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
    
    def get_name(self):
        return self._name

    def generate_arff_data(self):
        """
        This is a generator that yields one vector at a time. 

        """
        for infile in self._files:
            with open(infile, "r") as file:
                print "opening new file"
                tweet_lines = []
                count = 0
                for line in file:
                    if line == "|\n":
                        if len(tweet_lines) > 0:
                            count += 1                            
                            scores = self.analyze_tweet(tweet_lines)
                            scores.append(self._name)
                            yield scores
                        tweet_lines = []
                    else:
                        tweet_lines.append(line)

    def __str__(self):
        return self._name + " -- " + str(self._files)
        
    def analyze_tweet(self, tweet_lines):
        feature_scores = []
        for feature in feature_list:
            feature_scores.append(feature.get_score(tweet_lines))
        print feature_scores
        return feature_scores

class OutfileHandler(object):
    prologue_string = "@RELATION "
    attribute_prefix_string = "@ATTRIBUTE "
    data_tag = "@DATA"
    feature_data_type = "NUMERIC"

    def __init__(self, outfile_name):
        self._file = open(outfile_name, "w")
            
        self._prologue_string = "@RELATION "
        self._attribute_prefix_string = "@ATTRIBUTE "
        self._data_tag = "@DATA"
        self._feature_data_type = "NUMERIC"

    def write_file_prologue(self, feature_list, class_list):
        self._file.write(self._prologue_string + "tweet_info" + "\n\n")
        for feature in feature_list:
            self._file.write(self._attribute_prefix_string + feature.get_name() + "\t" + self._feature_data_type + "\n")
        self._file.write(self.attribute_prefix_string + "class" + "\t" + "{" + ','.join([u_class.get_name() for u_class in class_list]) + "}\n")

        self._file.write("\n" + self._data_tag + "\n")
                
    def write_vector(self, score_vector):
        #for i in xrange(len(score_vector)):
        self._file.write(", ".join(str(score) for score in score_vector) + "\n")
            #self._file.write(str(score_vector[i]))
            #self._file.write("\n" if i + 1 == len(score_vector) else " ,")


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
        raise NotImplementedError("You need to implement this in a subclass!")

    def get_name(self):
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
        super(ThirdPersonFeature, self).__init__("Third Person")
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
            if len(token) > 1 and all([letter == "." for letter in token]):
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
        super(WHWordsFeature, self).__init__("'wh-words")
        self._membership_set = ["WDT", "WP", "WP$", "WRB"]

    def get_line_score(self, string):
        count = 0
        for token in string.split():
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count



class ModernSlangFeature(Feature):

    def __init__(self):
        super(ModernSlangFeature, self).__init__("Modern Slang")
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
            if token.isupper():
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
            token_count += len(split_line)
            untagged_tokens = [token.split("/")[0] for token in split_line if token.split("/")[0] not in self._punctuation_set]
            #for punc in self._punctuation_set:
            #    if punc in untagged_tokens:
            #        untagged_tokens.remove(punc)
            total_token_length += sum([len(token.split("/")[0]) for token in split_line ])
        avg_token_length = float(total_token_length) / token_count
        
        
        return "{0:.3f}".format(avg_token_length)


            
class SentenceCountFeature(Feature):
    def __init__(self):
        super(SentenceCountFeature, self).__init__("sentencecount")
   
    def get_score(self, tweet):
        return len(tweet)



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
    f18 = AverageSentenceLengthFeature()
    f19 = AverageTokenLengthFeature()
    f20 = SentenceCountFeature()

    feature_list = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17, f18, f19, f20]


def main():
    parser = argparse.ArgumentParser(description="Build ARRF files from tokenized and tagged tweets")
    parser.add_argument("-n", metavar="NumberOfTweets", type=int, required=False, default=0)
    parser.add_argument("class_names", metavar="ClassNames", type=str, nargs='+')
    parser.add_argument("output_file", metavar="OutputFile", type=str, nargs=1)
    args = parser.parse_args()
    user_classes = extract_classes_from_list(args.class_names)
    build_count_feature_set()
    out = OutfileHandler(args.output_file[0])
    for user_class in user_classes:
        print "Generating new Arff data!"
        out.write_file_prologue(feature_list, user_classes)
        for score_vector in user_class.generate_arff_data():
           out.write_vector(score_vector) 


if __name__=="__main__":
    main()
