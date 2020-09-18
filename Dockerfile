FROM python:3.8.5-slim-buster
RUN apt update -y
RUN apt install curl -y

WORKDIR /app

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.19.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl && mv ./kubectl /bin/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app .

EXPOSE 80
CMD [ "python", "k8sui.py" ]
