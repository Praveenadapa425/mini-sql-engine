"""
Web interface for the Mini SQL Database Engine.
Provides a simple web UI to interact with the SQL engine.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.parser import SQLParser
from src.engine import SQLEngine, format_results
from src.exceptions import SQLError

app = Flask(__name__)

# Initialize components
parser = SQLParser()
engine = SQLEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_query():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Empty query'}), 400
            
        # Parse and execute query
        parsed_query = parser.parse(query)
        result = engine.execute_query(parsed_query)
        formatted_result = format_results(result)
        
        return jsonify({
            'success': True,
            'result': formatted_result,
            'query': query
        })
    except SQLError as e:
        return jsonify({'error': f'SQL Error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)