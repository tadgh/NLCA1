import twtt
__author__ = 'tadgh'
import os

ROOT_DIR = "tweets/"
OUTPUT_DIR = "output/"
if __name__ == "__main__":
    tweet_filenames = os.listdir(ROOT_DIR)
    for filename in tweet_filenames:
        twtt.analyze_files(ROOT_DIR + filename, OUTPUT_DIR + filename + ".twt")




