FROM python:3.11.9-slim-bookworm
WORKDIR /app
ADD . ./

RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential
RUN apt-get -y update && apt-get -y install curl
RUN apt-get install -y poppler-utils 

RUN pip install -r requirements.txt 
EXPOSE 8080 
CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]