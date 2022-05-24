import os
import numpy as np
import math
import struct

# Google音声認識を使用するためのライブラリ
from google.cloud import speech

# マイク入力のライブラリ
import pyaudio

# 入力音声データを保持するデータキュー
from six.moves import queue

#
# Google Streaming ASRを用いて音声認識を行うクラス群
#

#
# 音声入力を行うためのクラス
# 音声区間を検出し、発話が終了すると音声入力も終了する
#
class MicrophoneStream(object):
	
	# 音声入力ストリームを初期化する
	# マイク入力のサンプリングレートと音声データを受け取る単位（サンプル数）を指定する
	def __init__(self, rate, chunk):
		
		# マイク入力のパラメータ
		self.rate = rate		# サンプリングレート
		self.chunk = chunk		# 音声データを受け取る単位（サンプル数）
		
		# 入力された音声データを保持するデータキュー
		self.buff = queue.Queue()
		
		# pyaudioの初期化
		self.audio_interface = pyaudio.PyAudio()
		
		# マイク音声入力の設定と開始
		self.audio_stream = self.audio_interface.open(
			format = pyaudio.paInt16,			# 音声データの形式
			channels = 1,						# チャネル数
			rate = rate,						# サンプリングレート
			input = True,						# 音声入力として使用
			frames_per_buffer = self.chunk,		# 音声データを受け取る単位
			stream_callback = self.callback		# 音声データを受け取る度に呼び出される関数
		)

		# 音声ストリームを開始したのでフラグをオフに
		self.closed = False
	
	# 音声入力の度に呼び出される関数
	# 同時に音声パワーに基づいて音声区間を判定
	# 引数は pyaudio の仕様に合わせたもの
	def callback(self, in_data, frame_count, time_info, status_flags):
		
		# 入力された音声データをキューへ保存
		self.buff.put(in_data)
		
		# 次のフレームの入力を受け取るために必要
		return None, pyaudio.paContinue
	
	# 音声認識を行うクラスが音声データを取得するための関数
	def generator(self):

		# 音声ストリームが開いている間は処理を行う
		while not self.closed:
			
			# キューに保存されているデータを全て取り出す
			
			# 先頭のデータを取得
			chunk = self.buff.get()
			if chunk is None:
				return
			data = [chunk]

			# まだキューにデータが残っていれば全て取得する
			while True:
				try:
					chunk = self.buff.get(block=False)
					if chunk is None:
						return
					data.append(chunk)
				except queue.Empty:
					break
			
			# yieldにすることでキューのデータを随時取得できるようにする
			yield b''.join(data)

	# 終了時の処理
	# 音声認識を終了したいときにはこの関数を呼び出す
	def exit(self):

		# 音声ストリームを終了
		self.audio_stream.stop_stream()
		self.audio_stream.close()
		
		# 終了フラグ
		self.closed = True

		# キューへNoneを追加
		self.buff.put(None)
		
		# pyAudioを終了
		self.audio_interface.terminate()

#
# Google音声認識を行うためのクラス
# マイク入力のためのクラスのインスタンスを受け取る
#
class GoogleStreamingASR(object):

	# 音声認識インタフェースを初期化
	# サンプリングレートとマイク入力のためのクラスのインスタンスを受け取る
	def __init__(self, rate, microphone_stream):
		
		# Google音声認識APIを使用するための認証キーの設定
		path_key = './google-credentials.json'		# 認証キーのファイルパスを指定する
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_key

		# マイク入力のためのクラスのインスタンスを保持
		self.microphone_stream = microphone_stream

		# 音声認識クライアントの初期化
		self.client = speech.SpeechClient()

		# 音声認識の設定
		self._config = speech.RecognitionConfig(
			encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,		# 音声データの形式
			sample_rate_hertz = rate,		# サンプリングレート
			language_code = 'ja-JP'			# 言語設定
		)

		# ストリーミング音声認識の設定
		self.streaming_config = speech.StreamingRecognitionConfig(
			config=self._config,
			interim_results=True
		)

	# 音声認識結果を受信したときの処理
	def recieve_asr_result(self, responses):
		
		# responseはイテレータのため、新たな認識結果が得られる度にこのループが実行される
		for response in responses:
			
			# 認識結果が無効であれば処理しない
			if not response.results:
				continue

			result = response.results[0]
			if not result.alternatives:
				continue
			
			# 現時点での認識結果の文を取得
			result_sentence = result.alternatives[0].transcript
			
			# 音声認識の途中結果の場合
			# ストリーミング音声認識の場合に取得可能
			if not result.is_final:
				
				# 途中の認識結果を表示
				print(u'\r途中結果: ' + result_sentence, end='')
			
			# 確定した認識結果の場合
			# マイク入力を終了する
			else:
				# 認識結果データを保存
				self.final_asr_result = result
				
				# マイク入力を終了
				self.microphone_stream.exit()

	# 音声認識APIの実行して最終的な認識結果を得る
	def get_asr_result(self):

		# マイク入力に応じてストリーミング音声認識を実行
		audio_generator = self.microphone_stream.generator()
		requests = (speech.StreamingRecognizeRequest(audio_content=content)
			for content in audio_generator)
			
		# 認識されるとrecieve_asr_result関数が呼ばれる
		responses = self.client.streaming_recognize(self.streaming_config, requests)
		self.recieve_asr_result(responses)

		# 認識結果を返す
		return self.final_asr_result

if __name__ == '__main__':
	# サンプリングレートは16000Hz
	# 音声データを受け取る（処理する）単位は 1600サンプル = 0.1秒

	# マイク入力を初期化・開始
	micStream = MicrophoneStream(16000, 1600)

	# Google音声認識を使用するクラスを初期化
	asrStream = GoogleStreamingASR(16000, micStream)

	print('＜認識開始＞')
	result = asrStream.get_asr_result()

	# 認識結果を表示
	if hasattr(result, 'alternatives'):
		print()
		print('最終結果：' + result.alternatives[0].transcript)
		print('信頼度スコア(0.0 ~ 1.0)：%f' % result.alternatives[0].confidence)
