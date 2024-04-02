from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
import re, random

# Формирует промпт и делает запрос. Возвращает ответ LLM
def stoic_message(system, user_input, llm):

    # system - текст системного промпта
    # user_input - текст пользовательского промпта
    # llm - llm модель

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"{system}"),
        ("user", "{input}")
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    response = chain.invoke({"input" : f"{user_input}"})

    return response

# Возвращает ссылку на сгенерированное изображение
def image_generator(llm_image, image_desc, style):
    
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        template= f"Generate a prompt with length less than 950 symbols to generate an image without text and not detailed faces in {style} style based on the following description:" + "{image_desc}.",
    )
    chain = LLMChain(llm=llm_image, prompt=prompt)
    image_url = DallEAPIWrapper(model="dall-e-3").run(chain.run(f"{image_desc}"))

    return image_url

# Возвращает рандомную цитату и удаляет выбранный элемент из словаря
def quote_chooser(stoic_dict):
    
    # stoic_dict - словарь писатель-книга-цитата

    while True:
        
        if len(stoic_dict) > 0:
            random_stoic = random.choice(list(stoic_dict.keys()))
            if len(stoic_dict[random_stoic]) > 0:
                random_book = random.choice(list(stoic_dict[random_stoic].keys()))
                if len(stoic_dict[random_stoic][random_book]) > 0:
                    random_quote = random.choice(stoic_dict[random_stoic][random_book])
                    remove_quote = random_quote
                    stoic_dict[random_stoic][random_book].remove(remove_quote)
                    return random_stoic, random_book, random_quote
                else: 
                    del stoic_dict[random_stoic][random_book]
            else:
                stoic_dict[random_stoic]
        else:
            break

# Возвращает рандомный стиль из списка
def get_style(styles):
    random_style = random.choice(styles)
    return random_style

# Возвражает цитату из текста, выделенную жирным
def get_citation(text, tag):
    pattern = f'<{tag}>(.*?)</{tag}>'
    return re.findall(pattern, text)