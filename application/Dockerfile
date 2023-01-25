FROM python:3.10.6
WORKDIR /application
COPY . .
EXPOSE 80
RUN pip install --no-cache-dir --upgrade -r /application/requirements.txt
WORKDIR /application/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
