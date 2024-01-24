FROM python:3.10-slim

RUN mkdir app

COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r ./requirements.txt;

COPY ./app ./app

WORKDIR /app

#CMD ["python", "./tests/start_tests.py"]
ENTRYPOINT ["uvicorn", "--reload", "app:app", "--host", "0.0.0.0", "--port", "8000"]
