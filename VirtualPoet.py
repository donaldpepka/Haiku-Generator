import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import requests


# takes in corpus, converted into list of tokens, with punctuation.
# outputs adjacent words as a generator
def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield corpus[i], corpus[i+1]


def make_triplets(corpus):
    for i in range(len(corpus)-2):
        yield corpus[i], corpus[i+1], corpus[i+2]


# works a little different from the normal markov chain; this takes two words and finds
# one likely to come after it. I came up with this, based on the original markov_text()
# it's more intensive and slower, but it produces much more reasonable results
def enhanced_markov():
    corpus = open('NewHaikus.csv', encoding='utf8').read()
    haikus = corpus.split()
    triplet_dict = {}
    pair_dict = {}
    word_count = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    triplets = make_triplets(haikus)
    pairs = make_pairs(haikus)

    for word_1, word_2 in pairs:
        if word_1 in pair_dict.keys():
            pair_dict[word_1].append(word_2)
        else:
            pair_dict[word_1] = [word_2]

    for word_1, word_2, word_3 in triplets:
        if (word_1, word_2) in triplet_dict.keys():
            triplet_dict[(word_1, word_2)].append(word_3)
        else:
            triplet_dict[(word_1, word_2)] = [word_3]

    first_word = np.random.choice(haikus)
    second_word = np.random.choice(pair_dict[first_word])
    chain = [first_word, second_word]
    n_words = np.random.choice(word_count)

    for i in range(n_words):
        chain.append(np.random.choice(triplet_dict[(chain[-2], chain[-1])]))

    result = ' '.join(chain)

    temp = result[0]
    result = result[1:]
    result = temp.upper() + result
    return result


# I did not invent this code; someone else came up with most of this, and I made a few small
# adjustments. this creates a semi-random sentence, with 3-17 words.
def markov_text():
    corpus = open('NewHaikus.csv', encoding='utf8').read()
    haikus = corpus.split()
    word_dict = {}
    word_count = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    pairs = make_pairs(haikus)

    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    first_word = np.random.choice(haikus)
    chain = [first_word]
    n_words = np.random.choice(word_count)

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    result = ' '.join(chain)

    temp = result[0]
    result = result[1:]
    result = temp.upper() + result
    return result


# takes in a word as string. returns its syllable count as int.
# word must be in the vocabulary
def get_syllable(word):
    df = pd.read_csv("NewVocabulary.csv")
    vocab = df["Vocab"].tolist()
    cleaned = clean_text(word)
    try:
        index = vocab.index(cleaned)
    except ValueError:
        try:
            index = vocab.index(cleaned.lower())
        except ValueError:
            update_vocab(cleaned)
            return get_syllable(cleaned)
    return df.at[index, "Syllables"]


# finds syllables of a word off the internet; copied from SyllableScraper.py
def find_syllables(word, base):
    key = ""
    word = word.lower()
    page = requests.get(base + word)
    soup = BeautifulSoup(page.content, 'html.parser')
    souper = soup.findAll("style")

    temp = str(souper)
    if "abxy" in temp:
        index = temp.find("abxy")
        key = temp[index:index+7]
    else:
        return None

    soupy = soup.select("#"+key)
    ans = soupy[0].get_text()
    return int(ans)


# input a word; this function adds the word to the vocabulary csv, and its syllable. no output
def update_vocab(word):
    df = pd.DataFrame()
    df["Vocab"] = [word]
    df["Syllables"] = [find_syllables(word, "https://www.howmanysyllables.com/words/")]
    df.to_csv("NewVocabulary.csv", mode='a', header=False)


# alternatively, input a word and its syllable count to add this information to the vocabulary.
def update_vocab(word, syllable):
    df = pd.DataFrame()
    df["Vocab"] = [word]
    df["Syllables"] = [syllable]
    df.to_csv("NewVocabulary.csv", mode='a', header=False)


# better version which demands user input
def query_vocab(word):
    frame = pd.DataFrame()
    frame["Vocab"] = [word]
    syllable = find_syllables(word, "https://www.howmanysyllables.com/words/")
    if syllable is not None:
        frame["Syllables"] = [syllable]
    else:
        syllable = int(input("Enter the number of syllables in " + word + ". "))
        frame["Syllables"] = [syllable]
    frame.to_csv("NewVocabulary.csv", mode='a', header=False)


# takes in phrase as string. returns phrase as string, with annoying characters stripped away.
def clean_text(phrase):
    punctuation = ['.', '-', '?', '!', '"', ';', ':', '"', ',', "—"]
    text = list(phrase)
    for i in punctuation:
        while i in text:
            text.remove(i)

    text = ''.join(text)
    return text


# takes in a sentence (or part of a sentence) as a string, and a syllable size count as an int.
# returns the first subsentence with syllable length equal to size, if possible.
# if not, (word order doesn't work, or not enough total syllables) returns None.
# in some ways, this is the crown jewel of this whole project. this is what everything relies on,
# and what everything culminates in.
def fit_line(phrase, size):
    words = phrase.split()
    sentence = []
    running = 0
    for word in words:
        running += get_syllable(word)
        sentence.append(word)
        if running == size:
            return ' '.join(sentence)
        elif running > size:
            return None
    return None


# takes in a phrase, ideally a finished haiku, and inserts punctuation randomly in each space.
def random_punctuation(haiku):
    punctuation = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                   ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                   '. ', '. ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                   '. ', '. ', '. ', '. ', '. ', '? ', '! ', ' -- ', ' -- ', '... ', '; ']
    temp = haiku.split()
    result = ""
    for word in temp:
        if temp.index(word) != len(temp)-1:
            result += word + np.random.choice(punctuation)
        else:
            result += word
    return result


# takes in sentence(s) as string (could be random, could be not) and tries to shape it into a
# haiku. if it can, returns a finished haiku. if not, returns None.
def haiku_parser(text):
    end_punctuation = ['.', '.', '.', '.', '.', '.', '.', '?', '!', '--', '...']
    haiku = clean_text(text)
    haiku = haiku.split()
    while ' ' in haiku:
        haiku.remove(' ')
    haiku = ' '.join(haiku)
    line1 = fit_line(haiku, 5)
    if line1 is None:
        return None
    haiku = haiku.replace(line1, '')
    line2 = fit_line(haiku, 7)
    if line2 is None:
        return None
    haiku = haiku.replace(line2, '')
    line3 = fit_line(haiku, 5)
    if line3 is None:
        return None
    line1 = random_punctuation(line1)
    line2 = random_punctuation(line2)
    line3 = random_punctuation(line3)
    result = line1 + "\n" + line2 + "\n" + line3 + np.random.choice(end_punctuation)
    return result


# draws random text until it can make a haiku; then returns a haiku.
def generate_haiku():
    haiku = ""
    while haiku == "":
        text = haiku_parser(markov_text())
        if text is None:
            haiku = ""
        else:
            haiku = text
    return haiku


def generate_enhanced_haiku():
    haiku = ""
    while haiku == "":
        text = haiku_parser(enhanced_markov())
        if text is None:
            haiku = ""
        else:
            haiku = text
    return haiku


go = True
print("Welcome! Would you like")
print("a haiku? Then enter 'h'")
print("or type 'q' to quit.")
while go:
    action = input()
    if action == 'h':
        print(generate_enhanced_haiku())
    elif action == 'q':
        go = False
    else:
        print("Error. Unrecognized input.")