require 'json'

STDERR.puts "Reading words.en.txt..."
en_words = {}
File.open('words.en.txt').each_line do |line|
  en_words[line.strip.downcase] = true
end

STDERR.puts "Reading words.es.txt..."
es_words = {}
File.open('words.es.txt').each_line do |line|
  line.strip.split(' ').each do |word|
    es_words[word.downcase] = true
  end
end

STDERR.puts "Reading akwid.raw.txt..."
lines = []
File.open('akwid.raw.txt').each_line do |line|
  object = JSON.parse(line)
  if object['type'] == 'song_text'
    lines += object['song_text']
  end
end

STDERR.puts "Processing and sorting..."

lines.map! { |line| line.strip }
lines.reject! { |line| line == '' }

lines.reject! do |line|
  words = line.downcase.split(/\s/)
  num_en_words = words.count { |word| en_words[word] }
  num_es_words = words.count { |word| es_words[word] }
  num_es_words < num_en_words || (num_es_words < words.size / 2)
end

File.open 'akwid.clean.txt', 'w' do |file|
  for line in lines.sort_by { |line| line.length }.map { |line| line.downcase }
    file.puts line
  end
end
