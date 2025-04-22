# inference.py
import sys
import json
import torch
import pickle
import random
import numpy as np
import spacy
from model import NeuralNet
from spacy_utils import sentence_embedding, tokenize_and_normalize

def load_inference():
    meta = torch.load("model_and_metadata.pth", map_location="cpu")
    model = NeuralNet(meta["emb_size"], meta["hidden_size"], meta["num_classes"])
    model.load_state_dict(meta["model_state"])
    model.eval()
    with open("glove_embeddings.pkl", "rb") as f:
        glove = pickle.load(f)
    tags = meta["tags"]
    return model, glove, tags

model, glove, tags = load_inference()
nlp = spacy.load("en_core_web_sm")

if len(sys.argv) < 2:
    print("🤖 [AI ERROR: No input]")
    sys.exit(1)

text = sys.argv[1].strip().strip('"').strip("'")
tokens = tokenize_and_normalize(text)
vec = sentence_embedding(tokens, glove, emb_dim=len(glove[next(iter(glove))]))
X = torch.from_numpy(vec).float().unsqueeze(0)

with torch.no_grad():
    out = model(X)
    probs = torch.softmax(out, dim=1)
    idx = probs.argmax(dim=1).item()
    confidence = probs[0][idx].item()
    tag = tags[idx]

with open("trainingDataset.json", "r") as f:
    intents = json.load(f)["intents"]

THRESH = 0.4
if confidence > THRESH:
    intent = next((i for i in intents if i["tag"] == tag), None)
    if intent and intent.get("responses"):
        print(random.choice(intent["responses"]))
    else:
        print(f"Oops, I recognized '{tag}' but have no response configured.")
else:
    print("Sorry, I’m not confident. Try rephrasing your query.")

