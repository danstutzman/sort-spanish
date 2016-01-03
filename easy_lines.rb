#!/usr/bin/ruby
require 'json'
require 'unicode_utils/downcase'

if File.exists? 'rate_words.json'
  word2rating = JSON.parse(File.read('rate_words.json'))
else
  word2rating = {}
end

text_line2total_score = {}
text_line2artist_name = {}
i = 0
File.open('a.txt').each_line do |line|
  object = JSON.parse(line)
  if object['type'] == 'song_text'
    object['song_text'].each do |line2|
      text_line = UnicodeUtils.downcase(line2)
      scores = []
      text_line.split(/[^0-9a-zñáéíóúü]+/).each do |word|
        if word2rating[word] && word2rating[word] != 0
          scores.push word2rating[word] - 1.1
        else
          scores.push (3 - 1.1)
        end
      end
      total_score = scores.reduce { |a, b| a + b }
      if total_score
        text_line2total_score[text_line] = total_score
        text_line2artist_name[text_line] = object['artist_name']
      end
    end
  end
  i += 1
  break if i > 1000
end

text_line2total_score.sort_by { |text, total_score| -total_score }.each do |text, total_score|
  artist_name = text_line2artist_name[text]
  puts sprintf('%5.1f %-20s %s', total_score, artist_name, text)
end
