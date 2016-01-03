#!/usr/bin/ruby
require 'json'
require 'unicode_utils/downcase'

if File.exists? 'rate_words.json'
  word2rating = JSON.parse(File.read('rate_words.json'))
else
  word2rating = {}
end

word2count = {}
i = 0
File.open('a.txt').each_line do |line|
  object = JSON.parse(line)
  if object['type'] == 'song_text'
    text = UnicodeUtils.downcase(object['song_text'].map { |l| l.strip }.join(' '))
    text.split(/[^0-9a-zñáéíóúü]+/).each do |word|
      word2count[word] ||= 0
      word2count[word] += 1
    end
  end
  i += 1
  break if i > 1000
end

words = word2count.sort_by { |word, count| -count }.map { |word, count| word }.reject { |word| word2rating[word] }
while true
  word = words.shift
  p [word2rating.size, words.size]
  puts "Difficulty of: #{word}" # (#{word2count[word]}x)"
  rating = readline.to_i
  word2rating[word] = rating
  File.open 'rate_words.json', 'w' do |outfile|
    outfile.write JSON.dump(word2rating)
  end
end
