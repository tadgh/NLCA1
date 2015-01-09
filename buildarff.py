import argparse

__author__ = 'tadgh'

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
        pass

    def __str__(self):
        return self._name + " -- " + str(self._files)

class Feature(object):
    def __init__(self, name):
        self._name = name

    def get_score(self, string):
        raise NotImplementedError("You need to implement this in a subclass!")

class FirstPersonFeature(Feature):

    def ___init__(self):
        super(FirstPersonFeature, self).__init__("First Person")
        self._membership_set = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']

    def get_score(self, string):

        count = 0
        for token in string:
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count



class SecondPersonFeature(Feature):

    def __init__(self):
        super(SecondPersonFeature, self).__init__("Second Person")
        self._membership_set = ['you', 'your', 'yours', 'u', 'ur', 'urs']

    def get_score(self, string):

        count = 0
        for token in string:
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count



class ThirdPersonFeature(Feature):

    def __init__(self):
        super(ThirdPersonFeature, self).__init__("Third Person")
        self._membership_set = ['he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs']

    def get_score(self, string):

        count = 0
        for token in string:
            if token.split('/')[0].lower() in self._membership_set:
                count += 1
        return count


class CoordinatingConjunctionsFeature(Feature):

    def __init__(self):
        super(CoordinatingConjunctionsFeature, self).__init__("Coordinating Conjunctions")
        self._membership_set = ['CC']

    def get_score(self, string):
        count = 0
        for token in string:
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count


class PastTenseFeature(Feature):

    def __init__(self):
        super(PastTenseFeature, self).__init__("Past Tense")
        self._membership_set = ['VBD']

    def get_score(self, string):
        count = 0
        for token in string:
            if token.split('/')[1] in self._membership_set:
                count += 1
        return count

class FutureTenseFeature(Feature):

    def __init__(self):
        super(FutureTenseFeature, self).__init__("Future Tense")
        self._membership_set = ["'ll", "will", "gonna"]

    def get_score(self, string):
        count = 0
        for i in xrange(string):
            if string[i].split('/')[0].lower() in self._membership_set:
                count += 1
            elif string[i].split("/")[0] == "going":
                if string[i + 1].split("/")[0] == "to":
                    if string[i + 2].split("/")[1] == "VB":
                        count += 1
        return count

class CommaFeature(Feature):

    def __init__(self):
        super(CommaFeature, self).__init__("Commas")
        self._membership_set = [',']

    def get_score(self, string):
        count = 0
        for token in string:
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class ColonFeature(Feature):

    def __init__(self):
        super(ColonFeature, self).__init__("Colons and Semi-Colons")
        self._membership_set = [":", ";"]
    def get_score(self, string):
        count = 0
        for token in string:
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class DashFeature(Feature):

    def __init__(self):
        super(DashFeature, self).__init__("Dashes")
        self._membership_set = ["-"]
    def get_score(self, string):
        count = 0
        for token in string:
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class ParenFeature(Feature):

    def __init__(self):
        super(ParenFeature, self).__init__("Parentheses")
        self._membership_set = ["(", ")"]
    def get_score(self, string):
        count = 0
        for token in string:
            if token.split('/')[0] in self._membership_set:
                count += 1
        return count

class EllipsesFeature(Feature):

    def __init__(self):
        super(EllipsesFeature, self).__init__("Ellipses")

    def get_score(self, string):
        count = 0
        for token in string:
            if len(token) > 1 and all([letter == "." for letter in token]):
                count += 1
        return count


class CommonNounsFeature(Feature):

    def __init__(self):
        super(CommonNounsFeature, self).__init__("Common Nouns")

    def get_score(self, string):
        pass

class ProperNounsFeature(Feature):

    def __init__(self):
        super(ProperNounsFeature, self).__init__("Proper Nouns")

    def get_score(self, string):
        pass


class AdverbsFeature(Feature):
    def __init__(self):
        super(AdverbsFeature, self).__init__("Adverbs")

    def get_score(self, string):
        pass

class WHWordsFeature(Feature):

    def __init__(self):
        super(WHWordsFeature, self).__init__("'wh-words")

    def get_score(self, string):
        pass

class ModernSlangFeature(Feature):

    def __init__(self):
        super(ModernSlangFeature, self).__init__("

    def get_score(self, string):
        pass


class AllCapsFeature(Feature):
    def __init__(self):
        super(AllCapsFeature, self).__init

    def get_score(self, string):
        pass

class AverageTokenFeature(Feature):
    def get_score(self, string):
        return super(AverageTokenFeature, self).get_score(string)

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

def build_count_feature_set():
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

def main():
    parser = argparse.ArgumentParser(description="Build ARRF files from tokenized and tagged tweets")
    parser.add_argument("-n", metavar="NumberOfTweets", type=int, required=False, default=0)
    parser.add_argument("class_names", metavar="ClassNames", type=str, nargs='+')
    parser.add_argument("output_file", metavar="OutputFile", type=str, nargs=1)
    args = parser.parse_args()
    extract_classes_from_list(args.class_names)
    
if __name__=="__main__":
    main()
