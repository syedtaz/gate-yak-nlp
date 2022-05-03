from scipy.stats import fisher_exact
import numpy as np

# previous result (n=544, p=13.5%)
x = [74, 470]

# current result
SUMMARY_FILE = "./analysis/vulgarity_summary.txt"
outfile = open(SUMMARY_FILE, 'r')
line = outfile.readline()
y = line.split()[0].split("/")

# fischer's test
table = np.array([x, y])
_, p = fisher_exact(table, alternative='two-sided')
alpha = 0.05
print("There is {}a statistically significant difference in the frequency of vulgarity used with p={:.2e}"
      .format("NOT " if p > alpha else "", p))