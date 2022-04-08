import pandas as pd

# constant
DATA_FILE = "tweets.csv"
VULGARITY_FILES = "swear_voc.txt"
OUT_FILE = "vulgar_tweets.csv"

# load vulgarity
vulgars = set()
with open(VULGARITY_FILES, "r") as f:
    for line in f:
        vulgars.add(line.strip())        

# check if the sentence contains vulgar language
def is_vulgar(str):
    for word in str.split():
        if word.lower().strip() in vulgars:
            return True
    return False

# using twitter data
data = pd.read_csv(DATA_FILE)
data["vulgarity"] = data["content"].apply(lambda x: is_vulgar(x))
data.to_csv(OUT_FILE, index=False)

# proportion of vulgarity
N = data.shape[0] # number of tweets
N_is_vulgar = data[data["vulgarity"] == True].shape[0] # number of tweets with vulgarity
print("{}/{} ({:.2f}%) tweets contain vulgarity".format(N_is_vulgar, N, 100*N_is_vulgar/N))