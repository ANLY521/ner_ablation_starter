# coding: utf-8

import argparse
from util import read_ner_sents
import re
import unicodedata

def base_features(tokens, idx):
        """
        from CRFTagger
        Extract basic features about this word including
             - Current Word
             - Is Capitalized ?
             - Has Punctuation ?
             - Has Number ?
             - Suffixes up to length 3
        Note that : we might include feature over previous word, next word ect.

        :return : a list which contains the features
        :rtype : list(str)

        """
        token = tokens[idx]

        feature_list = []

        if not token:
            return feature_list

        # Capitalization
        if token[0].isupper():
            feature_list.append("CAPITALIZATION")

        # Number
        if re.search(r"\d", token) is not None:
            feature_list.append("HAS_NUM")

        # Punctuation
        punc_cat = set(["Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"])
        if all(unicodedata.category(x) in punc_cat for x in token):
            feature_list.append("PUNCTUATION")

        # Suffix up to length 3
        if len(token) > 1:
            feature_list.append("SUF_" + token[-1:])
        if len(token) > 2:
            feature_list.append("SUF_" + token[-2:])
        if len(token) > 3:
            feature_list.append("SUF_" + token[-3:])

        feature_list.append("WORD_" + token)

        return feature_list

def all_in(tokens, idx):
    # TODO: add features
    feats = base_features(tokens, idx)
    return feats


def main(train_file, dev_file):
    # load the train data
    train_sents = read_ner_sents(train_file)

    dev_sents = read_ner_sents(dev_file)

    # TODO 1: Write two additional feature functions and complete the all_in function
    # refer to class lectures to get ideas of good features for NER

    # TODO 2: Train a new CRFTagger with each combination of feature functions (see README)
    # HINT: see CRFTagger's init kwarg 'feature_func', easier than the subclass used in the lab
    # A function can be treated as a variable in Python
    condition_to_func = {"base": base_features, "all_in": all_in}
    for cond, func in condition_to_func.items():
        print(f"Training tagger for condition {cond}")

        # TODO 3: Write each set of results to an output file
        # you will evaluate using wnuteval.py and write up your results in the README




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", type=str,
                        default="emerging_entities_17/wnut17train.conll",
                        help="wnut tsv file including annotations")
    parser.add_argument("--dev_file", type=str,
                        default="emerging_entities_17/emerging.dev.conll",)

    args = parser.parse_args()

    main(args.train_file, args.dev_file)
