# 导入所需的库和模块
from flask import Flask, request, jsonify
from modelscope import (  # 从modelscope库中导入snapshot_download、AutoModelForCausalLM、AutoTokenizer和GenerationConfig
   snapshot_download,
   AutoModelForCausalLM,
   AutoTokenizer,
   GenerationConfig,
)
import torch

# 创建Flask应用实例
app = Flask(__name__)

# 设置模型ID、修订版本和模型目录
model_id = 'qwen/Qwen-VL-Chat'
revision = 'v1.1.0'
model_dir = snapshot_download(model_id, revision=revision)
torch.manual_seed(1234)

# 从模型目录中加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, fp16=True).eval()
model.generation_config = GenerationConfig.from_pretrained(model_dir, trust_remote_code=True)

# 初始化聊天历史记录
history = None

# 定义'/chat'接口，接受POST请求并返回响应
@app.route('/chat', methods=['POST'])
def chat():
   global history
   # 从请求中获取图像上下文和文本输入
   data = request.json
   image_context = data.get('image_context', {})
   text_input = data.get('text', '')
   # 将图像上下文和文本输入转换为分词器格式
   query = tokenizer.from_list_format([
       image_context,
       {'text': text_input},
   ])
   # 使用模型进行聊天，并将聊天历史记录传递给下一个接口
   response, history = model.chat(tokenizer, query=query, history=history)
   # 返回响应
   return jsonify({'response': response})

# 定义'/chat_bbox'接口，接受POST请求并返回响应和图像
@app.route('/chat_bbox', methods=['POST'])
def chat_bbox():
   global history
   # 从请求中获取文本输入
   text_input = request.json.get('text', '')
   # 使用模型进行聊天，并将聊天历史记录传递给下一个接口
   response, history = model.chat(tokenizer, text_input, history=history)
   # 在响应中添加图像路径
   image = tokenizer.draw_bbox_on_latest_picture(response, history)
   image_path = 'output_chat.jpg'
   image.save(image_path)
   # 返回响应和图像路径
   return jsonify({'response': response, 'image_url': image_path})

# 启动Flask应用，监听来自任何IP地址和端口的请求
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)



#readme
# api请求例子
"""
import json
import requests

data = {
    "text": "这是什么",
    "image_context": {
        "image": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"
    }
}



response = requests.post("http://127.0.0.1:5000/chat", json=data)
response_json = response.json()
chat_response = response_json.get("response", "")
print(chat_response)

"""


# curl请求例子
"""

curl -X POST \
 -H "Content-Type: application/json" \
 -d '{
       "text": "这是什么", 
       "image_context": {
           "image": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"
       }
   }' \
 http://127.0.0.1:5000/chat
"""