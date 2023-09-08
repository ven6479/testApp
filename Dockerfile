FROM python:3.11.3

RUN apt-get update && apt-get install -y libldap2-dev libsasl2-dev libsasl2-modules

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]