# coding: utf-8

from nltk.chunk import tree2conlltags
from nltk import pos_tag, ne_chunk
import argparse
from util import read_ner_sents

def get_iob_ner(tokens):
    """
    :param tokens: list of string
    :return: ner tags, list of strings
    """
    ner_tags = []
    return ner_tags

def main(wnut_data, output_file):

    all_sents = read_ner_sents(wnut_data)

    with open(output_file, 'w') as pred_file:
        for sent in all_sents:
            sent_words = [line.split()[0] for line in sent]
            gold_tags = [line.split()[1] for line in sent]

            # TODO 1: complete get_iob_ner
            # the function will use the default named entity tagger in nltk, with the function ne_chunk
            # then it will convert the resulting tree structure into IOB tags on tokens
            as_conll = get_iob_ner(sent_words)

            # TODO 2: convert predicted tags from nltk's entity set to the tags in the WNUT set
            # conversion given in the README

            # TODO 3: write the token, gold standard tag, and predicted tag as tab-sep values
            # this file format can be evaluated by wnuteval.py

            # add an empty line after each sentence
            pred_file.write("\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--wnut_file", type=str,
                        default="emerging_entities_17/emerging.dev.conll",
                        help="wnut tsv file including annotations")
    parser.add_argument("--output_file", type=str, default="predictions.tsv",
                        help="file to write results")

    args = parser.parse_args()

    main(args.wnut_file, args.output_file)
