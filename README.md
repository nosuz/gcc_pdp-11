# GCC C compiler for PDP-11

PDP-11用のGCC C compilerのDev Containerです。

## Demos

サンプルプログラムが`demo`ディレクトリーにあります。

## Git

editor が設定されていないため、コマンドラインから`git commit --amend`など編集が必要な操作ができません。そこで、`.git/config`に`editor`の設定を加えます。

```
[core]
 editor = code --wait
```

ローカルの`~/.gitconfig`に設定がある場合は、デフォルト設定ではこのファイルがコピーされるのでコンテナ毎の設定は不要です。

## 参考

- [PDP 11 GCC Cross Compiler](https://github.com/hoglet67/PiTubeDirect/wiki/PDP-11-GCC-Cross-Compiler)
