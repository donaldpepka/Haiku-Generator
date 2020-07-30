import pandas as pd


# cleans the text
def clean_text(phrase):
    punctuation = ['.', '?', '!', '-', '—', '"']
    text = list(phrase)
    for i in punctuation:
        while i in text:
            text.remove(i)

    text = ''.join(text)
    return text


# creates a new, updated vocab csv. This code has been through many many changes.kind of a mess
def new_Vocab():
    df = pd.read_csv("NewHaikus.csv")
    voc = pd.read_csv("Vocabulary.csv")
    old_vocab = voc["Vocab"].tolist()
    vocabulary = set()
    haikus = df['Haikus'].tolist()

    for haiku in haikus:
        haiku_list = set(haiku.split())
        vocabulary = vocabulary.union(haiku_list)
    vocabulary = list(vocabulary)

    for i in range(len(vocabulary)):
        vocabulary[i] = clean_text(vocabulary[i])

    with open('NewVocabulary.csv', 'w', encoding="utf8") as output:
        for word in vocabulary:
            output.write(word+'\n')
