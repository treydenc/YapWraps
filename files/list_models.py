import requests

def list_models():
    url = "https://api.elevenlabs.io/v1/models"
    headers = {
        "xi-api-key": "sk_e0874727d38627d958542d52d9b8ced506f0149c679a3ddf"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        models = response.json()

        for model in models:
            print(f"Model ID: {model['model_id']}")
            print(f"Name: {model['name']}")
            print(f"Can do TTS: {model['can_do_text_to_speech']}")
            print("---")
    else:
        print(f"Failed to retrieve models: {response.status_code} - {response.text}")

if __name__ == "__main__":
    list_models()
