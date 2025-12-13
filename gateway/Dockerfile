FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./project ./project
EXPOSE 5000
CMD ["python", "project/app.py"]
