import telebot, os, schedule, time, quotes_dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from stoic_quotes import stoic_message, quote_chooser, image_generator, get_citation, get_style

print("Bot started")

# Отравка поста
def send_message():
    
    load_dotenv()
    bot_token = os.environ.get("SENDER_BOT_TOKEN")
    bot = telebot.TeleBot(bot_token)
    open_ai_key = os.environ.get("OPENAI_API_KEY")
    llm_stoic_message = ChatOpenAI(model = "gpt-4-turbo-preview", openai_api_key = open_ai_key, temperature = 0.3)
    #llm_image = OpenAI(openai_api_key = open_ai_key, temperature = 0.4)

    random_stoic, random_book, random_quote = quote_chooser(quotes_dict.stoic_dict)
    #style = get_style(quotes_dict.styles)

    system = f"Вы философ. Предоставьте короткий комментарий по цитате и фразе. Комментарий должен быть понятным и доступным, кратким.\
             Избегай биографии, но укажи кто автор цитаты и её источник. Не описывай кто автор цитаты. Сосредоточься только на цитате.\
             Избегай введение в комментарии, клишированных фраз ('в современном мире', 'в эпоху социальных сетей', 'в эпоху' и т.д.); фраз,\
             что циатата/идея является центральной, основной ключевой и т.д. Не пишите 'цитата:', 'Комментарий:'."
    user_input = f"Сделай комментарии |comment| о цитате {random_quote}. Если цитата или фрагмент длиннее 4 предложений,\
            то сократи её, вычленив главную мысль не меняя текст с длинной менее 4 предложений.\
            Цитату |quote| переведи на русский. Общая длина ответа должна быть менее 900 знаков. Добавь несколько эмоджи среди текста комментария.\
            Ответ должен иметь вид с разметкой html:\
             <b>|quote|</b>. \n\n <i>–{random_stoic}, {random_book}</i> \n\n <b>Комментарий</b> \n |comment|"
    
    stoic_message_output = stoic_message(system, user_input, llm_stoic_message)

    #quote = get_citation(stoic_message_output, "b")
    #quote = " ".join(quote)

    #image_url = image_generator(llm_image, quote, style)    

    bot.send_message(-1001999833879, text=stoic_message_output, parse_mode="HTML")
    #bot.send_photo(-1001999833879, photo=image_url, caption=stoic_message_output, parse_mode="HTML")

# Schedule the message to be sent every day at 05:00 AM UTC
schedule.every().day.at("05:00").do(send_message)

# Main loop
while True:
    schedule.run_pending()
    time.sleep(60)  # Увеличение времени ожидания до 3600 секунд