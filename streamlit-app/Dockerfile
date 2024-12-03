FROM python:3.11.9-slim-bookworm

WORKDIR /streamlit-app 

ADD . ./

EXPOSE 8051 

RUN pip install -r requirements.txt 

ENTRYPOINT streamlit run test_app.py  