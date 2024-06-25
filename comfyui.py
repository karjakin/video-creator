from urllib import request, error
import json
import random
import os

json_file_path = 'upscaler.json'

# Load JSON data from file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

def queue_prompt(prompt):
    try:
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')  # Convert the Python dictionary back to a JSON formatted string to send in the request
        req = request.Request("http://127.0.0.1:8188/prompt", data=data)
        with request.urlopen(req) as response:
            print("Request successful, response:", response.read())
    except error.HTTPError as e:
        print('HTTPError: ', e.code, e.reason)
    except error.URLError as e:
        print('URLError: ', e.reason)
    except Exception as e:
        print('Generic Exception: ', e)

def generate_random_15_digit_number():
    return random.randint(100000000000000, 999999999999999)

def json_imagen(json_data, id, negative_prompt):
  
    negative = negative_prompt

    
    # Create directory
    dir_path = f'C:\\Users\\jairc\\Pictures\\ComfyUI\\output\\video\\{id}'
    os.makedirs(dir_path, exist_ok=True)
    print(f"Directory created at {dir_path}")
    


    for i, prompt in json_data.items():
        random_15_digit_numberr = generate_random_15_digit_number()
        data["49"]["inputs"]["seed"] = random_15_digit_numberr
        data["3"]["inputs"]["text"] = prompt
        data["4"]["inputs"]["text"] = negative
        data["56"]["inputs"]["output_path"] = f"./video/{id}"
        data["56"]["inputs"]["filename_prefix"] = "video"
        print(f"Processing prompt: {prompt}")
        queue_prompt(data)  # Assuming this generates the image and saves it to the specified path

    return "comfyui"


