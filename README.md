Training CRF's for NER on Emerging Entities
--------------------------------------------

This project trains conditional random fields models for named entity recognition 
using NLTK/CRFSuite for the WNUT2017 Emerging Entities Task.

Data and links to task information and paper are available 
[on github](https://github.com/leondz/emerging_entities_17). NOTE: there are illegal tags in the test data.


## wnuteval.py

Taken from the WNUT17 website. Slight modifications fix import error in Python 3 and stop crashing on 
illegal tags in test data. (This fix does NOT ensure test tags are valid.)

Use with a tab-separated submission in the form:
`<original word>  <gold standard tag>   <predicted tag>`

Example usage:

`python wnuteval.py my_predictions.tsv`

## Lab 1: ner_eval.py

Loads WNUT data and uses `nltk`'s `ne_chunk` to predict labels for each sentence.
HINT: requires part-of-speech tagging and conversion between tree and conll formats.

Converts entity classes using the scheme described below in Entity Mapping.

Writes a flat (text) file of NER predictions that can be scored by `wnuteval.py`.

```
python ner_eval.py --wnut_file emerging_entities_17/emerging.dev.conll --output_file predictions.tsv
python wnuteval.py predictions.tsv
```


### Entity mapping

 | Nltk entity type | WNUT entity  |
 | ------------- | ------------- |
 |ORGANIZATION | -> corporation |
 |PERSON | -> person |
 |LOCATION | -> location |
 |DATE | None |
 |TIME | None |
 |MONEY | None |
 |PERCENT| None |
 |FACILITY| -> location |
 |GPE | -> location |

## Lab 2: ner_train.py

`ner_train.py` creates a child class of `nltk.tag.crf.CRFTagger` that adds word shape information to the feature function.
Then it trains a tagger on WNUT train data and prints the results 
in a format that can be evaluated by wnuteval.py. 

`python ner_train.py --train_file emerging.train.conll --dev_file emerging.dev.conll`

## Homework: `ner_ablate.py`

Experiment with two additional features of your choosing on the WNUT
data. Train on train and write development set results on dev for four conditions:

* Base features (provided in starter code)
* Base + your feature 1
* Base + your feature 2
* All-in (Base + feature 1 + feature 2)

**Neither new feature can be the wordshape feature added in lab!**

Report your entity-level results in the table in Results. (Use `wnuteval.py`)
`python ner_ablate.py --train_file emerging.train.conll --dev_file emerging.dev.conll`

## Results

TODO: complete this chart with your Entity Precision/Recall/F1 on dev here.
Explain/motivate each feature you added (~2 sentences each) and
analyze your results (at least 3 sentences).


|Condition | F1 | Precision | Recall|
|--- | --- | ---|---|
|All-in | ? | ? | ?|
|(Fill in) | ? | ? | ?|
|(Fill in) | ? | ? | ?|
|Base | ? | ? | ?|
