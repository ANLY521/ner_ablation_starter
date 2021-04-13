# coding: utf-8

from nltk.chunk import tree2conlltags
from nltk import pos_tag, ne_chunk
import argparse

# borrowed from wnuteval.py
# splits data that is separated with an extra newline
def read_ner_sents(ner_file):
    """
    Args:
        lines (Iterable[str]): the lines

    Yields:
        List[str]: sentences as list
    """

    # open data and read sentences out
    with open(ner_file, 'r') as od:
        orig_lines = od.readlines()

    sents = []
    sent = []
    stripped_lines = (line.strip() for line in orig_lines)
    for line in stripped_lines:
        if line == '':
            sents.append(sent)
            sent = []
        else:
            sent.append(line)
    sents.append(sent)
    return sents

def get_iob_ner(tokens):
    """
    :param tokens: list of string
    :return: ner tags, list of strings
    """
    # named entity chunking happens off POS tags
    sent_with_pos = pos_tag(tokens)
    # run the default named entity recognizer
    nes = ne_chunk(sent_with_pos)
    # convert to conll format
    as_iob = tree2conlltags(nes)
    return [ner for token,pos,ner in as_iob]

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

            for i, tag_prediction in enumerate(as_conll):
                original_word = sent_words[i]
                if "-" in tag_prediction:
                    iob, entity = tag_prediction.split("-")
                    if entity not in ["PERSON", "ORGANIZATION",
                                      "GPE", "FACILITY", "LOCATION"]:
                        tag_prediction = "O"
                    else:
                        if entity == "ORGANIZATION":
                            entity = "corporation"
                        if entity in ["FACILITY", "GPE"]:
                            entity = "location"
                        tag_prediction = f"{iob}-{entity.lower()}"
                line_as_str = f"{original_word}\t{gold_tags[i]}\t{tag_prediction}\n"
                pred_file.write(line_as_str)

            # add an empty line after each sentence
            pred_file.write("\n")

        expected_output= """    ### ENTITY F1-SCORES ###
                processed
                15733
                tokens
                with 836 phrases;
                found: 911
                phrases;
                correct: 207.
            
                accuracy: 91.06 %;
                precision: 22.72 %;
                recall: 24.76 %;
                FB1: 23.70
            
                corporation:
                precision: 3.39 %;
                recall: 23.53 %;
                FB1: 5.93
                8
    
                creative - work:
                precision: 0.00 %;
                recall: 0.00 %;
                FB1: 0.00
                0
                
                group:
                precision: 0.00 %;
                recall: 0.00 %;
                FB1: 0.00
                0
                
                location:
                precision: 9.18 %;
                recall: 37.84 %;
                FB1: 14.78
                28
                
                person:
                precision: 46.22 %;
                recall: 36.38 %;
                FB1: 40.71
                171
                
                product:
                precision: 0.00 %;
                recall: 0.00 %;
                FB1: 0.00
                0"""

        print("Expected output when evaluating with wnuteval.py:")
        print(expected_output)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--wnut_file", type=str,
                        default="emerging_entities_17/emerging.dev.conll",
                        help="wnut tsv file including annotations")
    parser.add_argument("--output_file", type=str, default="predictions.tsv",
                        help="file to write results")

    args = parser.parse_args()

    main(args.wnut_file, args.output_file)
