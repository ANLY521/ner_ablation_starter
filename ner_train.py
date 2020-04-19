# coding: utf-8

import argparse
from util import read_ner_sents
from nltk.tag.crf import CRFTagger


#TODO create subclass of CRFTagger

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

    sample_sentences = [
        "You should ' ve stayed on Redondo Beach Blvd .".split(),
        "All I ' ve been doing is BINGE watching Rick and Morty ".split()
    ]

    # load the train data

    train_sents = read_ner_sents(train_file)

    train_data = []
    for example in train_sents:
        if example:
            train_data.append([token.split('\t') for token in example])

    print(train_data[0])

    crf = MyTagger()
    print("training")
    crf.train(train_data, 'model.wnut.tagger')

    print("training")
    print(crf.tag(sample_sentences[0]))
    print("\n")
    print(crf.tag(sample_sentences[1]))


    dev_sents = read_ner_sents(dev_file)
    print("writing output")

    with open("mytagger_output.tsv", 'w') as pred_file:
        for sent in dev_sents:
            sent_words = [line.split()[0] for line in sent]
            gold_tags = [line.split()[1] for line in sent]

            with_tags = crf.tag(sent_words)

            for i, output in enumerate(with_tags):
                original_word, tag_prediction = output
                line_as_str = f"{original_word}\t{gold_tags[i]}\t{tag_prediction}\n"
                pred_file.write(line_as_str)
            # add an empty line after each sentence
            pred_file.write("\n")




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", type=str,
                        default="../emerging_entities_17/wnut17train.conll",
                        help="wnut tsv file including annotations")
    parser.add_argument("--dev_file", type=str,
                        default="../emerging_entities_17/emerging.dev.conll",)

    args = parser.parse_args()
    
    for word in "Hello , today is Thursday ! 123 , Dr.".split():
        print(f"Word: {word}\tShape: {word_shapes(word)}")
        print()

    main(args.train_file, args.dev_file)
