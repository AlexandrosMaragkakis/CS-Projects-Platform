# change later to more recent version
FROM python:3.9-slim 

WORKDIR /flask-app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt






CMD ["python", "run.py", "--reload"]
