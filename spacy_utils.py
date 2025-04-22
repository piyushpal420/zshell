import spacy
import numpy as np

# load once at import
nlp = spacy.load("en_core_web_sm")

def load_glove_embeddings(emb_path, emb_dim=300):
    word2vec = {}
    with open(emb_path, 'r', encoding='utf-8') as f:
        for line in f:
            vals = line.strip().split()
            word = vals[0]
            vec  = np.array(vals[1:], dtype=np.float32)
            if len(vec) == emb_dim:
                word2vec[word] = vec
    return word2vec

def sentence_embedding(tokens, word2vec, emb_dim=300):
    vecs = [word2vec[t] for t in tokens if t in word2vec]
    if not vecs:
        return np.zeros(emb_dim, dtype=np.float32)
    return np.mean(vecs, axis=0)

def tokenize_and_normalize(text, ignore_chars=['?', '.', ',', '!']):
    doc = nlp(text.lower())
    return [t.text for t in doc if t.text not in ignore_chars]

