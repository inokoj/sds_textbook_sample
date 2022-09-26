# 音声対話システム －基礎から実装まで－
このページは『音声対話システム －基礎から実装まで－』（オーム社, 2022年10月15日 発売）のサポートサイトです。

<img src="https://user-images.githubusercontent.com/31427099/192208284-5c1e25a6-2188-401d-a234-8409f84d04cd.jpg" width="30%">

* * *
## 書籍情報

- オーム社（目次などの詳細はこちら）
　https://www.ohmsha.co.jp/book/9784274229541/
- Amazon
　https://www.amazon.co.jp/dp/4274229548/
- honto
　https://honto.jp/netstore/search.html?k=978-4-274-22954-1&srchf=1
- 紀伊国屋書店
　https://www.kinokuniya.co.jp/f/dsg-01-9784274229541

## サンプルソースコード（Hands-on）

Hands-onとして紹介したソースコードのリンクは以下の通りです。また、書籍に掲載しきれなかった実装についてもこちらで随時追加・更新しています。

### 3章（クラウド型音声認識の利用）

- [音声認識（ストリーミング型）](src/asr_google_streaming.ipynb)
- [音声認識（ストリーミング型・発話区間検出有り）](src/asr_google_streaming_vad.ipynb)

### 4章（言語理解の実装）

- [言語理解（ルールによる方法）](src/slu_rule.ipynb)
- [言語理解（機械学習による方法：ドメイン推定）](src/slu_ml_domain.ipynb)
- [言語理解（機械学習による方法：スロット値推定）](src/slu_ml_slot.ipynb)

### 5章（対話管理の実装）

- [対話管理（有限オートマトンによる方法）](src/dm_fst.ipynb)
- [対話管理（フレームによる方法）](src/dm_frame.ipynb)

### 6章（用例ベースの実装）

- [用例ベース](src/example_based.ipynb)

### 7章（クラウド型音声合成の利用）

- [音声合成](src/tts_google.ipynb)

### 8章（システム統合）

- [システム統合１（有限オートマトン）](src/system1.ipynb)
- [システム統合２（フレーム）](src/system2.ipynb)
- [システム統合３（フレーム＋機械学習言語理解）](src/system3.ipynb)
- [システム統合４（有限オートマトン＋機械学習言語理解）](src/system4.ipynb)
- [システム統合５（用例ベース）](src/system5.ipynb)

* * *
## 連絡先
本書の内容に関するご質問、誤りなどのご指摘は下記までお願いします。

京都大学　井上 昂治<br>
<img width="200" alt="email" src="https://user-images.githubusercontent.com/31427099/192209972-6a6038fb-94c7-450e-83ff-6bc94639ab41.png">
