# coding=UTF-8
# Note: if you get UnicodeEncodeError, run with PYTHONIOENCODING=utf_8

import codecs
import glob
import json
import math
import re
import pattern.es
import subprocess

lemma_tag2num_tokens = {}
num_lemma_tag_tokens = 0
i = 0
for filename in glob.iglob('../spanish_in_texas/*.txt'):
#for filename in subprocess.check_output(['find', '../CORLEC_TXT_FINAL/', '-name', '*.txt']).split('\n'):
  i += 1
  #if i > 1: break
  if filename == '':
    continue
  print filename

  with codecs.open(filename, 'r', 'utf8') as f:
    for line in f:
      line = line.strip()

      if line != '':
        line = re.sub(r'^>>[si]: ', '', line)
        line = re.sub(u'[¿¡]', '', line)
        sentences = pattern.es.parsetree(line, lemmata=True)
        for sentence in sentences:
          for word in sentence:
            if re.match(u'^[a-záéíóúñü-]+$', word.lemma):
              lemma_tag = word.lemma + '/' + word.tag
              #if lemma not in ['.', ',', '?', '...', '!', '[', ']', 'no.', ';']:
              #  print lemma
              if not lemma_tag in lemma_tag2num_tokens:
                lemma_tag2num_tokens[lemma_tag] = 0
              lemma_tag2num_tokens[lemma_tag] += 1
              num_lemma_tag_tokens += 1

#for lemma_tag in sorted(lemma_tag2num_tokens, key=lambda lemma_tag: lemma_tag2num_tokens[lemma_tag]):
#  lemma, tag = lemma_tag.split('/')
#  #if not tag in ['DT', 'IN', 'WP$', 'CC', 'PRP', 'PRP$']:
#  if True:
#    print u'%-20s %-4s %6d'.encode('utf8') % \
#      (lemma, tag,
#      lemma_tag2num_tokens[lemma_tag] * 1000000.0 / num_lemma_tag_tokens)

#with open('lemma2num_tokens.json', 'w') as outfile:
#  json.dump(lemma_tag2num_tokens, outfile)

line2score = {}
for line in open('akwid.clean.txt'):
  sentences = pattern.es.parsetree(line, lemmata=True)
  sum_score = 0
  for sentence in sentences:
    for word in sentence:
      lemma_tag = word.lemma + '/' + word.tag
      num_tokens = lemma_tag2num_tokens.get(lemma_tag)
      if num_tokens:
        score = -math.log(1000000.0 / num_tokens)
      else:
        score = -99
      sum_score += score
  line2score[line.strip()] = sum_score
for line in sorted(line2score, key=lambda line: line2score[line]):
  print line2score[line], line
