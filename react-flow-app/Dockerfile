FROM node:22.12.0-slim
WORKDIR /react-flow-app

ADD . ./

RUN npm install -y 

EXPOSE 4173

ENTRYPOINT npm run preview --host 


