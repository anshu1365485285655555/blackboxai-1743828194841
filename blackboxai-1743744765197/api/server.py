from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import os
import requests

app = Flask(__name__, static_folder='../', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process')
def process():
    return app.send_static_file('process.html')

@app.route('/results')
def results():
    return app.send_static_file('results.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Connect to external AI service (example using requests)
    try:
        image_file = request.files['image']
        prompt = request.form.get('prompt', 'high quality design variation')
        
        # Canva API integration
        api_url = "https://api.canva.com/v1/images/generate"
        headers = {
            "Authorization": "Bearer X6P7-8C4Q-3366-C3XQ-PF45-VFC6-HWHQ-Q649-52WR-28QF-XCFM-CRMP-J94J-9MGQ-75GV-HJC7-357P-2F5G-JG96-C9FG",
            "Content-Type": "application/json"
        }
        
        # Prepare the request
        # Request 4 design variations with different styles
        variations = []
        styles = ['photo', 'art', 'sketch', 'painting']
        
        for style in styles:
            payload = {
                "source_image": base64.b64encode(image_file.read()).decode('utf-8'),
                "prompt": prompt,
                "style_preset": style,
                "output_format": "jpeg",
                "variation_count": 1
            }
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            variations.append({
                "style": style,
                "image": response.json()['result']
            })
            image_file.seek(0)  # Reset file pointer for next iteration
        
        return jsonify({"variations": variations})
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'note': 'Failed to connect to AI service'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
