# FAQ

## インストールと環境

#### transformers のバージョンは？

4.31.0 が望ましいです。

#### コードとチェックポイントをダウンロードしましたが、モデルをローカルにロードできません。どうすればよいでしょうか？

コードを最新のものに更新し、すべてのシャードされたチェックポイントファイルを正しくダウンロードしたかどうか確認してください。

#### `qwen.tiktoken` が見つかりません。これは何ですか？

これは tokenizer のマージファイルです。ダウンロードする必要があります。[git-lfs](https://git-lfs.com) を使わずにリポジトリを git clone しただけでは、このファイルをダウンロードできないことに注意してください。

#### transformers_stream_generator/tiktoken/accelerate が見つかりません。

コマンド `pip install -r requirements.txt` を実行してください。このファイルは [https://github.com/QwenLM/Qwen-VL/blob/main/requirements.txt](https://github.com/QwenLM/Qwen-VL/blob/main/requirements.txt) にあります。
<br><br>



## デモと推論

#### デモはありますか？

ウェブデモは `web_demo_mm.py` を参照してください。詳細は README を参照してください。



#### Qwen-VLはストリーミングに対応していますか？

いいえ、まだサポートしていません。

#### 世代と命令は関係ないようですが...

Qwen-VL ではなく Qwen-VL-Chat を読み込んでいないか確認してください。Qwen-VL はアライメントなしのベースモデルで、SFT/Chat モデルとは動作が異なります。

#### 量子化はサポートされていますか？

いいえ。早急に量子化をサポートするつもりです。

#### 長いシーケンスの処理で不満足なパフォーマンス

NTK が適用されていることを確認してください。`config.json` の `use_dynamc_ntk` と `use_logn_attn` を `true` に設定する必要がある（デフォルトでは `true`）。
<br><br>


## Tokenizer

#### bos_id/eos_id/pad_id が見つかりません。

私たちのトレーニングでは、セパレータとパディングトークンとして `<|endoftext|>` のみを使用しています。bos_id、eos_id、pad_id は tokenizer.eod_id に設定できます。私たちの tokenizer について詳しくは、tokenizer についてのドキュメントをご覧ください。

