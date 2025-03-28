FROM python:3.11-slim

RUN pip install gpiod

COPY kuma_control.py /kuma_control.py

CMD ["python", "/kuma_control.py"]
