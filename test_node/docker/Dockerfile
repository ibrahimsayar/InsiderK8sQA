FROM python:3
WORKDIR /usr/src/app
COPY ./test_controller/docker ./
RUN apt-get update && \
    apt-get install -y --no-install-recommends vim procps && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 80
EXPOSE 443
CMD ["python", "-u", "./test-case.py", "-v"]