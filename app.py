from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

client = Groq(
    api_key="your_api_key_here",
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST', 'OPTIONS'])  # Add OPTIONS method
def translate():
    if request.method == 'OPTIONS':  # Handle preflight request
        return '', 204
    try:
        if not request.is_json:
            return jsonify({'error': 'Missing JSON in request'}), 400

        text = request.json.get('text', '').strip()
        if not text:
            return jsonify({'error': 'Empty text provided'}), 400
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a French translator. Translate the text to French. Only provide the translation."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        translation = completion.choices[0].message.content.strip().strip('"').strip()
        
        if not translation:
            return jsonify({'error': 'No translation received from API'}), 500

        return jsonify({
            'original': text,
            'french': translation
        })

    except Exception as e:
        app.logger.error(f'Translation error: {str(e)}')
        return jsonify({'error': str(e)}), 500  # Return actual error for debugging

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Explicitly set port to 5000
