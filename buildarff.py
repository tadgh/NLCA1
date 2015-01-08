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

def main():
    parser = argparse.ArgumentParser(description="Build ARRF files from tokenized and tagged tweets")
    parser.add_argument("-n", metavar="NumberOfTweets", type=int, required=False, default=0)
    parser.add_argument("class_names", metavar="ClassNames", type=str, nargs='+')
    parser.add_argument("output_file", metavar="OutputFile", type=str, nargs=1)
    args = parser.parse_args()
    extract_classes_from_list(args.class_names)
    
if __name__=="__main__":
    main()
