FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "fastapi", "dev", "main.py", "--port", "80", "--host", "0.0.0.0" ]
