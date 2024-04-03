FROM python:3.11.3-alpine
RUN mkdir /sender_bot
WORKDIR /sender_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]