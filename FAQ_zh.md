# FAQ

## 安装&环境

#### 我应该用哪个transformers版本？

建议使用4.31.0。

#### 我把模型和代码下到本地，按照教程无法使用，该怎么办？

答：别着急，先检查你的代码是不是更新到最新版本，然后确认你是否完整地将模型checkpoint下到本地。

#### `qwen.tiktoken`这个文件找不到，怎么办？

这个是我们的tokenizer的merge文件，你必须下载它才能使用我们的tokenizer。注意，如果你使用git clone却没有使用git-lfs，这个文件不会被下载。如果你不了解git-lfs，可点击[官网](https://git-lfs.com/)了解。

#### transformers_stream_generator/tiktoken/accelerate，这几个库提示找不到，怎么办？

运行如下命令：`pip install -r requirements.txt`。相关依赖库在[https://github.com/QwenLM/Qwen-VL/blob/main/requirements.txt](https://github.com/QwenLM/Qwen-VL/blob/main/requirements.txt) 可以找到。
<br><br>


## Demo & 推理

#### 是否提供Demo？

`web_demo_mm.py`提供了Web UI。请查看README相关内容了解更多。

#### Qwen-VL支持流式推理吗？

Qwen-VL当前不支持流式推理。

#### 模型的输出看起来与输入无关/没有遵循指令/看起来呆呆的

请检查是否加载的是Qwen-VL-Chat模型进行推理，Qwen-VL模型是未经align的预训练基模型，不期望具备响应用户指令的能力。我们在模型最新版本已经对`chat`接口内进行了检查，避免您误将预训练模型作为SFT/Chat模型使用。

#### 是否有量化版本模型

目前Qwen-VL不支持量化，后续我们将支持高效的量化推理实现。

#### 处理长序列时效果有问题

请确认是否开启ntk。若要启用这些技巧，请将`config.json`里的`use_dynamc_ntk`和`use_logn_attn`设置为`true`。最新代码默认为`true`。
<br><br>


## Tokenizer

#### bos_id/eos_id/pad_id，这些token id不存在，为什么？

在训练过程中，我们仅使用<|endoftext|>这一token作为sample/document之间的分隔符及padding位置占位符，你可以将bos_id, eos_id, pad_id均指向tokenizer.eod_id。请阅读我们关于tokenizer的文档，了解如何设置这些id。

