from __future__ import division

import sys, os
import numpy as np
import MeCab
from gensim.models import KeyedVectors

#
# 用例ベースの対話
#

class ExampleBased(object):

	# 初期化
	def __init__(self):
		
		# 用例データを読み込む
		self.pair_data = []
		filename = './data/example-base-data.csv'
		print('Load from %s' % filename)
		with open(filename, 'r', encoding='utf8') as f:
			lines = f.readlines()
			for line in lines:
				u1 = line.split(',')[0].strip()
				u2 = line.split(',')[1].strip()
				self.pair_data.append([u1, u2])
				print('%s -> %s' % (u1, u2))
		print()
		
		# 各発話をMeCabで分割しておく
		self.pair_data_mecab = []
		for d in self.pair_data:
			u1 = self.parse_mecab(d[0])
			u2 = d[1]
			self.pair_data_mecab.append([u1, u2])
		
		#
		# Bag-of-Wordsのための処理
		#

		# 想定ユーザ発話を用いてBag-of-Words表現を作成する
		# 学習データの想定ユーザ発話の単語を語彙（カバーする単語）とする
		self.word_list = {}

		for each_pair in self.pair_data_mecab:
			for word in each_pair[0]:
				self.word_list[word] = 1

		print('bag-of-wordsの語彙')
		print(self.word_list.keys())

		# 単語とそのインデクスを作成する
		self.word_index = {}
		for idx, word in enumerate(self.word_list.keys()):
			self.word_index[word] = idx

		print('bag-of-wordsの語彙と単語インデクス')
		print(self.word_index)

		# ベクトルの次元数（未知語を扱うためにプラス１）
		self.vec_len = len(self.word_list.keys()) + 1
		print('bag-fo-wordsの次元数 = %d' % self.vec_len)
		print()

		#
		# Word2vecのための処理
		#

		# 学習済みWord2vecファイルを読み込む
		model_filename = './data/entity_vector.model.bin'
		self.model_w2v = KeyedVectors.load_word2vec_format(model_filename, binary=True)

		# 単語ベクトルの次元数
		print('word2vecの次元数 = %d' % self.model_w2v.vector_size)
		print()
	
	# 各発話をMeCabで分割しておき、名詞・形容詞・動詞・感動詞のみを扱う
	def parse_mecab(self, sentence):
		
		m = MeCab.Tagger ("")
		d_list = m.parse(sentence).strip().split('\n')
		
		u = []
		for d in d_list:
			
			if d.strip() == 'EOS':
				break
			
			word = d.split('\t')[0]
			pos = d.split('\t')[1].split(',')[0]
			
			if pos in ['名詞', '形容詞', '動詞', '感動詞']:
				u.append(word)
		
		return u


	# 単語の系列とBag-of-Words表現を作成するための情報を受け取りベクトルを返す関数を定義
	# ※言語理解のときと同じ関数
	def make_bag_of_words(self, words):

		vec = [0] * self.vec_len
		pos_unk = self.vec_len-1
		for w in words:

			# 未知語
			if w not in self.word_index:
				vec[pos_unk] = 1
			
			# 学習データに含まれる単語
			else:
				vec[self.word_index[w]] = 1
		
		return vec

	# 類似度計算
	# 入力：ユーザ発話の単語の系列
	# 出力：入力ユーザ発話に最も類似するシステム応答
	def matching_bagofwords(self, input_data_mecab):
		
		# コサイン類似度が最も高いものを採用
		cos_dist_max = 0.
		response = None
		
		# 用例毎に処理
		for pair_each in self.pair_data_mecab:
			
			# Bag-of-Words表現に変換
			v1 = np.array(self.make_bag_of_words(input_data_mecab))
			v2 = np.array(self.make_bag_of_words(pair_each[0]))
			
			# コサイン類似度を計算
			cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
			if cos_dist_max < cos_sim:
				cos_dist_max = cos_sim
				response = pair_each[1]
		
		return ''.join(response), cos_dist_max

	# Word2vecで特徴量を作成する関数を定義
	# ここでは文内の各単語のWord2vecを足し合わせたものを文ベクトルととして利用する
	# ※言語理解のときと同じ関数
	def make_sentence_vec_with_w2v(self, words):

		sentence_vec = np.zeros(self.model_w2v.vector_size)
		num_valid_word = 0
		for w in words:
			if w in self.model_w2v:
				sentence_vec += self.model_w2v[w]
				num_valid_word += 1
		
		# 有効な単語数で割
		sentence_vec /= num_valid_word
		return sentence_vec
	
	# 類似度計算（Word2vec版）
	# 入力：ユーザ発話の単語の系列と用例データ
	# 出力：入力ユーザ発話に最も類似するシステム応答
	def matching_word2vec(self, input_data_mecab):
		
		# コサイン類似度が最も高いものを採用
		cos_dist_max = 0.
		response = None
		
		# 用例毎に処理
		for pair_each in self.pair_data_mecab:
			
			# Bag-of-Words表現に変換
			v1 = self.make_sentence_vec_with_w2v(input_data_mecab)
			v2 = self.make_sentence_vec_with_w2v(pair_each[0])
			
			# コサイン類似度を計算
			cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
			if cos_dist_max < cos_sim:
				cos_dist_max = cos_sim
				response = pair_each[1]
		
		return ''.join(response), cos_dist_max


if __name__ == '__main__':

	exampleBased = ExampleBased()
	m = MeCab.Tagger ("-Owakati")

	# 入力発話
	input_data = '趣味は何ですか'
	input_data_mecab = exampleBased.parse_mecab(input_data)

	print('Bag-fo-Words')
	response, cos_dist_max = exampleBased.matching_bagofwords(input_data_mecab)

	print('入力：%s' % input_data)
	print('応答：%s' % response)
	print('類似度：%s' % cos_dist_max)
	print()

	print('Word2vec')
	response, cos_dist_max = exampleBased.matching_word2vec(input_data_mecab)

	print('入力：%s' % input_data)
	print('応答：%s' % response)
	print('類似度：%s' % cos_dist_max)
