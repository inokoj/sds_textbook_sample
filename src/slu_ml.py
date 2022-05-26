from __future__ import division

import sys, os
import re
import numpy as np
import pickle

from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from gensim.models import KeyedVectors

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

import MeCab

#
# 機械学習ベースの言語理解を行うクラス
#

class SluML(object):

	# 初期化
	def __init__(self):
		
		#
		# 学習済みモデルを読み込む
		#

		# ドメイン推定
		filename_model_domain_word2vec = './data/slu-domain-svm-word2vec.model'
		self.model_domain_word2vec = pickle.load(open(filename_model_domain_word2vec, 'rb'))

		# スロット値推定（レストラン検索）
		filename_model_slot_restaurant = './data/slu-slot-restaurant-crf.model'
		self.model_slot_restaurant = pickle.load(open(filename_model_slot_restaurant, 'rb'))

		# スロット値推定（天気案内）
		filename_model_slot_weather = './data/slu-slot-weather-crf.model'
		self.model_slot_weather = pickle.load(open(filename_model_slot_weather, 'rb'))
		
		# Word2vecモデルを読み込む
		model_filename = './data/entity_vector.model.bin'
		self.model_w2v = KeyedVectors.load_word2vec_format(model_filename, binary=True)

		# MeCabの初期化
		self.mecab_tagger = MeCab.Tagger ("-Owakati")
	
	# 入力文を単語に分割
	def _parse_input(self, input_sentence):

		# MeCabによる分割と特徴量抽出
		m = MeCab.Tagger ("-Owakati")
		words_input = m.parse(input_sentence).strip().split(' ')

		return words_input
	
	# Word2vecで特徴量を作成する関数を定義
	# ここでは文内の各単語のWord2vecを足し合わせたものを文ベクトルとして利用する
	def _make_sentence_vec_with_w2v(self, words):

		sentence_vec = np.zeros(self.model_w2v.vector_size)
		num_valid_word = 0
		for w in words:
			if w in self.model_w2v:
				sentence_vec += self.model_w2v[w]
				num_valid_word += 1
		
		# 有効な単語数で割
		sentence_vec /= num_valid_word
		return sentence_vec
	
	# ドメイン推定を行う
	def estimate_domain(self, sentence):

		words = self._parse_input(sentence)
		featvec = self._make_sentence_vec_with_w2v(words)
		result = self.model_domain_word2vec.predict([featvec])[0]

		return result
	
	# スロット値抽出を行う（レストラン検索）
	def extract_slot_restaurant(self, sentence):

		return self._extract_slot(sentence, self.model_slot_restaurant)
	
	# スロット値抽出を行う（天気案内）
	def extract_slot_weather(self, sentence):

		return self._extract_slot(sentence, self.model_slot_weather)

	# スロット値抽出を行う
	def _extract_slot(self, sentence, model):

		words = self._parse_input(sentence)
		predict_y = model.predict([words])[0]

		for word, tag in zip(words, predict_y):
			print(word + "\t" + tag)

		# 推定したタグの情報からスロット値を抽出する
		slot_extracted = {}
		word_extracted = ''
		last_slot_name = ''
		found = False
		for idx, (word, tag) in enumerate(zip(words, predict_y)):
			
			if tag.startswith('B-'):
				
				slot_name_extracted = tag.split('-')[1].strip()

				# スロットの終端を検出
				if found == True and last_slot_name != slot_name_extracted:
					slot_extracted[last_slot_name] = word_extracted
					last_slot_name = ''
					word_extracted = ''
					found = False
				
				word_extracted += word
				last_slot_name = slot_name_extracted
				found = True
			
			if found == True and tag.startswith('I-'):
				slot_name_extracted = tag.split('-')[1].strip()
				
				if last_slot_name == slot_name_extracted:
					word_extracted += word
				
				# 実際にはあり得ないがスロットの終端を検出
				else:
					slot_extracted[last_slot_name] = word_extracted
					last_slot_name = ''
					word_extracted = ''
					found = False
			
			# スロットの終端を検出
			if found == True and tag == 'O':
				slot_extracted[last_slot_name] = word_extracted
				last_slot_name = ''
				word_extracted = ''
				found = False
			
		if found == True:
			slot_extracted[last_slot_name] = word_extracted
		
		# 他の言語理解のフォーマットに揃える
		results = []
		for label, slot_value in slot_extracted.items():

			results.append({'intent': '', 'slot_name': label, 'slot_value': slot_value})

		return results


if __name__ == '__main__':

	parser = SluML()

	# 入力データを読み込む
	with open('./data/slu-sample3.txt', 'r', encoding='utf-8') as f:
		lines = f.readlines()

	list_input_data = []
	for line in lines:
		if not line.strip():
			continue
		list_input_data.append(line.strip())

	# 入力文をマッチさせてみる
	for data in list_input_data:

		print('-----------------------')
		print('入力：' + data)
		
		# ドメイン推定
		domain = parser.estimate_domain(data)
		print('[Domain] %d' % domain)
		print()

		# スロット値抽出
		slots = parser.extract_slot_restaurant(data)
		print('[Slot]')
		print(slots)
		print()

