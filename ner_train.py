# coding: utf-8

import argparse
from util import read_ner_sents
from nltk.tag.crf import CRFTagger


#TODO create subclass of CRFTagger


def main(train_file, dev_file):
    # load the train data
    train_sents = read_ner_sents(train_file)

    train_data = []
    for example in train_sents:
        if example:
            train_data.append([token.split('\t') for token in example])

    print("training")
    # TODO: instantiate your class and train


    dev_sents = read_ner_sents(dev_file)
    print("writing output")

    with open("mytagger_output.tsv", 'w') as pred_file:
        # TODO: write your outputs
        for sent in dev_sents:
            # TODO: predict, then write your outputs so you can evaluate with wnuteval.py
            pass




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", type=str,
                        default="../emerging_entities_17/wnut17train.conll",
                        help="wnut tsv file including annotations")
    parser.add_argument("--dev_file", type=str,
                        default="../emerging_entities_17/emerging.dev.conll",)

    args = parser.parse_args()

    main(args.train_file, args.dev_file)
