FROM python:3.11.9-slim-bookworm
WORKDIR /app
ADD . ./

RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential
RUN apt-get -y update && apt-get -y install curl
RUN apt-get install -y poppler-utils 

RUN pip install --no-cache-dir -r requirements.txt  
EXPOSE 8000 
CMD python3 -m uvicorn main:app --workers 10
