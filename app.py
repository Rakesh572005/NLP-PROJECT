import streamlit as st
from logic import extract_text_from_pdf, summarize_text, extract_insights, summarize_based_on_input

# ==========================
# LOAD CSS
# ==========================
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ==========================
# MAIN FUNCTION
# ==========================
def main():
    st.set_page_config(page_title="Context-Aware PDF Summarizer", page_icon="📘", layout="wide")
    load_css()

    # ===== FIXED NAVBAR =====
    st.markdown("""
    <nav class="custom-navbar">
      <div class="nav-content">
        <div class="nav-left">
          <img src="https://img.icons8.com/color/48/artificial-intelligence.png" class="nav-logo" />
        </div>
        <div class="nav-right">
          <a href="#home">Home</a>
          <a href="#developer">Developer</a>
          <a href="https://rakesh-manubolu.vercel.app/" target="_blank">Portfolio</a>
        </div>
        <div class="hamburger" onclick="toggleMenu()">☰</div>
      </div>
    </nav>

    <div id="mobileMenu" class="mobile-menu">
      <a href="#home" onclick="toggleMenu()">Home</a>
      <a href="#developer" onclick="toggleMenu()">Developer</a>
      <a href="https://rakesh-manubolu.vercel.app/" target="_blank" onclick="toggleMenu()">Portfolio</a>
      <a href="#" class="close-btn" onclick="toggleMenu()">✕</a>
    </div>

    <script>
      function toggleMenu(){
        document.getElementById("mobileMenu").classList.toggle("open");
      }
      document.addEventListener('DOMContentLoaded', function(){
        document.querySelectorAll('a[href^="#"]').forEach(anchor=>{
          anchor.addEventListener('click', function(e){
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({behavior:'smooth'});
          });
        });
      });
    </script>
    """, unsafe_allow_html=True)

    # ===== PAGE HEADER =====
    st.markdown("""
      <section id="home" class="page-header">
        <h1 class="main-heading">📘 Context-Aware PDF Summarizer</h1>
        <hr class="main-divider">
      </section>
    """, unsafe_allow_html=True)

    # ===== SIDEBAR =====
    with st.sidebar:
        st.image("https://img.icons8.com/ios-filled/100/1976d2/pdf.png", width=80)
        st.markdown("## 📘 PDF Summarizer")
        st.markdown("Upload PDFs and extract key insights effortlessly.")
        st.markdown("---")
        st.markdown("👨‍💻 **Created by:** Rakeshuuuu")
        st.markdown("🌐 [Visit Portfolio](https://rakesh-manubolu.vercel.app/)")

    # ===== FILE UPLOAD =====
    pdf_file = st.file_uploader("📂 Upload your PDF file", type=["pdf"], key="pdf_uploader_main")

    if pdf_file:
        with st.spinner("⏳ Extracting and analyzing text..."):
            text = extract_text_from_pdf(pdf_file)

        if len(text.strip()) == 0:
            st.error("❌ No readable text found in the PDF.")
            return

        # ===== SUMMARY SECTION =====
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 Extracted Summary")
        summary = summarize_text(text)
        st.write(summary)
        st.download_button(
            label="💾 Download Summary",
            data=summary,
            file_name="pdf_summary.txt",
            mime="text/plain"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # ===== INSIGHTS SECTION =====
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💡 Key Insights & Suggestions")
        entities, suggestions = extract_insights(text)
        st.write("**Top Entity Types:**", entities)
        for s in suggestions:
            st.markdown(f"- {s}")
        st.markdown("</div>", unsafe_allow_html=True)

        # ===== CONTEXT-AWARE SECTION =====
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🎯 Context-Aware Re-Summarization")
        user_input = st.text_input("Enter a focus area (e.g., 'methods', 'results', 'finance'):")
        if user_input:
            with st.spinner("Generating context-aware summary..."):
                context_summary = summarize_based_on_input(text, user_input)
            st.markdown("### Focused Summary")
            st.write(context_summary)
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== DEVELOPER SECTION (BOTTOM) =====
    st.markdown("""
    <section id="developer" class="developer-section">
      <h2>👨‍💻 About the Developer</h2>
      <p>Built by <strong>Rakeshuuuu</strong> — a passionate developer from LBRCE focusing on AI, Web, and IoT innovation.</p>
      <p>💻 <a href="https://rakesh-manubolu.vercel.app/" target="_blank">Visit Portfolio</a></p>
      <p>📧 rakeshuuuu@gmail.com</p>
      <p class="copy">© 2025 Rakeshuuuu — All Rights Reserved</p>
    </section>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
