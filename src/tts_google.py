import os
from google.cloud import texttospeech

from pydub import AudioSegment
from pydub.playback import play

#
# Google Text-to-Speechを用いて音声合成を行うクラス
#
class GoogleTextToSpeech(object):

	def __init__(self, path_key='./google-credentials.json', language_code='ja-JP', tts_name='ja-JP-Wavenet-C', pitch=0.0):
		
		# APIのパラメータ
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_key

		# クライアントの初期化
		self._client = texttospeech.TextToSpeechClient()

		# 音声合成のパラメータを設定
		self._voice = texttospeech.VoiceSelectionParams(
			language_code = language_code,
			name = tts_name
		)

		# 音声の設定
		self._audio_config = texttospeech.AudioConfig(
			audio_encoding = texttospeech.AudioEncoding.MP3,
			pitch = pitch
		)
	
	# 音声合成
	def generate(self, text, filename='./data/tts-temp.mp3'):

		# 音声合成を実行
		synthesis_input = texttospeech.SynthesisInput(text=text)
		response = self._client.synthesize_speech(input=synthesis_input, voice=self._voice, audio_config=self._audio_config)

		# 合成したデータをmp3ファイルとして書き出し
		with open(filename, 'wb') as out:
			out.write(response.audio_content)

	# 合成音声の再生
	def play(self, filename='./data/tts-temp.mp3'):
		audio_data = AudioSegment.from_mp3(filename)
		play(audio_data)

if __name__ == '__main__':
	
	tts = GoogleTextToSpeech()
	tts.generate('京都大学へようこそ。')
	tts.play()
