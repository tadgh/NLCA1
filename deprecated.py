__author__ = 'tadgh'

def old_split_into_tokens(sentence):
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
    # "sentence is", sentencegary
    for word in sentence:
        i = 0
        last_split = 0
        while i < len(word):
            if word[i] in punctuation_set:
                #checking for posessive clitic
                if i + 2 == len(word) and word[i] == "'" and word[i + 1] == "s":
                    print "Found posessive clitic!"
                    tokens.append(word[last_split:])
                    i += 2
                    last_split += 2
                elif i + 1 == len(word) and word[i] == "'" and word[i - 1] == "s":
                    print "Found posessive clitic!"
                    tokens.append(word[last_split:])
                    i += 1
                    last_split += 1
                else:
                    tokens.append(word[last_split: i])
                    last_split = i
                    j = 1
                    while i + j < len(word) and word[i + j] == word[i]:
                        j += 1
                    if i + j >= len(word):
                        tokens.append(word[last_split:])
                        last_split = len(word)
                    else:
                        tokens.append(word[last_split: i + j])
                        last_split = i + j
                    i += j
            else:
                i += 1
        tokens.append(word[last_split:])
    return [tok for tok in tokens if tok != '']



def split_into_sentences_old(tweet, abbreviations):
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
            sentences.append(separated_tweet[last_sentence_index: i + 1])
            last_sentence_index = i + 1
        elif separated_tweet[i].endswith(".") and separated_tweet[i].lower() not in abbreviations:
            sentences.append(separated_tweet[last_sentence_index: i + 1])
            last_sentence_index = i + 1
    if last_sentence_index < len(separated_tweet):
        sentences.append(separated_tweet[last_sentence_index:])

    return [sentence for sentence in sentences if sentence != '']