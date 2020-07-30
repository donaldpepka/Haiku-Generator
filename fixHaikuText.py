import pandas as pd
import re


# takes in word containing hyphen. replaces hyphen with a space. returns word.
def remove_hyphen(word):
    while '-' in word:
        loc = word.find('-')
        word = word[0:loc] + " " + word[loc+1:]
    return word


# takes in a singular word; determines if the word is hyphenated. returns bool
def is_hyphenated(word):
    regex = re.compile('\w+(?:-\w+)+')
    inter = regex.match(word)
    if inter is None:
        return False
    else:
        return True


# goes through every word in haikus.csv and, if the word is hyphenated, it replaces the hyphen with a space.
df = pd.read_csv("Haikus.csv")
haikus = df['Haikus'].tolist()
remove_words = []

for i in range(len(haikus)):
    haikus[i] = haikus[i].split()
    for j in range(len(haikus[i])):
        if is_hyphenated(haikus[i][j]):
            haikus[i][j] = remove_hyphen(haikus[i][j])
    haikus[i] = ' '.join(haikus[i])

df['Haikus'] = haikus

df.to_csv('NewHaikus.csv', index=False)
