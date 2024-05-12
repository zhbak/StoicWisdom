import telebot, os, schedule, time, quotes_dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from stoic_quotes import stoic_message, quote_chooser, image_generator, get_citation, get_style

print("Bot started")

# Отравка поста
def send_message():
    
    load_dotenv()
    bot_token = os.environ.get("TELEGRAM_TOKEN")
    bot = telebot.TeleBot(bot_token)
    open_ai_key = os.environ.get("OPENAI_API_KEY")
    llm_stoic_message = ChatOpenAI(model = "gpt-4-turbo-preview", openai_api_key = open_ai_key, temperature = 0.3)
    llm_image = OpenAI(openai_api_key = open_ai_key, temperature = 0.4)

    random_stoic, random_book, random_quote = quote_chooser(quotes_dict.stoic_dict)
    style = get_style(quotes_dict.styles)

    system = f"Вы философ. Предоставьте короткий комментарий по цитате и фразе. Комментарий должен быть понятным и доступным, кратким.\
             Избегай биографии, но укажи кто автор цитаты и её источник. Не описывай кто автор цитаты. Сосредоточься только на цитате.\
             Избегай введение в комментарии, клишированных фраз ('в современном мире', 'в эпоху социальных сетей', 'в эпоху' и т.д.); фраз,\
             что циатата/идея является центральной, основной ключевой и т.д. Не пишите 'цитата:', 'Комментарий:'.\
             Ответ должен иметь вид с разметкой html:\
             <b>Цитата</b>. \n\n <i>–{random_stoic}, {random_book}</i> \n\n <i>Жанр изображения: {style} 🎨</i> \n\n <b>Комментарий</b> \n Эмоджи."
    user_input = f"Предоставь комментарии о цитате {random_quote}. Напиши жанр ({style}) изображения на английском. Цитату приведи на русском. Если цитата или фрагмент длиннее 3 предложений,\
             то вычлени главную мысль не меняя текст с длинной менее 3 предложений. Общая длина ответа не должна превышать 900 знаков. Добавь несколько эмоджи среди текста."
    
    stoic_message_output = stoic_message(system, user_input, llm_stoic_message)

    quote = get_citation(stoic_message_output, "b")
    quote = " ".join(quote)

    image_url = image_generator(llm_image, quote, style)    

    bot.send_photo(-1002026682093, photo=image_url, caption=stoic_message_output, parse_mode="HTML")

# Schedule the message to be sent every day at 10:00 AM
schedule.every().day.at("08:00").do(send_message)

# Main loop
while True:
    schedule.run_pending()
    time.sleep(3600)  # Увеличение времени ожидания до 3600 секунд