import fitz  # PyMuPDF
import streamlit as st
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
    filtered_words = [w for w in words if w not in stop_words and w not in string.punctuation]
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
        suggestions.append("Dates are mentioned — you can explore timelines or event order.")
    if "GPE" in entity_labels:
        suggestions.append("Contains geographical data — mapping or location analysis could help.")
    if not suggestions:
        suggestions.append("General informative document — consider extracting topic keywords for deeper insights.")

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

# ==============================
# 6. STREAMLIT APP
# ==============================
def main():
    st.title("📘 Context-Aware PDF Summarizer with Key Insight Extraction")

    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_uploader_main")

    if pdf_file:
        with st.spinner("Extracting and analyzing text..."):
            text = extract_text_from_pdf(pdf_file)

        if len(text.strip()) == 0:
            st.error("No readable text found in the PDF.")
            return

        # ==============================
        # SUMMARY SECTION
        # ==============================
        st.subheader("Extracted Summary")
        summary = summarize_text(text)
        st.write(summary)

        # Download summary button
        st.download_button(
            label="💾 Download Summary as Text",
            data=summary,
            file_name="pdf_summary.txt",
            mime="text/plain"
        )

        # ==============================
        # INSIGHTS SECTION
        # ==============================
        st.subheader("Key Insights and Suggestions")
        entities, suggestions = extract_insights(text)
        st.write("**Top Entity Types:**", entities)
        st.write("**Suggestions:**")
        for s in suggestions:
            st.write("-", s)

        # ==============================
        # CONTEXT-AWARE SECTION
        # ==============================
        st.markdown("---")
        st.subheader("Context-Aware Re-Summarization")
        user_input = st.text_input("Enter your focus area or query (e.g., 'methodology', 'results', 'climate change'):")
        if user_input:
            with st.spinner("Generating context-aware summary..."):
                context_summary = summarize_based_on_input(text, user_input)
            st.write("### Focused Summary")
            st.write(context_summary)

if __name__ == "__main__":
    main()
