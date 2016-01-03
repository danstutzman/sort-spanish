require 'json'
require 'unicode_utils/downcase'

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

STDERR.puts "Reading original a.txt..."
song_names2done = {}
File.open 'a.txt', 'w' do |outfile|
  %w[/Users/daniel/dev/scrape-spanish-lyrics/a.txt
     /Users/daniel/dev/scrape-spanish-lyrics/a2.txt].each do |path|
    File.open(path).each_line do |line|
      object = JSON.parse(line)
      if object['type'] == 'song_text'
        next if object['song_name'] == ''
        next if UnicodeUtils.downcase(object['song_name']).match(/es?p?a[nñ]ol/)
        next if UnicodeUtils.downcase(object['song_name']).match(/portugues/)
        next if song_names2done[object['song_name']]
        song_names2done[object['song_name']] = true
    
        text = object['song_text'].join(' ')
        words = UnicodeUtils.downcase(text).split(/\s/)
        num_en_words = words.count { |word| en_words[word] }
        num_es_words = words.count { |word| es_words[word] }
        if num_es_words < num_en_words || (num_es_words < words.size / 2)
          nil
        else
          outfile.write line
          puts object['song_name']
        end
      end
    end
  end
end
