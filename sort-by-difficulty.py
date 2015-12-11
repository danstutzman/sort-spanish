import json
import math
import pattern.es
import codecs

with codecs.open('lemma2num_tokens.json', 'r', 'utf-8') as infile:
  lemma_tag2num_tokens = json.load(infile)

line2score = {}
for line in codecs.open('akwid.clean.txt', 'r', 'utf-8'):
  sentences = pattern.es.parsetree(line, lemmata=True)
  scores = []
  for sentence in sentences:
    for word in sentence:
      lemma_tag = word.lemma + '/' + word.tag
      num_tokens = lemma_tag2num_tokens.get(lemma_tag)
      if num_tokens:
        score = -math.log(1000000.0 / num_tokens)
      else:
        score = -99
      scores.append(score)
  sum_score = min(scores)
  line2score[line.strip()] = sum_score
for line in sorted(line2score, key=lambda line: line2score[line]):
  print line2score[line], line
