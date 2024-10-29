import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hardcode the Sarvam API key (not recommended for production)
SARVAM_API_KEY = 'e3f33b3d-9b13-42c0-a27c-31d247320b74'

if not SARVAM_API_KEY:
    raise ValueError("Sarvam API key is missing")


# Translation API function using Sarvam (without JSON, using form data)
def translate_text(text, target_language):
    url = "https://api.sarvam.ai/translate"  # Replace with actual Sarvam API endpoint
    headers = {
        'Ocp-Apim-Subscription-Key': SARVAM_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'text': text,
        'target_language': target_language
    }

    # Use data instead of json for form-urlencoded
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.text  # Assuming the response is plain text, adjust if needed
    elif response.status_code == 403:
        return "Error: Subscription key is missing or invalid."
    else:
        # Logging the error for debugging
        print(f"Error: {response.status_code} - {response.text}")
        return f"Error: {response.status_code} - {response.text}"


# Voice changer API function (TTS) using Sarvam (without JSON, using form data)
def convert_text_to_speech(text, voice_type="default"):
    url = "https://api.sarvam.ai/tts"  # Replace with actual Sarvam API endpoint
    headers = {
        'Ocp-Apim-Subscription-Key': SARVAM_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'text': text,
        'voice_type': voice_type
    }

    # Use data instead of json for form-urlencoded
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.text  # Assuming the response is plain text, adjust if needed
    elif response.status_code == 403:
        return "Error: Subscription key is missing or invalid."
    else:
        # Logging the error for debugging
        print(f"Error: {response.status_code} - {response.text}")
        return f"Error: {response.status_code} - {response.text}"


@app.route('/')
def home():
    return render_template('index.html')


# Translation page route
@app.route('/translate', methods=['GET', 'POST'])
def translate_page():
    translated_text = None
    if request.method == 'POST':
        original_text = request.form['text']
        target_language = request.form['language']  # Get selected target language
        translated_text = translate_text(original_text, target_language)
    return render_template('translate.html', translated_text=translated_text)


# Voice changer page route
@app.route('/voicechanger', methods=['GET', 'POST'])
def voicechanger_page():
    audio_url = None
    if request.method == 'POST':
        voice_text = request.form['text']
        voice_type = request.form.get('voice_type', 'default')  # Optional voice type selection
        audio_url = convert_text_to_speech(voice_text, voice_type)
    return render_template('voicechanger.html', audio_url=audio_url)


@app.errorhandler(403)
def api_key_error(error):
    return "Error: Subscription key is missing or invalid.", 403


@app.route('/back_home')
def back_home():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
