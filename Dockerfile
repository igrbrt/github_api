FROM python:3.10.12-alpine

ADD . /app

WORKDIR /app

RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]