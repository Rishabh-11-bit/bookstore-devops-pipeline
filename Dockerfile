FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir streamlit mysql-connector-python pandas numpy

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
