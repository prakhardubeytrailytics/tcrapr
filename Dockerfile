FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

RUN apt-get update && apt-get install -y xvfb

WORKDIR /app
COPY . .
RUN chmod +x entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install

ENV DISPLAY=:99
EXPOSE 8080
CMD ["./entrypoint.sh"]
