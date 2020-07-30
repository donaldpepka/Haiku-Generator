from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd


# takes in string; returns an integer representing the number of hyphens ("-") in the string
# this is defunct; it no longer is needed, thanks to find_syllables
def count_syllables(text):
    count = 0
    for i in text:
        if i == "-":
            count += 1
    return count + 1


# takes in word and base url as string; returns string representation of phonetic word pronunciation
# if the word is not found in the dictionary, the word is added to a list to be removed.
# this is defunct; it doesn't cover all cases.
def find_pron(word, base):
    try:
        page = requests.get(base+word)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup = soup.find("span", class_="pron-spell-content css-z3mf2 evh0tcl2")
        soup = soup.get_text()
        soup = soup.split()
        soup = soup[1]
        print(soup)
        return soup
    except AttributeError:
        remove_words.append(word)
        return


# takes in a list of words to remove; has no output.
# Copies file; removes words from copy; writes to new file.
# Removes words from Haikus
def delete_word(words):
    file = open("Haikus.csv", 'r', encoding="utf8")
    copy = file.readlines()

    for i in range(len(copy)):
        copy[i] = copy[i].split()
        for word in words:
            while word in copy[i]:
                copy[i].remove(word)
        copy[i] = ' '.join(copy[i])

    with open("NewHaikus.csv", 'w', encoding="utf8") as output:
        for line in copy:
            output.write(line+"\n")


# due to issues with dictionary.com, a new function was made to detect syllables, using a new
# website. it is more complicated, but it pulls the syllable count directly from the website.
# takes in word and url base as string. outputs syllable count as int (though it could be string)
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


link1 = "https://www.dictionary.com/browse/"
link2 = "https://www.howmanysyllables.com/words/"
dictionary = pd.read_csv("NewVocabulary.csv")
vocab = dictionary["Vocab"].tolist()
remove_words = []
syllables = []

for word in vocab:
    print(word)
    syllables.append(find_syllables(word, link2))

dictionary["Syllables"] = syllables

dictionary.to_csv("NewVocabulary.csv")

# delete_word(remove_words)
