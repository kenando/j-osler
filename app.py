from flask import Flask, render_template, request, jsonify
import os
import re
from app.ai_connector import generate_summary

# Note: We need to specify the template_folder and static_folder
# because the app.py is in the root, but the templates/static files
# are in the 'app/' directory.
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static'))

# In a real application, this would be loaded securely, e.g., from environment variables
# For example: DUMMY_API_KEY = os.environ.get("AI_SERVICE_API_KEY")
DUMMY_API_KEY = "dummy_key_for_prototype"

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

    # Call the AI connector to get the summary
    summary = generate_summary(api_key=DUMMY_API_KEY, text=case_text)

    return jsonify({'summary': summary})


@app.route('/api/format_lab_data', methods=['POST'])
def format_lab_data():
    """
    API endpoint to format lab data from a given text.
    """
    data = request.get_json()
    if not data or 'text_to_format' not in data:
        return jsonify({'error': 'Missing text_to_format in request'}), 400

    text_to_format = data['text_to_format']

    # Simple regex to find lines with a pattern like: "Item Name 123.45 unit"
    # This is a very basic prototype implementation.
    lab_item_pattern = re.compile(r'^\s*([^\s\d]+(?:\s+[^\s\d]+)*)\s+([\d\.\,]+)\s*(.*)\s*$', re.MULTILINE)

    formatted_lines = [
        "--- 整形された検査データ ---",
        "| 項目名 | 値 | 単位 |",
        "|---|---|---|"
    ]

    lines = text_to_format.strip().split('\n')
    found_items = 0
    for line in lines:
        match = lab_item_pattern.match(line)
        if match:
            item_name = match.group(1).strip()
            value = match.group(2).strip()
            unit = match.group(3).strip()
            formatted_lines.append(f"| {item_name} | {value} | {unit} |")
            found_items += 1

    if found_items == 0:
        result = "検査データと判断される項目が見つかりませんでした。入力テキストが「項目名 値 単位」の形式になっているか確認してください。"
    else:
        result = "\n".join(formatted_lines)

    return jsonify({'formatted_text': result})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
