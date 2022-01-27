# WebAuthn APIサンプル
[python-fido2](https://github.com/Yubico/python-fido2)を利用したWebAuthn APIのサンプルです。  
動作確認用に作成したのでDBは使用せず、ユーザー管理はJSONで行っています。  
トランザクション管理などはできないので実際に利用する場合はDB管理することをお勧めします。  

## 事前準備
1. パッケージをインストール
```
pip install fido2
pip install pyOpenSSL
```

2. settins.jsonを編集
```
{
  "server_name": "your_server_name"  // ←ここにホスト名を入力(DNS設定されていればホスト名でなくても可)
}
```

3. SSL証明書を作成
```
python createCert.py
```

## 実行方法（ローカル開発環境）
1. APIを起動
```
python root.py
```

2. 登録ページにアクセス
```
https://[your_server_name]/register
```
※\[your_server_name\]は1で設定したサーバー名を設定

3. ログインページにアクセス
```
https://[your_server_name]/register
```
※\[your_server_name\]は1で設定したサーバー名を設定

## 注意事項
1. WebAuthn APIはSSL通信環境下でないと動作しないようです。動作確認時は必ず上記事前準備手順を実行してください。
2. 冒頭にも記載していますが、実際に利用する場合はDB管理することをお勧めします。

## 参考サイト等
https://techblog.yahoo.co.jp/advent-calendar-2018/webauthn/  
https://engineering.mercari.com/blog/entry/2019-06-04-120000/  
https://github.com/Yubico/python-fido2  
https://github.com/paroga/cbor-js  
