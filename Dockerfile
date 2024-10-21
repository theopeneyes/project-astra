FROM python:3.11.9-slim-bookworm
ADD . /

RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential
RUN apt-get -y update && apt-get -y install curl
RUN apt-get install -y poppler-utils 

RUN make install 
RUN make lint
RUN make serve && make test 

CMD ["streamlit", "run"]
ENTRYPOINT [ "app.py" ]
EXPOSE 8501