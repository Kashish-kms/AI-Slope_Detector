from flask import Flask, render_template, request, jsonify, send_file
from config import Config
from database.database import db, AnalysisHistory
from models.detector import AIDetector
from models.openai_helper import OpenAIHelper
from scraper.scraper import WebScraper
from utils.metrics import SlopMetrics
import logging

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize Models
detector = AIDetector(app.config)
openai_bot = OpenAIHelper(app.config['OPENAI_API_KEY'])

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    content = data.get('text', '')
    is_url = data.get('is_url', False)

    try:
        if is_url:
            content = WebScraper.extract_text(content)
        
        if not content or len(content) < 50:
            return jsonify({"error": "Content too short for analysis (min 50 chars)"}), 400

        # 1. Run AI Detection
        scores = detector.predict(content)
        ppl = detector.calculate_perplexity(content)
        
        # 2. Get Metrics
        metrics = SlopMetrics.calculate_repetition(content)
        readability = SlopMetrics.get_readability_scores(content)
        
        # 3. Slop Probability logic (Hybrid)
        # AI slop = high AI score + low perplexity + high repetition
        slop_prob = (scores['ai'] * 0.6) + (max(0, (100-ppl)/100) * 0.4)
        
        # 4. OpenAI explanation
        explanation = openai_bot.analyze_slop(content, scores)

        # 5. Save to DB
        record = AnalysisHistory(
            content_type='url' if is_url else 'text',
            input_data=content[:500],
            ai_score=scores['ai'],
            human_score=scores['human'],
            slop_probability=slop_prob,
            summary=explanation
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            "status": "success",
            "results": {
                "ai_score": scores['ai'],
                "human_score": scores['human'],
                "slop_prob": slop_prob,
                "perplexity": ppl,
                "metrics": { "repetition": metrics, **readability },
                "explanation": explanation
            }
        })

    except Exception as e:
        logging.error(f"Analysis error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)