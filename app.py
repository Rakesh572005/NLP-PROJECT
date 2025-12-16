import streamlit as st
from logic import extract_text_from_pdf, summarize_text, extract_insights, summarize_based_on_input

def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Context-Aware PDF Summarizer", page_icon="📘", layout="wide", initial_sidebar_state="expanded")
    load_css()

    
    st.markdown(
        """
    <style>
    .fixed-nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background-color: #1976d2;a
        color: white;
        z-index: 9999;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .nav-inner {
        width: 100%;
        max-width: 1200px;
        margin: auto;
        padding: 0 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-links a {
        color: white;
        text-decoration: none;
        padding: 0 12px;
        font-size: 16px;
    }
    .nav-links a:hover {
        text-decoration: underline;
    }
    </style>

    <nav class="fixed-nav">
        <div class="nav-inner">
            <img src="https://img.icons8.com/color/48/artificial-intelligence.png" style="height:40px;" />
            <div class="nav-links">
                <a href="#home">Home</a>
                <a href="https://www.helpwire.app/builds/?token=XfRABQSxiuwFswuS4YeOhOLhDZ15dusLgtE26jnA">Developer</a>
                <a href="https://www.helpwire.app/builds/?token=oIt4dvQt6ySrQ1GCGsiLuNG1X64dENYc6RYQKgTp" target="_blank">Other Services</a>
            </div>
        </div>
    </nav>
    """,
        unsafe_allow_html=True
    )





    st.markdown("""
        <style>
            h1 a, h2 a, h3 a {
                display: none !important;
                visibility: hidden !important;
            }
        </style>

        <section id="home" class="page-header">
            <h1 class="main-heading">Context-Aware PDF Summarizer BATCH-15</h1>
            <hr class="main-divider">
        </section>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://img.icons8.com/ios-filled/100/1976d2/pdf.png", width=80)
        st.markdown("## PDF Summarizer")
        st.markdown("Upload PDFs and extract key insights effortlessly.")
        st.markdown("---")
        st.markdown("**Created by:** Batch-15")

    pdf_file = st.file_uploader(" Upload your PDF file", type=["pdf"], key="pdf_uploader_main")

    if pdf_file:
        with st.spinner(" Extracting and analyzing text..."):
            text = extract_text_from_pdf(pdf_file)

        if len(text.strip()) == 0:
            st.error(" No readable text found in the PDF.")
            return

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(" Extracted Summary")
        summary = summarize_text(text)
        st.write(summary)
        st.download_button(
            label=" Download Summary",
            data=summary,
            file_name="pdf_summary.txt",
            mime="text/plain"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💡 Key Insights & Suggestions")


        insights_text, suggestions = extract_insights(text)

        st.markdown("### Key Insights :")
        st.write(insights_text)

        st.markdown("### Suggestions :")
        for s in suggestions:
            st.markdown(f"- {s}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(" Context-Aware Re-Summarization")
        user_input = st.text_input("Enter a focus area (e.g., 'methods', 'results', 'finance'):")
        if user_input:
            with st.spinner("Generating context-aware summary..."):
                context_summary = summarize_based_on_input(text, user_input)
            st.markdown("### Focused Summary")
            st.write(context_summary)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <footer id="developer" class="footer">
      <div class="footer-content">
        <h3> About the Developer</h3>
        <p>Built by <strong>Batch-15</strong> — a passionate developer from LBRCE focusing on AI, Web, and IoT innovation.</p>
        <p> BATCH15@gmail.com</p>
        <p class="copy">© 2025 BATCH15 — All Rights Reserved</p>
      </div>
    </footer>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
