FROM python:3.9
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y gcc build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade openai

EXPOSE 5000

CMD ["python","-u", "app.py"]
