from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

text = "test"
wc = WordCloud()
wc.generate(text)
wc.to_file('Wordcloud.png')
