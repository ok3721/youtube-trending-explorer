FROM python:3.10-slim-buster

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5000"]
