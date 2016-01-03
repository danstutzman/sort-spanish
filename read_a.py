# coding=UTF-8
import codecs
import math
import json
import pattern.es
import re
import sys

#with codecs.open('lemma2num_tokens.json', 'r', 'utf-8') as infile:
#  lemma_tag2num_tokens = json.load(infile)

with codecs.open('rate_words.json', 'r', 'utf-8') as infile:
  word2score = json.load(infile)

with codecs.open('a.txt', 'r', 'utf-8') as f:
  for line in f:
    o = json.loads(line)
    if o['type'] == 'song_text' and not o['song_text'][0].startswith('Letra no disponible'):
      #   o['song_text'][1].startswith('Letra no disponible'):
      #  next

      #num_words = 0
      #num_recognized_words = 0
      #num_verbs = 0
      #num_present_verbs = 0
      #scores = []
      #lemma_tags = {}
      #for line in o['song_text']:
      #  sentences = pattern.es.parsetree(line, lemmata=True)
      #  for sentence in sentences:
      #    for word in sentence:
      #      num_words += 1
      #      if word.type and word.type.startswith('V'):
      #        num_verbs += 1
      #        for tense in pattern.es.tenses(word.string):
      #          time, person, number, indic_vs_imper, per_or_imper = tense
      #          if time == 'present':
      #            num_present_verbs += 1
                  #print word.string

      #      lemma_tag = word.lemma + '/' + word.tag
      #      lemma_tags[lemma_tag] = True
      #      #num_tokens = lemma_tag2num_tokens.get(lemma_tag)
      #      #if num_tokens:
      #      #  score = math.log(1000000.0 / num_tokens)
      #      #  scores.append(score)
      #      #  num_recognized_words += 1

      scores = []
      already_counted = {}
      for line in o['song_text']:
        for word in re.split(r'[^0-9a-zñáéíóúü]+', line.lower()):
          if word not in already_counted:
            already_counted[word] = True
            score = word2score.get(word, 4)
            if score > 0:
              scores.append(score)
      output = '%5.1f %-28s %s' % \
        (float(sum(scores)) / len(scores), o['path'], o['song_name'])
      print output.encode('utf-8')

      #for lemma_tag in lemma_tags.keys():
      #  num_tokens = lemma_tag2num_tokens.get(lemma_tag)
      #  if num_tokens:
      #    score = math.log(num_tokens)
      #    scores.append(score)
      #  else:
      #    scores.append(0)
      #total_score = sum(scores) / len(lemma_tags)
      #print ('%7.1f %-28s %s' % (total_score, o['path'], o['song_name'])).encode('utf-8')

      #print (u'%7.1f %-28s %s' % (sum(scores) / num_recognized_words, o['path'], o['song_name'])).encode('utf-8')
      #num_words = float(num_words)
      #if num_present_verbs/num_words >= 0.2:
      #    print u'v=%.2f pv=%.2f %s' % \
      #    (num_verbs/num_words,
      #     num_present_verbs/num_words,
      #     o['song_name'])
