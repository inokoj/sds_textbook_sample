from __future__ import division

import re

#
# ルールベースの言語理解を行うクラス
#

class SluRule(object):
	
	# 文法
	grammar = []
	grammar_extract = {}

	# 意味・格フレーム
	frames = []

	# 初期化
	def __init__(self):

		self.def_grammar()
		self.def_frame()

	
	# 文法を定義
	def def_grammar(self):
		
		# 要素の列挙
		place = '(京都|今出川)'
		genre = '(ラーメン|イタリアン|そば|そば屋)'
		tellme = '(教えてください|教えて|教えてほしい)'
		near = '(近く|辺り)'
		there = '(ありますか|ありませんか)'
		name = '(味亭|割烹井上)'

		time_open = '営業時間'
		time_from = '何時から'
		time_until = '何時まで'
		time_from_until = '(' + time_from + '|' + time_until + ')'

		# 文法１（レストラン検索）
		grammar1_1 = place + 'の(おいしい|美味しい)' + genre + 'を' + tellme
		grammar1_2 = place + 'の' + near + 'で' + genre + 'は' + there
		grammar1_3 = near + 'に(おいしい|美味しい)' + genre + 'は' + there

		# 文法２（営業時間検索）
		grammar2_1 = name + 'の' + time_open + 'を' + tellme
		grammar2_2 = name + 'は' + time_from_until + '(ですか|開いていますか)'
		
		# ユーザの意図と対応させる
		self.grammars = [
			['find', grammar1_1],
			['find', grammar1_2],
			['time', grammar2_1],
			['time', grammar2_2]
		]

		# 抜き出す要素を定義
		self.grammar_extract = {
			
			# 文法１
			'find': [
				['place', place],
				['genre', genre],
			],
			
			# 文法２
			'time': [
				['name', name],
				['open', time_open],
				['from', time_from],
				['until', time_until],
			]
		}
	
	# 格フレームを定義
	def def_frame(self):
		
		# 意味フレームの列挙
		place = '(京都|今出川|烏丸御池|百万遍)'
		genre = '(ラーメン|イタリアン|そば|中華|タイ料理)'
		budget = '(1000|2000|3000)円'
		name = '(味亭|割烹井上)'
		time_open = '営業時間'
		time_from = '何時から'
		time_until = '何時まで'

		# 格フレームの意味と対応させる
		# ここにユーザ意図の種類を記述しておくことも可能
		self.frames = [
			['place', place],
			['genre', genre],
			['name', name],
			['budget', budget],
			['time_open', time_open],
			['time_from', time_from],
			['time_until', time_until]
		]
	
	# 入力文に対して文法を用いてパージングする
	# 戻り値は，マッチした文法の意図名と意図名，スロット名，スロット値のリスト
	def parse_grammar(self, input_sentence):

		results = []
		matched_grammer = None

		for grammar in self.grammars:
			
			result = re.match(grammar[1], input_sentence)
			
			if result is not None:
				
				matched_grammer = grammar[0]

				# 文法にマッチしたら要素を抜き出す
				intent = matched_grammer
				for extract_pattern in self.grammar_extract[intent]:
					
					slot_name = extract_pattern[0]
					rule = extract_pattern[1]
					
					# 要素抽出を試みる
					result2 = re.search(extract_pattern[1], input_sentence)
					if result2 is not None:
						slot_value = result2.group()
					
						# 意図名、スロット名、スロット値を追加
						results.append({'intent': intent, 'slot_name': slot_name, 'slot_value': slot_value})

		return matched_grammer, results

	# 入力文に対して意味・格フレームを用いてパージングする
	# 戻り値は，マッチしたスロット名とスロット値のリスト
	def parse_frame(self, input_sentence):
		
		results = []

		for frame in self.frames:
			
			result = re.search(frame[1], input_sentence)
			
			if result is not None:
				
				# マッチしたスロット名，スロット値を取得・格納
				intent = None
				slot_name = frame[0]
				slot_value = result.group()
				results.append({'intent': intent, 'slot_name': slot_name, 'slot_value': slot_value})
		
		return results

if __name__ == '__main__':

	# 入力データを読み込む

	with open('./data/slu-sample1.txt', 'r', encoding='utf-8') as f:
		lines = f.readlines()

	list_input_data = []
	for line in lines:
		if not line.strip():
			continue
		list_input_data.append(line.strip())
	
	parser = SluRule()

	# 入力文をマッチさせてみる
	for data in list_input_data:

		print('-----------------------')
		print('入力：' + data)
		
		# 文法
		intent, results = parser.parse_grammar(data)
		print(results)
		print('[Grammar]')
		for r in results:
			print(r['intent'] + ' : ' + r['slot_name'] + ' : ' + r['slot_value'])
		if len(results) == 0:
			print('Nothing was matched')
		print()

		# 意味・格フレーム
		results = parser.parse_frame(data)
		print('[Semantic/Case frame]')
		for r in results:
			print(r['slot_name'] + ' : ' + r['slot_value'])
		if len(results) == 0:
			print('Nothing was matched')
		print()

