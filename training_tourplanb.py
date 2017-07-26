from gensim.models.word2vec import Word2Vec
import multiprocessing
import codecs
import time
import numpy as np

tpbPlaces = np.load(file="tmp2.npy")
tpbPlaces = tpbPlaces.tolist()
print("open data")

start = time.time()
size=128
batch_words=100000
iter=1000
min_count = 0
print("training start time:", start)
model = Word2Vec(tpbPlaces, size = size, sg=1, batch_words = batch_words, iter = iter, min_count=min_count, workers=multiprocessing.cpu_count())


# model = Doc2Vec(alpha=0.025, min_alpha=0.025)
# model.build_vocab(tpbPlaces, keep_raw_vocab=True)
# for epoch in range(10) :
#     model.train(tpbPlaces)
#     model.alpha -= 0.002
#     model.min_alpha = model.alpah

print("word2vec done")
print("word2vec time: ", time.time() - start)
# print("doc2vec done")
# print("doc2vec time: ", time.time() - start)


model.save("tourplanb_place_saved_word2vec_model")
# model.save("tourplanb_place_saved_doc2vec_model")
print("save done")
print("saved word : ", len(model.wv.vocab))
