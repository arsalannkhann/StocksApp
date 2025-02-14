import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class Llama2Model:
    def __init__(self, model_name="meta-llama/Llama-2-7b"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_prediction(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors="pt")
        output = self.model.generate(**inputs, max_length=100)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)