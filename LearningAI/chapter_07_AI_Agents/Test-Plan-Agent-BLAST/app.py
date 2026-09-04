"""
Flask Web Application - Jira Test Plan Generator
Layer 4: Web UI & Styling

Purpose: Provide web interface for test plan generation
Status: Phase 4 Implementation
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

from navigation import TestPlanOrchestrator

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize orchestrator
orchestrator = TestPlanOrchestrator()


@app.route('/', methods=['GET'])
def index():
    """Landing page."""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_test_plan():
    """
    Generate test plan from Jira issue ID.
    
    Request JSON:
    {
        "issueKey": "PROJ-123"
    }
    
    Response JSON:
    {
        "metadata": {...},
        "testPlan": {...},
        "coverage": {...},
        ...
    }
    """
    try:
        data = request.get_json()
        issue_key = data.get('issueKey', '').strip().upper()
        
        if not issue_key:
            return jsonify({'error': 'Issue key is required'}), 400
        
        # Generate test plan
        result = orchestrator.generate_test_plan(issue_key)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/download/<issue_key>', methods=['GET'])
def download_markdown(issue_key):
    """Download generated Markdown file."""
    try:
        file_path = f'.tmp/{issue_key.upper()}_test_plan.md'
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=f'{issue_key}_test_plan.md')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-json/<issue_key>', methods=['GET'])
def download_json(issue_key):
    """Download generated JSON file."""
    try:
        file_path = f'.tmp/{issue_key.upper()}_test_plan.json'
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=f'{issue_key}_test_plan.json')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'online',
        'service': 'Jira Test Plan Generator',
        'timestamp': str(__import__('datetime').datetime.now())
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Jira Test Plan Generator - Starting Server")
    print("=" * 60)
    print()
    print("📍 Open your browser:")
    print("   URL: http://localhost:5000")
    print()
    print("   Generating test plans from Jira issues...")
    print("   LLM: Groq (qwen/qwen3.8-27b)")
    print("   Jira: https://sharbaniai2026.atlassian.net/")
    print()
    print("=" * 60)
    print()
    
    app.run(debug=True, host='localhost', port=5000)
