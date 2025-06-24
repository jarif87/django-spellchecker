from django.core.cache import cache
import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

vocab_cache_key = 'vocab_cache'
probs_cache_key = 'probs_cache'

vocab = cache.get(vocab_cache_key)
probs = cache.get(probs_cache_key)

if vocab is None or probs is None:
    vocab_path = os.path.join(BASE_DIR, 'vocab.pkl')
    probs_path = os.path.join(BASE_DIR, 'word_probability.pkl')

    with open(vocab_path, 'rb') as f:
        vocab = pickle.load(f)
    cache.set(vocab_cache_key, vocab, None)

    with open(probs_path, 'rb') as f:
        probs = pickle.load(f)
    cache.set(probs_cache_key, probs, None)
