FROM python:3.8.6

WORKDIR /code

COPY . .

RUN pip install -r ./requirements.txt

CMD ["Python", "hybridbot.py" ]