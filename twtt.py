import string
from constants import sentence_split_regex, url_regex, secondary_url_regex, token_split_regex

__author__ = 'tadgh'
import HTMLParser
import argparse
import re
import htmlentitydefs

import tagger.NLPlib as nlp

# ##
# Tweet Preprocessor. Strips all HTML tags, replaces HTML codes with ascii equivalents, removes all URLS, Removes
# Hashtags and Mention symbols, renders each sentence in a tweet on its own line. Tweets are delimited by the Pipe |
###


def preprocess_tweet(tweet, parser, abbreviations, tagger):
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
<<<<<<< HEAD
        tweet = remove_urls(tweet, url_regex)
=======
        tweet = remove_urls(tweet)
>>>>>>> FETCH_HEAD
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
def remove_urls(tweet):
    """
    Removes URLs from any string.

    :param tweet: A tweet with URLs(possibly) in it, a string.
    :return: The original tweet parameter with all URLs removed.
    """
    tweet = re.sub(url_regex, "", tweet)
    tweet = re.sub(secondary_url_regex, "", tweet)
    return tweet

<<<<<<< HEAD
=======
def split_into_sentences(tweet, abbreviations):

    #First we save our abbreviations so we don't wipe them out. This repalcement token is arbitrary, but it makes sure
    #I don't have to try to rebuild strings after accidentally oversplitting on periods.
    for abbr in abbreviations:
        tweet = re.sub(" " + re.escape(abbr), " " +abbr.upper().rstrip(".") + "~|~|", tweet, flags=re.IGNORECASE)
>>>>>>> FETCH_HEAD

    #potential_sentences = re.split(r"(\.\.+\s?)(?=[A-Z])|([?!]+)|(\.\s)|(\.$)", tweet)
    potential_sentences = sentence_split_regex.split(tweet)
    #cleaning out unmatched groups
    potential_sentences = [sentence.strip() for sentence in potential_sentences if sentence]

    #recombining the sentence with its punctuation for ease of transport.
    repunctuated_sentences = []
    i = 0
    while i < len(potential_sentences) - 1:
        repunctuated_sentences.append(potential_sentences[i] + potential_sentences[i + 1])
        i += 2

    #Grabbing the final sentence if it wasn't terminated by punctuation.
    if i < len(potential_sentences):
        repunctuated_sentences.append(potential_sentences[-1])

    #Re-adding abbreviation periods.
    i = 0
    while i < len(repunctuated_sentences):
        repunctuated_sentences[i] = re.sub(r'~\|~\|', ".", repunctuated_sentences[i], flags=re.IGNORECASE)
        i += 1

    return [s for s in repunctuated_sentences if s]


<<<<<<< HEAD
    separated_tweet = tweet.split()
    sentences = []
    last_sentence_index = 0
    #Iterate through the entire tweet separated on spaces.
    for i in xrange(len(separated_tweet)):
        #! and ? are definitely terminating punctuation
        if separated_tweet[i].endswith(("!", "?")):
            sentences.append(separated_tweet[last_sentence_index : i+1])
            last_sentence_index = i+1

        #otherwise a period at the end of a sentence is terminating if it isnt an abbreviation.
        elif separated_tweet[i].endswith(".") and separated_tweet[i].lower() not in abbreviations:
            sentences.append(separated_tweet[last_sentence_index : i+1])
            last_sentence_index = i+1

        #Now check for any periods. If there are multiples get the rightost.
        #Is the character following that period a capital letter? 
        elif "." in separated_tweet[i]:
            period_index = separated_tweet[i].rfind(".")
            if separated_tweet[i][period_index + 1].isupper():
                sentences.append(separated_tweet[last_sentence_index : i+1])
                last_sentence_index = i+1

    if last_sentence_index < len(separated_tweet):
        sentences.append(separated_tweet[last_sentence_index:])

    #print "sentences are: ", str(sentences)
    return sentences
=======
>>>>>>> FETCH_HEAD

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
    tokens = token_split_regex.split(sentence)
    return [token for token in tokens if token.strip()]

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

            eng_abbrs = [line.lower().strip() for line in abbr1.readlines()] + [line.lower().strip() for line in abbr2.readlines()]
    return eng_abbrs


def analyze_files(input_file, output_file):
    """

    :param input_file: the input filename to analyze
    :param output_file: the output .twt file to write results to
    :return: None
    """

    in_file = open(input_file, "r")
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
    #url_regex2 = re.compile(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?', re.IGNORECASE)
    #url_regex3 = re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-]*)?\??(?:[\-\+=&;%@\.\w]*)#?(?:[\.\!\/\\\w]*))?)', re.IGNORECASE)
    #TODO regex sourced from https://gist.github.com/uogbuji/705383


    count = 0
    for tweet in in_file:
        count += 1
        tweet_sentences_processed = preprocess_tweet(tweet, parser, abbreviations, tagger)
        #print count, " --- ", tweet_sentences_processed
        out_file.write_tweet(tweet_sentences_processed)
    print count, " --- ", in_file
    out_file.close()


def main():
    #Generic Argument arsing setup to handle CLI arguments.
    argparser = argparse.ArgumentParser(description="Pre-process a tweet file.")
    argparser.add_argument('input_file', metavar="infile", type=str)
    argparser.add_argument('output_file', metavar="outfile", type=str)
    args = argparser.parse_args()


    #run analysis on the appropriate filenames.
    analyze_files(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
