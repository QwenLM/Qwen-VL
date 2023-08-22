# FAQ

## Installation & Environment

#### Which version of transformers should I use?

4.31.0 is preferred.

#### I downloaded the codes and checkpoints but I can't load the model locally. What should I do?

Please check if you have updated the code to the latest, and correctly downloaded all the sharded checkpoint files.

#### `qwen.tiktoken` is not found. What is it?

This is the merge file of the tokenizer. You have to download it. Note that if you just git clone the repo without [git-lfs](https://git-lfs.com), you cannot download this file.

#### transformers_stream_generator/tiktoken/accelerate not found

Run the command `pip install -r requirements.txt`. You can find the file at [https://github.com/QwenLM/Qwen-VL/blob/main/requirements.txt](https://github.com/QwenLM/Qwen-VL/blob/main/requirements.txt).
<br><br>



## Demo & Inference

#### Is there any demo?

Yes, see `web_demo_mm.py` for web demo. See README for more information.



#### Can Qwen-VL support streaming?

No. We do not support streaming yet.

#### It seems that the generation is not related to the instruction...

Please check if you are loading Qwen-VL-Chat instead of Qwen-VL. Qwen-VL is the base model without alignment, which behaves differently from the SFT/Chat model.

#### Is quantization supported?

No. We would support quantization asap.

#### Unsatisfactory performance in processing long sequences

Please ensure that NTK is applied. `use_dynamc_ntk` and `use_logn_attn` in `config.json` should be set to `true` (`true` by default).
<br><br>


## Tokenizer

#### bos_id/eos_id/pad_id not found

In our training, we only use `<|endoftext|>` as the separator and padding token. You can set bos_id, eos_id, and pad_id to tokenizer.eod_id. Learn more about our tokenizer from our documents about the tokenizer.

