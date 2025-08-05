# Demo

DCJ11 の動作を確認する小さなサンプルプログラムがこのフォルダーに登録されています。

作成したバイナリーファイルは、[PDP11GUI](https://github.com/j-hoppe/PDP11GUI)(Windows 用のみ)を使ってメモリー上にロードできます。

## aout2abs.py

GCC により作成されたバイナリーファイルを absolute loader 用紙テープイメージに変換する Python スクリプトです。

## blinky

ボードの LED を点滅させるいわゆる「L チカ」プログラムです。

## timer

電源ラインの周波数をもとにしたタイマー KW11-L を使用した「L チカ」プログラムです。interrupt を使用せず、polling でタイミングを見ています。

## interrupt

KW11-L の割込みを使用した「L チカ」プログラムです。

## interrupt_clang

interrupt と同じ KW11-L の割込みを使用した「L チカ」プログラムを C 言語で書いた例です。
