import requests

url = 'https://api.sarvam.ai/translate'  # Replace with the actual API endpoint
headers = {
    'Ocp-Apim-Subscription-Key': 'e3f33b3d-9b13-42c0-a27c-31d247320b74'
}
data = {
    'text': 'Sarvam AI is a powerful platform for LLM tasks.',
    'target_language': 'es'  # Example: translating to Spanish (es)
}

response = requests.post(url, headers=headers, json=data)

# Handle the response
if response.status_code == 200:
    try:
        print(response.json())  # Assuming the response is JSON formatted
    except ValueError:
        print(response.text)
else:
    print(f"Error: {response.status_code} - {response.text}")
