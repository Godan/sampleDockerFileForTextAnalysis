#!/bin/env python
#coding:utf-8

import MeCab as mc
from collections import OrderedDict
from pprint import pprint
import pandas as pd
import os
from operator import add
from functools import reduce
import CaboCha as cabo


class TextAnalyze:
    def makeWordCountListByCabocha(self, text=None):

        if len(text) <= 0:
            return False
        wordList = []
        parser = cabo.Parser()

        result =  parser.parse(text)
        resultText = result.toString(cabo.FORMAT_LATTICE)

        tmpWord = ''
        tmpType = ''
        for row in resultText.splitlines():
            row = row.split('\t')
            word = row[0]

            if len(row) > 1:
                wordInfo = row[1].split(',')
            else:
                    wordInfo = None
            if wordInfo != None:
                # 関係なさそうなのは外す

                # 文節に来たら（*）リセットして次
                if word is '*':
                    tmpWord = ''
                    tmpType = ''
                    continue

                # 数字は飛ばす
                if str(word).isdigit():
                    continue

                # 一個前は名詞?
                if tmpType ==  wordInfo[0] and tmpType != '動詞':
                    if wordInfo[6] is '*':
                        tmpWord += word
                    else:
                        tmpWord += wordInfo[6]
                else:
                    if len(tmpWord) > 0 :
                        wordList.append(tmpWord)
                        tmpWord = ''
                        tmpType = ''

                    if wordInfo[0] in ['記号', '助詞', '接頭詞', '副詞', '助動詞', '動詞'] :
                        tmpWord = ''
                        tmpType = ''
                        continue
                    elif wordInfo[0]  is '動詞' and len(word) <= 1:
                        tmpWord = ''
                        tmpType = ''
                        continue
                    elif wordInfo[6] is '*':
                        tmpWord = word
                    else:
                        tmpWord = wordInfo[6]
                    tmpType = wordInfo[0]
            else:
                tmp=''

        # return resultText.splitlines()
        return wordList


    # カウントを行う
    def frequentWords(self, text=None):
        wordList = self.makeWordCountListByCabocha(text)
        if wordList == False:
            return False
        countList = {}

        for word in wordList:
            if word in countList:
                countList[word] += 1
            else:
                countList[word] = 1
        # 降順にして返す
        return OrderedDict(reversed(sorted(countList.items(), key=lambda x:x[1])))
