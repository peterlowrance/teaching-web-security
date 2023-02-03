FROM python:3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY attacking-website ./attacking-website
COPY vulnerable-bank ./vulnerable-bank
COPY start-attack-and-bank.sh .

EXPOSE 8080
EXPOSE 8081

CMD [ "sh", "start-attack-and-bank.sh" ]