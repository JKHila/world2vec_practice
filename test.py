# coding=utf-8
import gensim
#from lib.jamo import differences, shortest_word
import operator
import sys

a = gensim.models.word2vec.Word2Vec.load("tourplanb_test2/tourplanb_place_saved_word2vec_model")


while (True) :

    b = input("단어를 입력하세요 (positive) :")
    b = b.split(",")
    # b = findAndReplace(b)
    # b = shortest_word(b, a.wv.vocab)
    c = input("단어를 입력하세요 (negative) :")
    if (c) :
        c = c.split(",")
    else :
        c = ""
    # c = shortest_word(c, a.wv.vocab)

    try:
        print(a.most_similar(positive=b, negative=c))
        pass
    except Exception as e:

        print (e)
        print("그런 단어 없습니다.")


    else:
        pass
