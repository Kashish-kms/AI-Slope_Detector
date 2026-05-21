import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, GPT2LMHeadModel, GPT2Tokenizer
import numpy as np

class AIDetector:
    def __init__(self, config):
        # Main Detector
        self.tokenizer = AutoTokenizer.from_pretrained(config.DETECTOR_MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(config.DETECTOR_MODEL)
        
        # Perplexity Model (GPT-2)
        self.ppl_tokenizer = GPT2Tokenizer.from_pretrained(config.PPL_MODEL)
        self.ppl_model = GPT2LMHeadModel.from_pretrained(config.PPL_MODEL)

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        
        probs = torch.softmax(logits, dim=1).numpy()[0]
        # Label 0: Real, Label 1: Fake
        return {"human": float(probs[0]), "ai": float(probs[1])}

    def calculate_perplexity(self, text):
        # AI text usually has LOWER perplexity (more predictable)
        encodings = self.ppl_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        input_ids = encodings.input_ids
        with torch.no_grad():
            outputs = self.ppl_model(input_ids, labels=input_ids)
            loss = outputs.loss
        return torch.exp(loss).item()