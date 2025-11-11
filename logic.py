# logic.py
import fitz  # PyMuPDF
import nltk
import spacy
import string
from collections import Counter
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# ==============================
# INITIAL SETUP
# ==============================
# Ensure required tokenizer data is available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")

# ==============================
# 1. EXTRACT TEXT FROM PDF
# ==============================
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ==============================
# 2. PREPROCESS TEXT
# ==============================
def preprocess_text(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    filtered_words = [w for w in words if w.isalpha() and w not in stop_words]
    return filtered_words

# ==============================
# 3. SUMMARIZATION
# ==============================
def summarize_text(text, num_sentences=5):
    sentences = sent_tokenize(text)
    words = preprocess_text(text)
    freq = nltk.FreqDist(words)

    scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in freq:
                scores[sent] = scores.get(sent, 0) + freq[word]

    summary = nlargest(num_sentences, scores, key=scores.get)
    return " ".join(summary)

# ==============================
# 4. INSIGHT EXTRACTION
# ==============================
def extract_insights(text):
    doc = nlp(text)
    entity_labels = [ent.label_ for ent in doc.ents]
    most_common = Counter(entity_labels).most_common(3)

    suggestions = []
    if "ORG" in entity_labels:
        suggestions.append("This document involves organizations — consider analyzing relationships between them.")
    if "DATE" in entity_labels:
        suggestions.append("Dates are mentioned — explore event timelines.")
    if "GPE" in entity_labels:
        suggestions.append("Contains geographical data — consider mapping or location-based insights.")
    if not suggestions:
        suggestions.append("General informative document — extract keywords for deeper insights.")

    return most_common, suggestions

# ==============================
# 5. CONTEXT-AWARE SUMMARIZATION
# ==============================
def summarize_based_on_input(text, user_query):
    sentences = sent_tokenize(text)
    filtered = [s for s in sentences if user_query.lower() in s.lower()]
    if len(filtered) < 3:
        filtered = sentences[:5]
    return " ".join(filtered)
