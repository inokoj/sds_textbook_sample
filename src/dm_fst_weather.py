from __future__ import division

import sys, os

#
# 有限オートマトンによる対話管理を行うクラス（天気案内）
#

class DmFst(object):
	
	# 現在の状態番号
	current_state = -1

	# 初期状態
	start_state = -1
	
	# 遷移条件にマッチしたユーザ発話を保持する
	context_user_utterance = []

	# 終了状態に達したかどうか
	end = False

	# 初期化
	def __init__(self):

		self.def_fst()
		self.reset()
		self.end = False

	# 有限オートマトンを定義
	def def_fst(self):
		
		# 状態の定義

		# 状態番号、対応するシステム発話
		self.states = [
			[0, 'こんにちは。天気案内システムです。どの地域の天気を聞きたいですか。'],
			[1, 'いつの天気を聞きたいですか。'],
			[2, 'ご案内します。'],
			[3, '地域名を「京都」のようにおっしゃってください。'],
			[4, '「今日」や「明日」のようにおっしゃってください。']
		]

		# 初期状態番号
		self.start_state = 0

		# 終了状態番号
		self.end_state = 2

		# 遷移の定義

		# 遷移元状態番号、遷移先状態番号、遷移条件（スロット名）
		self.transitions = [
			[0, 1, 'place'],
			[0, 3, None],
			[1, 2, 'when'],
			[1, 4, None],
			[3, 1, 'place'],
			[3, 3, None],
			[4, 2, 'when'],
			[4, 4, None]
		]

	# 入力であるユーザ発話に応じてシステム発話を出力し、内部状態を遷移させる
	# ただし、ユーザ発話の情報は「意図、フレーム名、フレーム値」のlistとする
	def enter(self, user_utterance):

		# フレーム名に対して行う
		# 最初の0番目のindexは1発話に対して複数のスロットが抽出された場合に対応するため
		# ここでは1発話につき１つのフレームしか含まれないという前提
		input_slot_name = None
		input_slot_value = None

		for u in user_utterance:
			input_slot_name = u['slot_name']
			input_slot_value = u['slot_value']
		
		system_utterance = ""
		
		# 現在の状態からの遷移に対して入力がマッチするか検索
		for trans in self.transitions:
			
			# 条件の遷移元が現在の状態か
			if trans[0] == self.current_state:
				
				# 無条件に遷移
				if trans[2] is None:
					self.current_state = trans[1]
					system_utterance = self.get_system_utterance()
					break
				
				# 条件にマッチすれば遷移
				if trans[2] == input_slot_name:
					self.context_user_utterance.append([input_slot_name, input_slot_value])
					self.current_state = trans[1]
					system_utterance = self.get_system_utterance()
					break
		
		# 修了状態に達したら
		if self.current_state == self.end_state:
			self.end = True
		
		return system_utterance

	# 初期状態にリセットする
	def reset(self):

		self.current_state = self.start_state
		self.context_user_utterance = []
		self.end = False

	# 指定された状態に対応するシステムの発話を取得
	def get_system_utterance(self):
		
		utterance = ""
		
		for state_ in self.states:
			if self.current_state == state_[0]:
				utterance = state_[1]
		
		return utterance

if __name__ == '__main__':

	dm = DmFst()

	# 初期状態の発話を表示
	print('システム発話 : ' + dm.get_system_utterance())	

	# ユーザ発話を設定
	user_utterance = [{'slot_name': 'place', 'slot_value': '京都'}]
	print('ユーザ発話')
	print(user_utterance)
	print()

	# 次のシステム発話を表示
	print('システム発話')
	print(dm.enter(user_utterance))

	# 誤った発話を入力してみる

	# ユーザ発話を設定
	user_utterance = [{'slot_name': 'place', 'slot_value': '新宿'}]
	print('ユーザ発話')
	print(user_utterance)
	print()

	# 次のシステム発話を表示
	print('システム発話')
	print(dm.enter(user_utterance))

	# ユーザ発話を設定
	user_utterance = [{'slot_name': 'when', 'slot_value': '明日'}]
	print('ユーザ発話')
	print(user_utterance)
	print()

	# 次のシステム発話を表示
	print('システム発話')
	print(dm.enter(user_utterance))
