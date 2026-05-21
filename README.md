# 🛡️ AI Slop Detector

An advanced web-based forensic tool designed to identify AI-generated content, low-quality "AI slop," and authentic human writing. This project combines deep learning (Transformers) with traditional linguistic metrics to provide a "Slop Probability Score."

## 🚀 Key Features
- **Hybrid Detection Engine**: Uses a combination of RoBERTa-based models and GPT-2 Perplexity analysis.
- **URL Analysis**: Integrated web scraper (BeautifulSoup) to analyze articles and blog posts directly via URL.
- **Explainable AI (XAI)**: Uses OpenAI GPT-4o-mini to explain *why* content was flagged as AI-generated.
- **Linguistic Metrics**: Calculates repetitiveness, keyword stuffing, and readability (Flesch-Kincaid).
- **History System**: Local persistence of analysis results using SQLite.
- **PDF Export**: Generate professional forensic reports of the analysis.

## 🛠️ Tech Stack
- **Backend**: Python, Flask, SQLAlchemy
- **AI/ML**: Hugging Face Transformers (RoBERTa), PyTorch, GPT-2
- **APIs**: OpenAI API
- **Scraping**: BeautifulSoup4, Requests
- **Frontend**: HTML5, CSS3 (Modern UI), JavaScript (ES6+)
- **Data**: Pandas, Scikit-learn, Textstat

## 🏗️ Architecture
```text
[ Browser ] <---> [ Flask API ] <---> [ SQLite DB ]
                       |
        -------------------------------
        |              |              |
 [ Scraper ]   [ NLP Metrics ]   [ Transformer Model ]
