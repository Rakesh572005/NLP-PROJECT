# logic.py
import fitz  # PyMuPDF
import nltk
import spacy
import string
from collections import Counter
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

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
#extract
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text
#preprocess
def preprocess_text(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    filtered_words = [w for w in words if w.isalpha() and w not in stop_words]
    return filtered_words
#summariztion
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



def extract_insights(text):
    doc = nlp(text)

    entity_map = {
        "ORG": [],
        "PERSON": [],
        "DATE": [],
        "GPE": [],
        "CARDINAL": []
    }

    for ent in doc.ents:
        if ent.label_ in entity_map:
            entity_map[ent.label_].append(ent.text)

    for k in entity_map:
        entity_map[k] = list(dict.fromkeys(entity_map[k]))[:10]

    insights_text = ""

    if entity_map["ORG"]:
        insights_text += f"This PDF mentions organizations such as {', '.join(entity_map['ORG'])}. "
    if entity_map["PERSON"]:
        insights_text += f"It includes people like {', '.join(entity_map['PERSON'])}. "
    if entity_map["DATE"]:
        insights_text += f"Important dates found include {', '.join(entity_map['DATE'])}. "
    if entity_map["GPE"]:
        insights_text += f"Geographical locations mentioned are {', '.join(entity_map['GPE'])}. "
    if entity_map["CARDINAL"]:
        insights_text += f"Several numerical values appear, such as {', '.join(entity_map['CARDINAL'])}. "

    if insights_text == "":
        insights_text = "No significant entities (people, orgs, dates, locations) were detected in this PDF."

    suggestions = []

    if entity_map["ORG"]:
        suggestions.append("Try exploring how these organizations relate to each other in the context of the PDF.")
    if entity_map["PERSON"]:
        suggestions.append("The people mentioned may be key contributors or stakeholders.")
    if entity_map["DATE"]:
        suggestions.append("Dates could represent important events or chronological flow.")
    if entity_map["GPE"]:
        suggestions.append("The mentioned locations may provide geographical context to the document.")
    if entity_map["CARDINAL"]:
        suggestions.append("The numbers in the PDF may indicate statistics, counts, or measurements.")

    if not suggestions:
        suggestions.append("This PDF looks general—no strong insights detected.")

    return insights_text.strip(), suggestions




def summarize_based_on_input(text, user_query):
    sentences = sent_tokenize(text)
    filtered = [s for s in sentences if user_query.lower() in s.lower()]
    if len(filtered) < 3:
        filtered = sentences[:5]
    return " ".join(filtered)
