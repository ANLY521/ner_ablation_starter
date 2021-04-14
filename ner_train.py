# coding: utf-8

import argparse
from util import read_ner_sents
from nltk.tag.crf import CRFTagger


#TODO 1 create subclass of CRFTagger
# only overwrite the method _get_features
# your version of _get_features should inherit the features
# from the parent and add word shape features
def word_shapes(word):
    shape = []
    for char in word:
        if char.isupper():
            shape.append("X")
        if char.islower():
            shape.append("x")
    return "".join(shape)



class MyTagger(CRFTagger):
    """Adds word shape features to the CRFTagger feature function"""

    def _get_features(self, tokens, idx):

        # get the list returned by the parent class method
        feature_list = super()._get_features(tokens, idx)

        wordshape = word_shapes(tokens[idx])
        if wordshape:
            feature_list.append(wordshape)

        return feature_list


def main(train_file, dev_file):
    # load the train data
    train_sents = read_ner_sents(train_file)

    train_data = []
    for example in train_sents:
        if example:
            train_data.append([token.split('\t') for token in example])

    print("training")
    # TODO 2: instantiate your class and train
    crf = MyTagger()
    crf.train(train_data, 'model.wnut.tagger')


    # quick debug
    sample_sentences = [
        "You should ' ve stayed on Redondo Beach Blvd .".split(),
        "All I ' ve been doing is BINGE watching Rick and Morty ".split()
    ]
    print(crf.tag(sample_sentences[0]))
    print("\n")
    print(crf.tag(sample_sentences[1]))

    dev_sents = read_ner_sents(dev_file)
    print("writing output")

    with open("mytagger_output.tsv", 'w') as pred_file:
        for sent in dev_sents:
            # TODO 3: predict, then write your outputs
            # use the tab-separated format required for wnuteval.py
            sent_words = [line.split()[0] for line in sent]
            gold_tags = [line.split()[1] for line in sent]

            with_tags = crf.tag(sent_words)

            for i, output in enumerate(with_tags):
                original_word, tag_prediction = output
                line_as_str = f"{original_word}\t{gold_tags[i]}\t{tag_prediction}\n"
                pred_file.write(line_as_str)
            # add an empty line after each sentence
            pred_file.write("\n")


    expected_output = """### ENTITY F1-SCORES ###
        processed 15733 tokens with 836 phrases; 
        found: 161 phrases; correct: 39.
        
        accuracy:  91.25%; 
        precision:  24.22%; 
        recall:   4.67%; 
        FB1:   7.82
        
              corporation: 
        precision:   0.00%; 
        recall:   0.00%; 
        FB1:   0.00  0
        
            creative-work: 
        precision:   0.00%; 
        recall:   0.00%; 
        FB1:   0.00  0
        
                    group: 
        precision:   0.00%; 
        recall:   0.00%; 
        FB1:   0.00  0
        
                 location: 
        precision:  26.53%; 
        recall:  17.57%; 
        FB1:  21.14  13
        
                   person: 
        precision:  35.62%; 
        recall:   5.53%; 
        FB1:   9.58  26
        
                  product: 
        precision:   0.00%; 
        recall:   0.00%; 
        FB1:   0.00  0"""


    print("Expected output when evaluating with wnuteval.py:")
    print(expected_output)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", type=str,
                        default="emerging_entities_17/wnut17train.conll",
                        help="wnut tsv file including annotations")
    parser.add_argument("--dev_file", type=str,
                        default="emerging_entities_17/emerging.dev.conll",)

    args = parser.parse_args()

    main(args.train_file, args.dev_file)
