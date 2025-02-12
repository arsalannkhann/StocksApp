import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def __init__(self, model_name="meta-llama/Llama-2-7b"):
    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    self.model = AutoModelForCausalLM.from_pretrained(model_name)


def predict_stock_trend(self, news_text):
    inputs = self.tokenizer(news_text, return_tensors="pt")
    output = self.model.generate(**inputs, max_length=100)
    return self.tokenizer.decode(output[0], skip_special_tokens=True)



