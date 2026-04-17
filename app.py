from flask import Flask, render_template, request, jsonify
from src.matcher import ResumeMatcher
from src.utils import format_report
import json

app = Flask(__name__)
matcher = ResumeMatcher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/match', methods=['POST'])
def match():
    try:
        data = request.json
        resume = data.get('resume', '')
        job_description = data.get('job_description', '')
        
        if not resume or not job_description:
            return jsonify({'error': 'Both resume and job description required'}), 400
        
        result = matcher.match_resume_to_job(resume, job_description)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/report', methods=['POST'])
def get_report():
    try:
        data = request.json
        resume = data.get('resume', '')
        job_description = data.get('job_description', '')
        
        result = matcher.match_resume_to_job(resume, job_description)
        report = format_report(result)
        
        return jsonify({'report': report})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)