from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd

df = pd.DataFrame()

df["col1"] = ["apple"]
df["col2"] = ["orange"]

df.to_csv("test.csv", mode='a', header=False)