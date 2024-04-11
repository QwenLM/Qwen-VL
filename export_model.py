from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer

path_to_adapter = '/home/suma/llm/demo/Qwen-VL/output_qwen'
new_model_directory = '/home/suma/llm/models/Qwen-VL-Chat-My'

tokenizer = AutoTokenizer.from_pretrained(
    path_to_adapter, # path to the output directory
    trust_remote_code=True
)
model = AutoPeftModelForCausalLM.from_pretrained(
    path_to_adapter, # path to the output directory
    device_map="auto",
    trust_remote_code=True
).eval()

#response, history = model.chat(tokenizer, "你好", history=None)

#print(response)

tokenizer.save_pretrained(new_model_directory)

merged_model = model.merge_and_unload()
# max_shard_size and safe serialization are not necessary. 
# They respectively work for sharding checkpoint and save the model to safetensors.
merged_model.save_pretrained(new_model_directory, max_shard_size="2048MB", safe_serialization=True)
