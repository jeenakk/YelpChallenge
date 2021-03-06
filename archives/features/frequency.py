import sys

# Tools
from utils import disp, data

# parsing
import json
from tokenizer import Tokenizer

# storing data
from collections import Counter

root = data.getParent(__file__)
#filename = root + "/dataset/yelp_academic_dataset_review_training_small.json"
filename = sys.argv[1]

# Variables

# number of reviews a token has to appear to be kept
hardthreshold = 2

print "> Scanning data"
print "Loading file", filename

reviews_feature = dict()
reviews_score = dict()
alltoken = dict()

tok = Tokenizer(preserve_case=True)
# extracting tokens
for line in data.generateLine(filename):
  review = json.loads(line)
  reviewid = review['review_id']
  text = tok.ngrams(review['text'], 1, 3)
  score = int(review['stars'])
  
  reviews_feature[reviewid] = Counter(text)
  reviews_score[reviewid] = score
  
  for token in text:
    if token not in alltoken:
      alltoken[token] = Counter()

    alltoken[token][reviewid] += 1

print "> End of full scan"
print "Total tokens", len(alltoken)

print "> Prunning"
releasedtoken = set(filter(lambda x: len(alltoken[x]) < hardthreshold, alltoken.keys()))
print "Pruning", str(len(releasedtoken)), "tokens"

for token in releasedtoken:
  del alltoken[token]

for reviewid in reviews_feature:
  tokens = list(reviews_feature[reviewid].keys())
  for token in tokens:
    if token in releasedtoken:
      del reviews_feature[reviewid][token]
print "> End prunning"


print "> Saving"
data.saveFile(alltoken, root + "/computed/alltoken.pkl")
data.saveFile(reviews_feature, root + "/computed/reviews_feature.pkl")
data.saveFile(reviews_score, root + "/computed/reviews_score.pkl")
