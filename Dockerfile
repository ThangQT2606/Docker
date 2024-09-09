FROM python:3.11.7
WORKDIR /app
COPY . .
RUN apt-get update
RUN pip3 install -r requirements.txt
CMD [ "streamlit","run","app.py"]