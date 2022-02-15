FROM python:3.10
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR .
# Install dependencies
COPY requirements.txt /requirements.txt
RUN python3.10 -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "main.py"]