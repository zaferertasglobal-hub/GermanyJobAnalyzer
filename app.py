from flask import Flask, render_template, request, jsonify
import json
import os
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)

app = Flask(__name__)

# JSON dosyasını yükle
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'data', 'germany_skills.json')

with open(json_path, 'r', encoding='utf-8') as f:
    skills_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        cv_text = request.form.get('cv_text', '').lower()
        
        # Tüm becerileri küçük harf listesi
        flat_skills = []
        for category in skills_data['top_skills'].values():
            flat_skills.extend([s.lower() for s in category])
        
        # Hangi beceriler CV’de var?
        found = [skill.title() for skill in flat_skills if skill in cv_text]
        
        # Skor hesapla (basit ama etkili)
        score = len(found) * 10
        bonus = ['python', 'java', 'javascript', 'react', 'aws', 'docker', 'kubernetes']
        for b in bonus:
            if b in cv_text:
                score += 12
        match_score = min(98, score)

        return jsonify({
            "match_score": match_score,
            "user_skills": found if found else ["Tespit edilemedi"],
            "top_skills": ["Python", "Java", "JavaScript", "React", "AWS"]
        })
        
    except Exception as e:
        return jsonify({"error": "Sunucu hatası: " + str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    app.run(debug=True)