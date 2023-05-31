# 最新の環境構築方法（2022年10月18日 更新）

このファイルではサンプルプログラム（Hands-on）の実行環境について最新の情報をまとめています。  
なお、Anaconda環境、python 3.8を想定しています。

## 3章 (クラウド型音声認識の利用)

### Google Cloud Platformの登録

#### APIの有効化

1. Google Cloud Platformのウェブサイト（ https://console.cloud.google.com ）へアクセス
1. 左上のメニューから「APIとサービス」→「ライブラリ」を選択
1. 検索欄に「speech」と入力し、「Cloud Speech-to-Text API」を開き、「有効化」を選択
1. 同様の方法で、「Cloud Text-to-Speech API」（音声合成）も有効化しておく

#### 認証キーの発行

5. Google Cloud Platformのウェブサイト（ https://console.cloud.google.com ）へアクセス
1. 左上のメニューから「APIとサービス」→「認証情報」を選択
1. 上部の「認証情報を作成」→「サービスアカウント」を選択し、以下のように入力
	1. 「サービスアカウント名」→（任意）
	1. 「アカウントID」→（空白不可、サービスアカウント名を入力されると自動的に設定される）
	1. 「サービスアカウントの説明」→（任意）
1. 「作成して続行」からそのまま「完了」まで進める
1. サービスアカウント一覧から作成したサービスアカウントを選択
1. 上部の「キー」を選択し、「鍵を追加」→「新しい鍵を作成」を選択
1. キーのタイプを「JSON」とし「作成」を選択すると認証キーファイル（JSON形式）のダウンロードが開始されるので保存する。例えば、このあとに実装するプログラムと同じフィルダに置くとよい。このファイルを公開したり他人に渡したりしないこと。

### Pythonパッケージのインストール

#### pyAudio
```
conda install -c anaconda pyaudio
```  
または
```
pip install pyaudio
```

#### google-cloud-speech
~~`> conda install -c conda-forge google-cloud-speech`~~
``` 
pip install google-cloud-speech
``` 


## 4章 (言語理解の実装)

### Pythonパッケージのインストール

#### scikit-learn
```
conda install -c intel scikit-learn
```  
または
```
pip install scikit-learn
```

#### sklearn-crfsuite

~~`>conda install -c conda-forge sklearn-crfsuite`~~
  
または
~~`> pip install sklearn-crfsuite`~~
```
pip install "git+https://github.com/MeMartijn/updated-sklearn-crfsuite.git#egg=sklearn_crfsuite"
```

#### gensim
```
conda install -c conda-forge gensim
```  
または
```
pip install gensim
```

### MeCabのインストール

#### MeCab本体

64bit Windows版の配布サイト  
https://github.com/ikegami-yukino/mecab/releases

#### MeCabバインディング
~~`> conda install -c conda-forge mecab`~~  
~~`> pip install mecab`~~
```
conda install -c mzh mecab-python3
```
または
```
pip install mecab-python3
```

## 7章 (クラウド型音声合成の利用)

### Pythonパッケージのインストール


### google-cloud-texttospeech

~~`> conda install -c conda-forge google-cloud-texttospeech`~~  
```
pip install --upgrade google-cloud-texttospeech
```


### ffmpeg
```
conda install -c conda-forge ffmpeg
```

### pydub
```
conda install -c conda-forge pydub
```
または
```
pip install pydub
```

## 今後の追加予定

※以下は今後のサンプルプログラムの追加で必要となるもの。

### pytorch (CPU版)
`> conda install pytorch torchvision torchaudio cpuonly -c pytorch`  
`(pip install torch torchvision torchaudio)`

### git
`> conda install -c anaconda git`

### transformers
`> pip install transformers`

### fugashi
`> pip install fugashi`

### unidic-lite
`> pip install unidic-lite`

### bi-lstm-crf
オリジナル（ https://github.com/jidasheng/bi-lstm-crf ）に対して修正を加えたもの  
`> pip install git+https://github.com/inokoj/bi-lstm-crf.git`

### more-itertools
`> conda install -c anaconda more-itertools`  
`(> pip install more-itertools)`
