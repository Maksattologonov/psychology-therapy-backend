FROM python:3.8
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR .
# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "accounts/main.py"]