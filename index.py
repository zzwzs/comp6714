from cgitb import text
import sys
import re
import string
import os
import nltk
import pickle
nltk.download('wordnet',quiet=True)
nltk.download('omw-1.4',quiet=True)
nltk.download('punkt',quiet=True)
import nltk.stem as ns

if __name__ == '__main__':
  term_dict = {}
  data = []
  set_string = set()
  list_string = []
  for filename in os.listdir(sys.argv[1]):
    with open(sys.argv[1]+'/'+filename,"r",encoding='UTF-8') as textFile:
      single_string = textFile.readline().replace('\n',' ')
      line = single_string
      while line:
        #print(line)
        line = textFile.readline().replace('\n',' ')
        single_string += line
    #print(single_string)
    #single_string = re.sub(r'(\w+)\.\n', r'\1\n',single_string)
    single_string = re.sub(r'(\w+)\. ', r'\1\n',single_string)
    #single_string = re.sub(r'\n([a-z])', r' \1',single_string)
    single_string = re.sub(r'([A-Z])\n', r'\1 ',single_string)
    single_string = re.sub(r'([0-9])\n', r'\1 ',single_string)
    single_string = re.sub('\.', '',single_string)
    remove = string.punctuation
    remove = remove.replace("'","")
    #print(remove)
    blank = ''
    for i in range(len(remove)):
      blank += ' '
    table = str.maketrans(remove, blank)
    single_string = single_string.translate(table)
    single_string = re.sub(' \d+ ', ' ',single_string)
    single_string = re.sub(' \d+ ', ' ',single_string)
    #print(single_string)
    #single_string = re.sub(r'(\w+)\. ', r'\1\n',single_string)
    single_string = re.sub("s'", 's',single_string)
    single_string = re.sub("'s", '',single_string)
    single_string = re.sub("'", ' ',single_string)
    sentences = re.split('\n|\?|\!',single_string)
    for i in range(len(sentences)):
      if sentences[i][0] == ' ':
        sentences[i] = re.sub(' +', ' ',sentences[i]).lower()[1:]
      else:
        sentences[i] = re.sub(' +', ' ',sentences[i]).lower()
    #print(sentences)
    new_sentences = []
    for s in sentences:
      if s == '':
        continue
      tokens = nltk.word_tokenize(s)
      pos_tags = nltk.pos_tag(tokens)
      #print(pos_tags)
      new_string = ''
      for word in pos_tags:
        lemmatizer = ns.WordNetLemmatizer()
        if word[1][0] == 'N': 
          n_lemma = lemmatizer.lemmatize(word[0], pos='n')
          new_string += n_lemma
          new_string += ' '
          set_string.add(n_lemma)
          list_string.append(n_lemma)
        elif word[1][0] == 'V': 
          v_lemma = lemmatizer.lemmatize(word[0], pos='v')
          new_string += v_lemma
          new_string += ' '
          set_string.add(v_lemma)
          list_string.append(v_lemma)
        else:
          new_string += word[0]
          new_string += ' '
          set_string.add(word[0])
          list_string.append(word[0])
      new_sentences.append(new_string)
    data.append(new_sentences)
    pos_word = 0
    for i in range(len(new_sentences)):
      reg = new_sentences[i]
      if reg[-1] == ' ':
        reg = reg[:-1]
      s = reg.split(' ')
      #print(s)
      for j in range(len(s)):
        if s[j] not in term_dict:
          term_dict[s[j]] = [[filename],{filename : [[pos_word+j],[i]]}]
        else:
          if filename not in term_dict[s[j]][0]:
            term_dict[s[j]][0].append(filename)
            term_dict[s[j]][1][filename] = [[pos_word+j],[i]]
          else:
            term_dict[s[j]][1][filename][0].append(pos_word+j)
            term_dict[s[j]][1][filename][1].append(i)
      pos_word += len(s)

    #print(new_sentences)
  print(term_dict)
  documents = len(data)
  tokens = len(list_string)
  terms = len(set_string)
  print('Total number of documents: ' + str(documents))
  print('Total number of tokens: ' + str(tokens))
  print('Total number of terms: ' + str(terms))

  if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])
  with open(sys.argv[2]+'/'+'index', 'wb+') as f:
    f.write(pickle.dumps(term_dict))
