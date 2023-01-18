FROM python:3.10.6
WORKDIR /applction
COPY . .
EXPOSE 80
RUN pip install --no-cache-dir --upgrade -r /applction/requirements.txt
WORKDIR /applction/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
