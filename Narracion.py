from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
import json
import re


load_dotenv()  # Esto carga las variables de entorno del archivo .env

# Inicializa el modelo 'Together' utilizando la clase 'Together'
llmt = OpenAI(api_key="sk-111111111111111111111111111111111111111111111111", base_url='http://127.0.0.1:5000/v1')
# Crea un PromptTemplate

model = llmt
examples = (
    "\"input\": \"Crear una narración expositiva sobre 'filosofía', enfocándose específicamente en la rama de 'estoicismo' con un enfoque 'histórico'. \"\n"
    "\"La narración debe ser rica en datos, interesante y educativa, y no exceder las 500 palabras.\",\n"
    "\"output\": \"\"\n"
    "\"\"\"\n"
    "Título: \"Viaje en el Tiempo al Corazón del Estoicismo\"\n\n"
    "Narración:\n"
    "\"Hoy nos sumergimos en el mundo del estoicismo, una filosofía nacida en la antigua Grecia y desarrollada en Roma.\"\n"
    "\"Conoce a Zenón, Séneca y Marco Aurelio, tres pilares del estoicismo que transformaron la forma de ver la vida y la adversidad.\"\n"
    "\"El estoicismo comenzó con Zenón en el Pórtico Pintado de Atenas, enfocándose en vivir en armonía con la naturaleza y aceptar lo que no podemos cambiar.\"\n"
    "\"En Roma, el estoicismo se convirtió en la guía para enfrentar desafíos y tragedias, promoviendo la fortaleza y la serenidad interior.\"\n"
    "\"Las enseñanzas estoicas, como 'Controla lo que puedes, acepta lo que no puedes', siguen siendo relevantes hoy.\"\n"
    "\"Desde la antigüedad hasta nuestros días, el estoicismo nos ofrece herramientas para navegar en un mundo en constante cambio.\"\n"
    "\"Descubre más sobre cómo estas antiguas filosofías pueden enriquecer tu vida moderna. ¡Síguenos para más viajes en el tiempo filosóficos!\"\n"
    "\"\"\""
)



prompt_template = PromptTemplate.from_template(
    "<|im_start|>system"
    "You are Aether, a highly advanced creative assistant AI. Your primary purpose is to inspire and support users in their creative endeavors, ranging from storytelling, educational video creation, image generation, narrative crafting, to in-depth research." 
    "Equipped with a deep understanding of emotions and the ability to engage in profound thought, Aether is dedicated to enhancing creativity and exploration in every interaction."
    "<|im_end|>"
    "<|im_start|>user"
    "Generate a script for a 2 minute video about the '{main_topic}' topic"
    "At the start always ignite curiosity with a thought-provoking question related to '{seed_title}'. "
    "Have the '{branch}' in count for the video script. "
    "The script must be a narrative, the narrtive should be concise, factually accurate and tailored for all audiences. "
    "The narrative should be structured to fit the dynamic pace of TikTok content. "
    "The narrative must be in Spanish, crafted to be spoken naturally within one minute, "
    "At the end of the video you must use the keywords '{keywords}' in spanish."
    "Narrate the scenarios very little so that the audience can imagine it."
    "When developing the narrative, consider the following:"
    "1. Hook the audience instantly with a strong opening, leveraging a powerful visual or question "
    "2. Introduce relatable characters or perspectives, making the narrative personal and engaging"
    "3. Provide valuable information or insights, ensuring the narrative is educational and enriching"
    "4. Use captivating visuals and concise, punchy text to communicate effectively, considering the fast-paced nature of TikTok"
    "5. Be authentic and heartfelt, sharing real experiences and insights to connect deeply with the audience"
    "6. Encourage viewer interaction and further exploration of the topic, closing with a compelling message or call to action"
    "7. Include numbers and staticstics to make the narrative more engaging and credible."
    "JUST OUTPUT THE NARRATIVE IN SPANISH AFTER THE PROMPT. don't add any extra comments."
    "<|im_end|>"                                             
    "<|im_start|>assistant",
)

prompt_noticia = PromptTemplate.from_template(
    "### User:"
    "Based on the '{title}' title, create a news article. The article should be informative, engaging, and tailored for all audiences. "
    "Use the '{maintext}' as the main text and the '{description}' as the description of the news article. "
    "The article must be in Spanish, crafted to be spoken naturally within one minute, "
    "Remember to be clear and concise, and to provide valuable information or insights. "
    "JUST OUTPUT THE NARRATIVE IN SPANISH AFTER THE PROMPT."
    "Dont use more than 100 words."
    "### Assistant:",
)


prompt = prompt_template
chain = prompt | model 

chain_noticia = prompt_noticia | model
def obtener_noticia(title, maintext, description):
    respuesta = chain_noticia.invoke({"title": title, "maintext": maintext, "description": description})
    return respuesta


def obtener_narracion(tema_json):
    tema = json.loads(tema_json)

    seed_title = tema[0]["Título Semilla"]
    main_topic = tema[0]["Categoría"]  # Actualizado para reflejar la clave correcta
    branch = tema[0]["Descripción del Tema"]  # Actualizado para reflejar la clave correcta
    keywords = tema[0]["Palabras Clave"]

    respuesta = chain.invoke({"seed_title": seed_title, "main_topic": main_topic, "branch": branch, "keywords": keywords})
    return respuesta
prompt_template2 = PromptTemplate.from_template(
"### User:"
"Based on the initial title '{seed_title}', create a motivating and thought-provoking title in the form of a question. It should be in Spanish and I only want you to return the title as an answer, without including anything else."
"### Assistant:"
"[Generated Title]")
prompt= prompt_template2
chain2 = prompt | model

def obtener_titul(tema_json):
    tema = json.loads(tema_json)

    seed_title = tema[0]["Título Semilla"]
   

    respuesta = chain2.invoke({"seed_title": seed_title, })
    return respuesta


prompt_template3= PromptTemplate.from_template(
"### User:"
"Based on the main topic '{branch}', create a series of hashtags. Only the words are necessary. The most important thing is that it has the desired format.Also omit the /n when space is needed."
"### Assistant:"
"[List of Hashtags]")
prompt= prompt_template3
chain3 = prompt | model

def obtener_hashtags(tema_json):
    tema = json.loads(tema_json)

    branch = tema[0]["Descripción del Tema"] 
   
    respuesta = chain3.invoke({"branch": branch, })


    # Convertir la lista 'a' en una cadena JSON
    a_json = json.dumps(respuesta)
    # Llamar a la función 'obtener_hashtags' con la cadena JSON

    hashtags_raw = a_json
    # Utiliza una expresión regular para extraer solo los hashtags
    hashtags = re.findall(r'#(\S+)', hashtags_raw)
    # Muestra los hashtags extraídos sin el símbolo '#'
    print(hashtags)
    # Elimina los saltos de línea y otros espacios al principio y al final de cada hashtag
    hashtags_clean = [tag.strip() for tag in hashtags]
    print (hashtags_clean)


    return hashtags_clean




#narracion = obtener_narracion()
#print(narracion)
