FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install requests
COPY ./app /app
COPY ./models /models
COPY .env .
RUN pip install python-dotenv
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/gunicorn_conf.py", "main:app"]