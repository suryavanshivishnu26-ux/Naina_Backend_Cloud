import os
from flask import Flask, request, jsonify
import base64
from datetime import datetime

app = Flask(__name__)

# Get API key from environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "your-groq-api-key-here")

# Don't initialize Groq client at import time - do it when needed
def get_groq_client():
    """Initialize Groq client only when needed"""
    from groq import Groq
    return Groq(api_key=GROQ_API_KEY)

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        print("\n" + "="*50)
        print("📸 Received image analysis request")
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        print("="*50)
        
        # Log all headers
        print("📋 Headers:")
        for header, value in request.headers:
            print(f"   {header}: {value}")
        
        # Get prompt type from header
        prompt_type = int(request.headers.get('X-Prompt-Type', 1))
        print(f"📝 Prompt Type: {prompt_type}")
        
        # Get raw image bytes
        image_bytes = request.get_data()
        print(f"📦 Image data length: {len(image_bytes)} bytes")
        
        if len(image_bytes) == 0:
            print("❌ Error: No image data received")
            return jsonify({'error': 'No image data provided'}), 400
        
        # Convert to base64 for Groq API
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        print(f"📏 Base64 length: {len(image_base64)} characters")
        
        # Define prompts based on type
        prompts = {
            1: "Solve this problem step by step. If it's a math problem, provide the solution. If it's text, transcribe it clearly.",
            2: "Identify and list all the objects visible in this image. Be specific and concise."
        }
        
        prompt_text = prompts.get(prompt_type, prompts[1])
        print(f"💬 Using prompt: {prompt_text}")
        
        # Create the message for Groq API
        print("\n🔄 Sending request to Groq API...")
        
        # Initialize Groq client here (not at module level)
        client = get_groq_client()
        
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # Groq's vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            stream=False
        )
        
        # Get the response
        response_text = completion.choices[0].message.content
        
        print("\n✅ Response received from Groq API:")
        print("-" * 50)
        print(response_text)
        print("-" * 50)
        
        # Store the result globally for DevKit to fetch
        global latest_result
        latest_result = {
            'response': response_text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"\n💾 Result stored for DevKit (timestamp: {latest_result['timestamp']})")
        
        # Prepare response for ESP32
        # Truncate if too long for OLED display
        truncated_response = response_text[:200] if len(response_text) > 200 else response_text
        
        result = {
            'success': True,
            'response': truncated_response,
            'full_response': response_text
        }
        
        print(f"\n📤 Sending response back to ESP32 ({len(truncated_response)} chars)")
        print("="*50 + "\n")
        
        return jsonify(result), 200
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        print(f"\n❌ {error_msg}\n")
        return jsonify({'error': error_msg}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Server is running'}), 200

@app.route('/test', methods=['POST'])
def test_endpoint():
    print("\n🧪 TEST ENDPOINT HIT")
    try:
        data = request.get_json(force=True)
        print(f"Received data: {data}")
        return jsonify({'status': 'success', 'received': data}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

# Store the latest result globally
latest_result = {
    'response': 'No analysis available yet. Waiting for ESP32-CAM to send an image.',
    'timestamp': None
}

@app.route('/get_result', methods=['GET'])
def get_result():
    """Endpoint for ESP32 DevKit to fetch the latest analysis result"""
    print("\n" + "="*50)
    print("📱 DevKit requesting latest result")
    print("="*50)
    
    if latest_result['timestamp']:
        print(f"✅ Returning result from {latest_result['timestamp']}")
    else:
        print("⚠️ No result available yet")
    
    return jsonify({
        'response': latest_result['response'],
        'timestamp': latest_result['timestamp']
    }), 200

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 ESP32 Image Analysis Backend Server")
    print("="*50)
    
    # Get port from environment variable (for cloud deployment) or use 5000
    port = int(os.environ.get("PORT", 5000))
    
    print(f"📡 Server starting on port {port}")
    print("💡 Make sure to set your GROQ_API_KEY environment variable")
    print("⚠️  Endpoints:")
    print("   - POST /analyze : Analyze images from ESP32")
    print("   - GET  /health  : Health check")
    print("   - GET  /get_result : Get latest result")
    print("="*50 + "\n")
    
    # Run the server
    # Use 0.0.0.0 to accept connections from any IP
    app.run(host='0.0.0.0', port=port, debug=False)

