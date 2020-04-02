# coding: utf-8

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

