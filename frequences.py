import nltk
from nltk import FreqDist
from nltk.corpus import brown
from nltk.corpus import inaugural
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math

brown_freq = FreqDist(brown.words())
print(brown_freq.most_common(10))
print(brown_freq["mother"])

for word in brown_freq.most_common():
    print("{} ~ {}".format("the", round(brown_freq.freq("the"), 2)))

print(sorted(brown_freq.hapaxes(), key = lambda w: len(w), reverse = True)[:20])

cats = ['mystery', 'adventure']
cfd = nltk.ConditionalFreqDist(
    (genre, word.lower())
    for genre in cats
    for word in brown.words(categories=genre))
print(cfd)

for cond in cfd.conditions():
    print(cond)
    print(cfd[cond].most_common(20))
    print()

for cond in cfd.conditions():
    print("mother in {} - {} - {}".format(cond, cfd[cond]["mother"], round(cfd[cond].freq("mother"), 4)))

print(sorted(stopwords.words('english')))

brown_freq.plot(50)

from nltk import WordNetLemmatizer

def convert_pos_tag(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith(('V', 'MD')):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    else:
        return 'r'

def lemmatize_tokens(tokens):
    lemmatized = []
    if type(tokens) == str:
        tokens = word_tokenize(tokens)
    for word in tokens:
        word = word.lower()
        treebank_tag = nltk.pos_tag([word])[0][1]
        wn_tag = convert_pos_tag(treebank_tag)
        # we'll lemmatize only adjectives, nouns, adverbs and verbs to save time
        if treebank_tag[0] in ['J', 'N', 'R', 'V']:
            word = WordNetLemmatizer().lemmatize(word, wn_tag)
        lemmatized.append(word)
    return lemmatized

print(inaugural.fileids())
speech_tokens = inaugural.words('1789-Washington.txt')
speech_tokens = list(speech_tokens)
print(speech_tokens[:30])
not_nes = []
for i in speech_tokens:
    if i in stopwords.words('english'):
            speech_tokens.remove(i)
lemmatized_t = lemmatize_tokens(speech_tokens)
print("Raw tokens:")
print(speech_tokens[:30])
print("Lemmatized:")
print(lemmatized_t[:30])


fd = FreqDist(lemmatized_t)
all_words = len(speech_tokens)
tf = dict(fd)
docs = inaugural.fileids()
sum_docs = len(docs)

corpus = inaugural.fileids()
lemmatized_data = {}
for doc in corpus:
    lemmatized_data[doc] = lemmatize_tokens(inaugural.words(doc))

idfs = {}

for text in lemmatized_data:
    words_in_doc = lemmatized_t
    lemmas = set(lemmatized_data[text])
    m = 0
for i in lemmatized_t:
    for lemma in lemmas:
        if i in lemma:
            if lemma not in idfs:
                idfs[lemma] = 1
            else:
                idfs[lemma] += 1
        else:
            m = m+1
for lemma in idfs:
    idfs[lemma] = round(math.log(len(lemmatized_data) / idfs[lemma]), 3)

print(idfs)

def calculate_tfidfs(texts, lemmatized_data, tfs, idfs):
    tfidfs = {}
    for text in texts:
        tfidfs[text] = {}
    for lemma in lemmatized_data[text]:
        tfidfs[text][lemma] = round(tfs[text][lemma] * idfs[lemma], 3)
        return tfidfs








