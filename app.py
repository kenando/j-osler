from flask import Flask, render_template, request, jsonify
import os

# Note: We need to specify the template_folder and static_folder
# because the app.py is in the root, but the templates/static files
# are in the 'app/' directory.
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static'))

@app.route('/')
def index():
    """
    Renders the main page.
    """
    return render_template('index.html')

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """
    API endpoint to generate a summary for the given text.
    """
    data = request.get_json()
    if not data or 'case_text' not in data:
        return jsonify({'error': 'Missing case_text in request'}), 400

    case_text = data['case_text']

    # --- Placeholder for AI logic ---
    # In the future, this will be replaced with a call to a sophisticated AI model.
    # For now, we'll just prepend a string to the input text.
    summary = f"【AIによる要約結果（プロトタイプ）】\n\n{case_text}"
    # --------------------------------

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
