FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./project ./project
EXPOSE 3000
CMD ["python", "project/app.py"]
