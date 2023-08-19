# ＴＦＴ1.77表示器とＳＷ２個、ＬＥＤ２個を実装したラズパイ汎用ＵＩ基板

<h4><<概要>></h4>
　ＴＦＴ1.77表示器とスイッチ２個、ＬＥＤ２個を実装したテスト用のラズパイ専用基板です。 <br>
　ブレッドボードで何か作ろうとしたときに、最低限のＵＩが必要ですが、それらもブレッドボード上に作るのは面倒です。 <br>
　最低限のＵＩを備えたこの基板があれば、作るべき物だけに集中できるので、作業がはかどります。 <br>
　すべてのソースプログラムを開示いたします。 <br>

・LEDの色等指定はできません。<br>
・部品の仕様が変わる場合があります。 <br>
・基板のバージョンが変わる場合がありますが、機能等に違いはありません。<br>
・ラズパイは付属しません。<br>

<h4><<使用方法>></h4>
git clone https://github.com/momorara/tft177 <br>
でラズパイにダウンロードしてください。<br>
インストールについては、インストール文書に従いインストールを行ってください。<br>
本基板にはブレッドボードと繋ぎやすいように、連結ピンを装着しています。
説明写真のような使い方ができます。<br>

<h4><<使用説明資料>></h4>
説明書類の中の資料を確認ください。
お問い合わせに関しては、サポート.txtを参照ください。><br>

<h4><<動作環境>>></h4>
2023/8/4 対応OS：Buster版、Bullseye版(〜11.7)での動作を確認しています。<br>

<h4><<ライセンス>></h4>
使用しているライブラリについては、ライブラリ制作者のライセンス規定を参照ください。 <br>
オリジナル部分については、オープソースとさせていただきます。 <br>
Released under the MIT license です。 <br>
プログラム自体はサンプルプログラムです。 <br>

<h4><<サポート情報>>></h4>
2022/10/10
lcd177.pyのinit('reset’)にバグがありました。 <br>
本来は、lcd177.init('reset') とすれば、画面が消去され、カーソルが原点に戻るはずでした。 <br>
しかし、この機能が動作していませんでした。 <br>
こちらの不手際で、大変ご迷惑をおかけしました。 <br>
改修したプログラムをアップロードしましたので、こちらに入れ替えて試してみてください。 <br>
よろしくお願いします。
