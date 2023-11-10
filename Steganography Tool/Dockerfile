FROM alpine:edge

RUN apk add --update py3-pip

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY app.py /usr/src/app/
COPY templates/ /usr/src/app/templates/
COPY steganography.py /usr/src/app/
COPY static/ /usr/src/app/static

EXPOSE 8080

CMD ["python3", "/usr/src/app/app.py"]
