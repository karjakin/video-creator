from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

load_dotenv()
import re
import json
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')



def obtener_JsonIma(texto):
    if not isinstance(texto, str):
        raise ValueError("La entrada debe ser una cadena de texto.")

    # Ajustar la expresión regular para dividir correctamente los prompts
    # y para manejar el último prompt que no termina con 'n/\n'
    prompts = re.split(r'n/\n(?=\d+\.)', texto)
    prompts_dict = {}

    for prompt in prompts:
        # Extraer el número del prompt
        numero = re.search(r'^\d+', prompt)
        if numero:
            clave = int(numero.group())
            # Eliminar el número del inicio del prompt
            valor = re.sub(r'^\d+\.\s', '', prompt)
            # Eliminar 'n/' del final del prompt, si existe
            valor = re.sub(r'n/$', '', valor).strip()
            prompts_dict[clave] = valor

    # Convertir el diccionario a JSON
    return json.dumps(prompts_dict, indent=4)

# Inicializa el modelo 'Together' utilizando la clase 'Together'
llmt = OpenAI(api_key="sk-111111111111111111111111111111111111111111111111", base_url='http://127.0.0.1:5000/v1')
prompt_template = PromptTemplate.from_template("""
### User:
Your task is to meticulously analyze the narrative provided below and craft a series of detailed, vivid descriptions for each distinct scene depicted in the story. These descriptions should serve as comprehensive guides for creating engaging, visually captivating content, closely aligned with the narrative's essence. 
There must be at least 10 scenes, each with a detailed description.
The descriptions should effectively encapsulate the core elements, mood, and tone of the story. The aim is to create compelling visual narratives that can be vividly brought to life through AI-driven tools like Stable Diffusion.

For each scene, your description should be approximately 100 characters long, encapsulating the essence of the scene with rich detail and precision. Each description must include:

1. Specificity: Clearly articulate the details of the scene's primary objects, characters, and setting. Describe the textures, colors, and spatial relationships to create a vivid mental image.
2. Style Definition: Suggest an art style or visual effects that align with the narrative's tone. This could range from surrealistic to hyper-realistic, depending on the scene's context and mood.
3. Mood and Emotion: Use descriptive language to convey the scene's emotional atmosphere. Whether it's a tense standoff or a tranquil landscape, the mood should be palpable through your words.
4. Dynamic Action: Employ action verbs to breathe life into the scene. Describe movements and actions in a way that adds dynamism and a sense of progress to the static image.
5. Color Palette: Provide a well-thought-out color palette to guide the visual tone of the scene. Mention the dominant colors and how they contribute to the scene's overall mood and theme.
6. Component Positioning: Detail the positioning of key elements within the scene, ensuring a balanced, coherent composition that aligns with the narrative's flow.

Your descriptions should be a fusion of these elements, forming complex, layered prompts that will guide the AI in generating images that are not only visually stunning but also narratively cohesive and true to the story's spirit.

---
'{narracion}'
---

Output a structured list like this, without adding any additional comments.
### Assistant:
""")

prompt_template_context_definition = PromptTemplate.from_template("""
### User:
Adjusts and improves a given image description based on the narrative context of a story. 
The improved description will align with the story's sequence, incorporating detailed descriptions 
of objects, settings, atmosphere, image style, scene mood, actions, colors, and object positions. 
To improve the image description, consider the global context and the original sentence on which it was based,
ensuring it fits the full context of the narrative.
Parameters:
                                                                                                                            
A story's narrative context:
---
'{narracion}'
---                                                                                                                              
The original sentence the prompt was based on:
---
'{oracion}'
---                                                                 
original image description to be improved:                                                               
===
'{mensaje}'
===                                                                                                                                     
Returns:
A single, detailed, and improved image description that fits the narrative context of the story. In English.
It is very important that you do not make extra comments or notes nor the length, only the improved image description.                                                                 
### Assistant:
""")

prompt_template_negative_definition = PromptTemplate.from_template("""
Your task is to generate a negative prompt based on the provided positive prompt. The negative prompt should guide the image generation model away from certain unwanted elements or qualities that are likely to be inferred from the positive prompt. Use the positive prompt as a context to anticipate and counter potential issues in the generated image.

Consider the following guidelines while generating the negative prompt:
1. The negative prompt should be relevant to the context of the positive prompt, addressing potential issues related to the positive description.
2. Ensure the language is precise and unambiguous to effectively guide the model away from unwanted elements.
3. Keep the prompt concise but comprehensive, covering all potential unwanted aspects that might arise from the positive prompt.
4. Format the output as a comma-separated list of negatives.

Positive Prompt:
===
'{positive_prompt}'
===

Generate a negative prompt based on the above positive prompt, do not exceed 100 characters, the negatives must be related to unwanted image descriptions, not text:
Assistant:
""")

prompt_template_short_narative = PromptTemplate.from_template("""
### User:                                                              
You need to condense the following narrative into a shorter, more direct version in English.

### Original Narrative (Spanish):
===
'{narrative}'
===
Please provide a concise and direct English version of the above narrative.
### Assistant:
""")
prompt_template_video = PromptTemplate.from_template("""
    ### User:
    Based on the data below create a list of NUMBERS with the durations in sec for each image to be displayed in a video the list must sum up to the audio duration."
    Narrative: 
    {narrative}
    Total number of images: 
    {image_count}
    Image descriptions: {image_descriptions}
    Audio duration: {audio_duration}
    The duration each image is displayed will be evenly distributed to maintain a dynamic and engaging flow, considering the pace of the narrative. "
    The duration of each image must be based on the narrative context and the amount of words in the description. The goal is to ensure that the images are displayed for an optimal duration to complement the narrative and maintain viewer engagement. "
    ### Assistant:
    """,
)


prompt_template_resume_news = PromptTemplate.from_template(
    "Based on the '{text}' text, create resume of the news article. Just include the most important information. Be concise and include facts and details that are relevant to the news article. The resume must be at least 170 characters long."
)

prompt_template_sentence = PromptTemplate.from_template("""
### User:
Your task is to analyze the current sentence of a narrative and develop a vivid and detailed description for the scene it represents. This description should serve as a comprehensive guide for creating visually engaging and captivating content, closely aligned with the essence of the narrative. The description should effectively summarize the central elements, mood, and tone of the story, with the aim of creating a compelling visual narrative that can be vividly brought to life through AI tools like Stable Diffusion.

The scene description should be approximately 50 words and summarize the essence of the scene with great detail and precision, including:

1. Specificity: Clearly articulate the details of the scene's main objects, characters, and setting. Describe textures, colors, and spatial relationships to create a vivid mental image.
2. Defining Style: Suggest an art style or visuals that align with the tone of the narrative. This could range from surreal to hyperreal, depending on the context and mood of the scene.
3. Mood and Emotion: Use descriptive language to convey the emotional atmosphere of the scene. Whether it's a tense confrontation or a calm landscape, the mood should be palpable through your words.
4. Dynamic Action: Use action verbs to bring the scene to life. Describe movements and actions in a way that adds dynamism and a sense of progress to the static image.
5. Color Palette: Provide a thoughtful color palette to guide the visual tone of the scene. Mention the dominant colors and how they contribute to the mood and overall theme of the scene.
6. Component Positioning: Detail the positioning of key elements within the scene, ensuring a balanced and coherent composition that aligns with the flow of the narrative.

Your description should be a fusion of these elements, forming a complex, layered prompt that will guide AI in generating images that are not only visually striking but also narratively cohesive and true to the spirit of the story.

---
'{sentence}'
---
A single, detailed, and improved image description In English.
It is very important that you do not make extra comments or notes nor the length, only the improved image description.  
### Assistant:
""")

def parse_prompts(input_str):
    # Split the input string by line breaks to get individual prompts
    prompts = input_str.split("\n")
    
    # Prepare the JSON output structure
    output = {}

    # Iterate over the prompts to add them to the JSON output
    for prompt in prompts:
        # Skip empty prompts
        if prompt.strip() and not prompt.strip() == "n/":
            # Extract the prompt number and the description
            number, description = prompt.split('.', 1)
            # Add the prompt to the output dictionary
            output[number.strip()] = description.strip()

    return output


def parse_detailed_prompts(input_str):
    # Split the input string by double line breaks to separate each detailed prompt
    prompts = input_str.split("\n\n")

    # Prepare the JSON output structure
    output = {}

    # Iterate over the prompts to add them to the JSON output
    for prompt in prompts:
        # Skip empty prompts
        if prompt.strip() and not prompt.strip() == "n/":
            # Split the prompt into lines to process each part
            lines = prompt.split("\n")
            # Initialize a dictionary to store the details of the prompt
            prompt_details = {}
            
            # Process each line
            for line in lines:
                # Split the line into a key and a value part
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key, value = parts
                    # Clean and store the key-value pair in the prompt details
                    prompt_details[key.strip()] = value.strip()
            
            # Get the prompt number from the first line (style description)
            number = lines[0].split('.')[0]
            # Add the prompt details to the output dictionary
            output[number.strip()] = prompt_details

    return output

prompt = prompt_template

llmr = OpenAI(api_key="sk-111111111111111111111111111111111111111111111111", base_url='http://127.0.0.1:5000/v1')
model = llmr
chain = prompt | model 

chains = prompt_template_context_definition | model
chain_image = prompt_template_negative_definition | model
chain_video = prompt_template_video | model
chain_sentence = prompt_template_sentence | model
chain_resume_news = prompt_template_resume_news | model
chain_short_narrative =prompt_template_short_narative | model


def obtener_short_narrative (narrative):
    # Invoke the chain with the generated prompt
    response = chain_short_narrative.invoke({'narrative': narrative})
    return response

def obtener_prompt(narracion):
    # Invoke the chain with the generated prompt
    response = chain.invoke({'narracion': narracion})
    
    
    return response

def obtener_prompt_context(narracion, mensaje, oracion):
    # Invoke the chain with the generated prompt
    response = chains.invoke({'narracion': narracion, 'mensaje': mensaje,'oracion': oracion })
    
    
    return response

def obtener_prompt_negative(positive_prompt):
    # Invoke the chain with the generated prompt
    response = chain_image.invoke({'positive_prompt': positive_prompt})
    
    
    return response

def obtener_prompt_video(narrative, image_count, image_descriptions, audio_duration):
    # Invoke the chain with the generated prompt
    response = chain_video.invoke({'narrative': narrative, 'image_count': image_count, 'image_descriptions': image_descriptions, 'audio_duration': audio_duration})
    
    
    return response

def obtener_prompt_resume_noticia(text):
    # Invoke the chain with the generated prompt
    response = chain_resume_news.invoke({'text': text})
    
    
    return response

def obtener_prompt_sentence(sentence):
    # Invoke the chain with the generated prompt
    response = chain_sentence.invoke({'sentence': sentence})
    
    return response