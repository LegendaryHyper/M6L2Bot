import json
import time
import config
import requests
import base64
from PIL import Image
from io import BytesIO
import random

class FusionBrainAPI:
    
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f"Key {api_key}",
            'X-Secret': f"Secret {secret_key}"
        }
    
    def get_pipeline(self):
        response = requests.get(self.URL + "key/api/v1/pipelines", headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']
    
    def generate(self, prompt, pipeline, images = 1, width = 1024, height = 1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }
        
        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + "key/api/v1/pipeline/run", headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']
    
    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + "key/api/v1/pipeline/status/" + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']
            
            attempts -= 1
            time.sleep(delay)

def base64_to_image(base64_string):
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image
def multiple_conv(file):
    pics = []
    id = random.randint(1,1000000)
    for i, file_data in enumerate(file):
        try:
            saved_gen = base64_to_image(file_data)
            filename = f"output_image_{i+1}ID{id}.png"
            saved_gen.save(filename)
            print(f"Saved: {filename}")
            saved_gen.show()
            pics.append(filename)
        except Exception as e:
            print(f"Error processing image {i+1}: {e}")
    return pics
def gen_and_save(prompt="A palace"):
    api = FusionBrainAPI("https://api-key.fusionbrain.ai/", config.KEY, config.SECRET)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)
    print(files)
    return multiple_conv(files)
if __name__ == '__main__':
    pass
    #print(gen_and_save("A wizard cat with huge classes casting a fire spell"))
