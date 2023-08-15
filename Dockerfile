FROM python:3.11-slim
COPY . /app/
EXPOSE 5000
WORKDIR /app/
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--reload", "--log-level=DEBUG", "kafc:create_app()"]