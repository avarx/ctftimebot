FROM python:3.6
ADD bot.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]