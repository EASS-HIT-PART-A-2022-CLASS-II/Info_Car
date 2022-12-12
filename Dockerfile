FROM python:3.10.6
WORKDIR /applction
COPY ./requirements.txt /applction/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /applction/requirements.txt
COPY ./main.py /applction/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]