import pandas as pd
from wordcloud import WordCloud as WC
from matplotlib import pylab as plt
from collections import Counter

# constant
DATA_FILE = "./data/yikyak.csv"
VULGARITY_FILES = "swear_voc.txt"
SUMMARY_FILE = "./analysis/vulgarity_summary.txt"
WORD_CLOUD = "./analysis/vulgarity_cloud.png"

# load vulgarity
vulgars = set()
with open(VULGARITY_FILES, "r") as f:
    for line in f:
        vulgars.add(line.strip())        

# check if the sentence contains vulgar language
def is_vulgar(x):
    if not isinstance(x, str):
        return False
    for word in x.split():
        if word.lower().strip() in vulgars:
            return True
    return False

def get_freq_vulgar(yaks):
    freq = Counter()
    for yak in yaks:
        if not isinstance(yak, str):
            continue
        for word in yak.split():
            if word.lower().strip() in vulgars:
                freq.update([word])
    return freq
                

# add vulgarity column in csv
data = pd.read_csv(DATA_FILE)
data["vulgarity"] = data["content"].apply(lambda x: is_vulgar(x))
data.to_csv(DATA_FILE, index=False)

# proportion of vulgarity
N = data.shape[0] # number of tweets
N_is_vulgar = data[data["vulgarity"] == True].shape[0] # number of tweets with vulgarity
outfile = open(SUMMARY_FILE, 'w')
outfile.write("{}/{} ({:.2f}%) tweets contain vulgarity".format(N_is_vulgar, N, 100*N_is_vulgar/N))

# get wordcloud
vulgar_freq = get_freq_vulgar(data["content"])
wc = WC().generate_from_frequencies(vulgar_freq)
plt.imshow(wc)
plt.axis('off')
plt.tight_layout()
plt.savefig(WORD_CLOUD)