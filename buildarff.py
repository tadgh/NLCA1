import argparse
import string
import features

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
        This is a score generator that yields one vector at a time. For each tweet in each file
        in self._files it will spit out a vector of length n+1, where n is the length of the feature
        list, and the +1 is the class name itself. 

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
        """
        Given a list of lines tweet_lines, calculate a per-feature score, return a score vector for one tweet. 
        """
        feature_scores = []
        for feature in feature_list:
            feature_scores.append(feature.get_score(tweet_lines))
        print feature_scores
        return feature_scores

class OutfileHandler(object):

    def __init__(self, outfile_name):
        self._file = open(outfile_name, "w")
            
        self._prologue_string = "@relation "
        self._attribute_prefix_string = "@attribute "
        self._data_tag = "@data"
        self._feature_data_type = "numeric"

    def write_file_prologue(self, feature_list, class_list):
        """
        Prepares the ARFF file, writing any necessary prologue data. 
        """
        self._file.write(self._prologue_string + "tweeters" + "\n\n")
        for feature in feature_list:
            self._file.write(self._attribute_prefix_string + feature.get_name() + "\t" + self._feature_data_type + "\n")
        self._file.write(self._attribute_prefix_string + "class" + "\t" + "{" + ','.join([u_class.get_name() for u_class in class_list]) + "}\n")

        self._file.write("\n" + self._data_tag + "\n")
                
    def write_vector(self, score_vector):
        """
        Given a list of scores, writes them to the file in proper format. 
        """
        self._file.write(", ".join(str(score) for score in score_vector) + "\n")



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
    """
    Generates the list of all features to be extracted. To add a new feature, subclass the Feature
    class, and implement get_line_score() to count the score for a single string. Also, override 
    get_score() if you need to change how the line scores are combined. By default they are summed. 
    """
    global feature_list
    f1 = features.FirstPersonFeature()
    f2 = features.SecondPersonFeature()
    f3 = features.ThirdPersonFeature()
    f4 = features.CoordinatingConjunctionsFeature()
    f5 = features.PastTenseFeature()
    f6 = features.FutureTenseFeature()
    f7 = features.CommaFeature()
    f8 = features.ColonFeature()
    f9 = features.DashFeature()
    f10 = features.ParenFeature()
    f11 = features.EllipsesFeature()
    f12 = features.CommonNounsFeature()
    f13 = features.ProperNounsFeature()
    f14 = features.AdverbsFeature()
    f15 = features.WHWordsFeature()
    f16 = features.ModernSlangFeature()
    f17 = features.AllCapsFeature()
    f18 = features.AverageSentenceLengthFeature()
    f19 = features.AverageTokenLengthFeature()
    f20 = features.SentenceCountFeature()
    
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
    out.write_file_prologue(feature_list, user_classes)
    for user_class in user_classes:
        print "Generating new Arff data!"
        for score_vector in user_class.generate_arff_data():
           out.write_vector(score_vector) 


if __name__=="__main__":
    main()
