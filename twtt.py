import string

__author__ = 'tadgh'
import HTMLParser
import argparse
import re
import htmlentitydefs

import tagger.NLPlib as nlp

###
# Tweet Preprocessor. Strips all HTML tags, replaces HTML codes with ascii equivalents, removes all URLS, Removes
# Hashtags and Mention symbols, renders each sentence in a tweet on its own line. Tweets are delimited by the Pipe |
###


def preprocess_tweet(tweet, parser, abbreviations, url_regex, tagger):
    """
    Takes a single tweet string, and returns a list of lists, each outer list is a sentence in the tweet. Each inner
    list is a list of the tokens in that tweet, with all unnecessary information stripped.

    Unnecessary information is:
        1) HTML Tags
        2) URLS
        3) # and @ symbol when they are prepended to a word.
        4)Any HTML Codes replaced with Ascii Equivalents.

    :param tweet: str: The tweet completely unprocessed.
    :param parser: A TweetHTMLParser object, any HTMLParser will do.
    :param abbreviations: A list of known abbreviations where a period does not break the sentence.
    :param url_regex: The regular expression used to capture all URLS.
    :return: List of List of Str, where each inner item is a token(untagged), and each outer item is a sentence.
    """
    tokens = []
    if tweet is not None:
        tweet = remove_html_tags(tweet, parser)
        #tweet = remove_urls(tweet, url_regex)
        tweet = new_url_removal(tweet)
        sentences = split_into_sentences(tweet, abbreviations)
        token_lists = split_all_sentences_into_tokens(sentences)
        tagged_tokens = []
        for token_list in token_lists:
            tags = tagger.tag(token_list)
            tag_tuples = zip(token_list, tags)
            tagged_tokens.append(["/".join(elem) for elem in tag_tuples])
        #nifty return " ".join([tok for sublist in tokens for tok in sublist])
    return tagged_tokens

def remove_html_tags(tweet, parser):
    """
    Removes HTML tags from any string.

    :param tweet: A string representing a tweet, potentially with HTML tags in it.
    :param parser: The TweetHTMLParser object responsible for actual parsing
    :return: A string representing a tweet, with all HTML tags removed.
    """

    parser.clear()
    parser.feed(tweet)
    return parser.data

#TODO remove this. It also removes things like "Hello.....whatever"
def remove_urls(tweet, url_regex):
    """
    Removes URLs from any string.

    :param tweet: A tweet with URLs(possibly) in it, a string.
    :param url_regex: A regular expression attempting to capture all possible URLs.
    :return: The original tweet parameter with all URLs removed.
    """
    tweet = re.sub(url_regex, "", tweet)

    return tweet

def new_url_removal(tweet):
    parts = tweet.split()
    return " ".join([word for word in parts if not word.lower().startswith(("http", "www"))])


def split_into_sentences(tweet, abbreviations):
    """
    Split a tweet into sentences using end-punctuation and a small set of heuristics.

    :param tweet: A string representing a tweet.
    :param abbreviations: A list of abbreviations that sentences should not split on.
    :return: A list of list of strings, each of which represents a sentence.
    """

    separated_tweet = tweet.split()
    sentences = []
    last_sentence_index = 0
    for i in range(len(separated_tweet)):
        if separated_tweet[i].endswith(("!", "?")):
            sentences.append(separated_tweet[last_sentence_index: i+1])
            last_sentence_index = i+1
        elif separated_tweet[i].endswith(".") and separated_tweet[i].lower() not in abbreviations:
            sentences.append(separated_tweet[last_sentence_index: i+1])
            last_sentence_index = i+1
    if last_sentence_index < len(separated_tweet):
        sentences.append(separated_tweet[last_sentence_index:])

    #print "sentences are: ", str(sentences)
    return sentences

def split_all_sentences_into_tokens(sentences):
    """
    Take all sentences, and properly tokenize every internal word in all sentences.

    :param sentences: a list of sentences. Each sentence is a list of strings indicating whitespace-delimited words.
    :return: List of list of tokens(strings) that have been properly split.
    """

    all_tokens = []
    for sentence in sentences:
        tokens = split_into_tokens(sentence)
        all_tokens.append(tokens)
    #print "all found tokens: ", all_tokens
    return all_tokens

def split_into_tokens(sentence):
    """
    Take a sentence(list of words) and return a list of tokens determined by the assignment spec.
        1)punctuation is its own token.
        2)multiple sequential punctuation is a single token
        3) clitics are weird. Not sure exactly what to do.
        4)also, split end apostrophe.
    :param sentence:
    :return:
    """

    punctuation_set = tuple(string.punctuation)
    tokens = []
    # "sentence is", sentence
    for word in sentence:
        i = 0
        last_split = 0
        while i < len(word):
            if word[i] in punctuation_set:
                tokens.append(word[last_split: i])
                last_split = i
                j = 1
                while i + j < len(word) and word[i+j] == word[i]:
                    j += 1
                if i + j >= len(word):
                    tokens.append(word[last_split:])
                    last_split = len(word)
                else:
                    tokens.append(word[last_split: i + j])
                    last_split = i+j
                i += j
            else:
                i += 1
        tokens.append(word[last_split:])
    return [tok for tok in tokens if tok != '']

class OutfileHandler(object):
    def __init__(self, filename):
        self.outfile = open(filename, "w")

    def write_tweet(self, tweet):
        self.outfile.write("|\n")
        for line in tweet:
            #Since the line is in fact a list of all the tokens, we must join it beore writing.
            self.outfile.write(" ".join(line) + "\n")

    def close(self):
        self.outfile.write("|\n")
        self.outfile.close()

class TweetHTMLParser(HTMLParser.HTMLParser):
    """
    Class to handle HTML parsing.
    Responsibility is to ignore anything that is a tag start or end, and keep only the actual data.
    """
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.data = ""

    def handle_starttag(self, tag, attrs):
        pass
        #print "Start Tag is:", tag

    def handle_endtag(self, tag):
        pass
        #print "End Tag is:", tag

    def handle_data(self, data):
        #print "Regular Data is:", data
        self.data += " ".join([word[1:] if word.startswith(("@", "#")) else word for word in data.split()]) + " "
        #print "String so far:", self.data

    def handle_entityref(self, name):
        #print "entref is", name
        data = unichr(htmlentitydefs.name2codepoint[name])
        self.data += data + " "

    def clear(self):
        self.data = ""

def init_abbreviations():
    """
    None -> List of strings

    Concatenates the two known abbreviation files into a single list which we can later scour for known abbreviations.
    :return: List of known abbreviations
    """
    eng_abbrs = []
    with open("abbrev.english", "r") as abbr1:
        with open("pn_abbrev.english", "r") as abbr2:
            eng_abbrs.append([line.lower().strip() for line in abbr1.readlines() + abbr2.readlines()])
    return eng_abbrs


def analyze_files(input_file, output_file):
    """

    :param input_file: the input filename to analyze
    :param output_file: the output .twt file to write results to
    :return: None
    """

    in_file = open(input_file, "r" )
    out_file = OutfileHandler(output_file)
    #Generating the Parser which we will use to strip all HTML tags.
    parser = TweetHTMLParser()

    #Prepping the NLP tagger.
    tagger = nlp.NLPlib()

    #TODO find out if I can use more.
    #Prepare the list of known abbreviations
    abbreviations = init_abbreviations()

    #TODO potentially remove my regex.
    ###Prepare the URL regex
    url_regex = re.compile(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?', re.IGNORECASE)

    for tweet in in_file:
        tweet_sentences_processed = preprocess_tweet(tweet, parser, abbreviations, url_regex, tagger)
        out_file.write_tweet(tweet_sentences_processed)
    out_file.close()

def main():
    #Generic Argument arsing setup to handle CLI arguments.
    argparser = argparse.ArgumentParser(description="Pre-process a tweet file.")
    argparser.add_argument('input_file', metavar="infile", type=str)
    argparser.add_argument('output_file', metavar="outfile", type=str)
    args = argparser.parse_args()


    #run analysis on the appropriate filenames.
    analyze_files(args.input_file, args.output_file)


if __name__=="__main__":
    main()
