import os
import h5py
import numpy as np

import gensim.models as gm

import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import verbnet

# get news titles from raw news files
def get_news_title(news_raw_dir, news_title_dir):
    for dirpath, dirname, filenames in os.walk(news_raw_dir):
        for filename in [f for f in filenames if f.endswith('.txt')]:
            title = ''
            # get titles
            if 'bloomberg' in dirpath:
                with open(os.path.join(dirpath, filename), 'r') as f:
                    title = f.readline().strip()
                    title = title.replace('- Bloomberg', '').strip()
                    print(title)
                f.close()

            tokens = dirpath.split('/')
            # dest dir
            dest_dirpath = news_title_dir + '/' + tokens[-1]
            if not os.path.exists(dest_dirpath):
                os.makedirs(dest_dirpath)

            # dest filename
            dest_filename = os.path.join(dest_dirpath, filename)
            
            # write title as content
            if not os.path.exists(dest_filename):
                with open(dest_filename, 'w') as f:
                    f.write(title + '\n')
                f.close()

# change from treebank tag to wordnet tag
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    elif treebank_tag.startswith('J'):
        return wordnet.ADJ
    else:
        raise 'No such tags!'

# lemmatize word according to wordnet
def lemmatize_word(word, wordnet_tag):
    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word, wordnet_tag)

    return lemma

# get all news title tags
def get_tags(news_title_dir, news_tag_dir):
    for dirpath, dirnames, filenames in os.walk(news_title_dir):
        for filename in [f for f in filenames if f.endswith('.txt')]:
            title = ''
            # get titles
            with open(os.path.join(dirpath, filename), 'r') as f:
                title = f.readline().strip()
                print(title)
            f.close()

            tokens = dirpath.split('/')
            # dest dir
            dest_dirpath = news_tag_dir + '/' + tokens[-1]
            if not os.path.exists(dest_dirpath):
                os.makedirs(dest_dirpath)

            # dest filename
            dest_filename = os.path.join(dest_dirpath, filename)
            
            # tag words
            target_tag_list = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VB                  N', 'VBP', 'VBZ', 'RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS']
            if not os.path.exists(dest_filename):
                with open(dest_filename, 'w') as f:
                    word_tokens = word_tokenize(title.lower())
                    tags = nltk.pos_tag(word_tokens)
                    for word, tag in tags:
                        if tag in target_tag_list:  # filter meaningless words
                            wordnet_tag = get_wordnet_pos(tag)
                            if wordnet_tag == 'v' or wordnet_tag == 'n':    # lemmatize verb and noun
                                lemma = lemmatize_word(word, wordnet_tag)
                                f.write(wordnet_tag + ' ' + lemma + '\n')
                                print(wordnet_tag + ' ' + lemma)
                            else:
                                f.write(wordnet_tag + ' ' + word + '\n')
                                print(wordnet_tag + ' ' + word)
                f.close()

# word to vector
def word_to_vector(news_tag_dir, news_word2vec_dir, word2vec_model_path):
    # load Google word2vec model
    model = gm.KeyedVectors.load_word2vec_format(word2vec_model_path, binary = True)

    for dirpath, dirname, filenames in os.walk(news_tag_dir):
        for filename in [f for f in filenames if f.endswith('.txt')]:
            # dest dir_path
            tokens = dirpath.split('/')
            dest_dirpath = news_word2vec_dir + '/' + tokens[-1]

            if not os.path.exists(dest_dirpath):
                os.makedirs(dest_dirpath)

            # dest filename
            dest_filename = os.path.join(dest_dirpath, filename) 
            dest_filename = dest_filename.replace('.txt', '.h5')

            feature = np.array([])
            if not os.path.exists(dest_filename): 
                with open(os.path.join(dirpath, filename), 'r') as f:           
                    for line in f: # one word per line
                        tag, word = line.strip().split(' ')
                        try:
                            vector = model.word_vec(word)
                            if feature.size == 0:
                                feature = np.hstack((feature, vector))
                            else:
                                feature = np.vstack((feature, vector))
                        except KeyError:
                            continue
                        print(feature.shape)

                f.close()

                hf = h5py.File(dest_filename, 'w')  # save word vector feature
                hf.create_dataset('feature', data = feature)
                hf.close()
