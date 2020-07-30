# Haiku Generator
Creates random haikus using Markov chains and web-scraping. This is intended to be a birthday present for a friend of mine.

## Files

EditVocabulary.py: Cleans text within the vocabulary csv.

HaikuScraper.py: Scrapes haikus off of temps libres (https://www.tempslibres.org/tl/tlphp/dbauteursl.php?lang=en&lg=e) and writes them to a csv.

SyllableScraper.py: Scrapes syllable counts for every word in the vocabulary off of How Many Syllables (https://www.howmanysyllables.com/words/) and writes these to a csv with the corresponding vocabulary word. Initially intended to scrape this off of Dictionary.com (https://www.dictionary.com/) but that did not work.

fixHaikuText.py: Cleans the text in the haiku csv. Also has the critical function of separating hyphenated words, since How Many Syllables cannot process such words.

VirtualPoet.py: Uses a Markov chain to generate a random string of text. Then uses syllable counts of individual vocabulary words to determine how to divide the text into a haiku, if it is possible at all. Finally, adds punctuation randomly into the haiku. NewHaikus.csv serves as the corpus from which the random text is drawn.

setup.py: Running this code from the console freezes VirtualPoet.py, creating VirtualPoet.exe, a dll file, and a lib folder, so that this code can be easily distributed to anyone (does not work for Mac users).
