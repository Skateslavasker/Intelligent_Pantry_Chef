FROM python:3.10-slim 

WORKDIR /app 

COPY auth_server.py .



RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir fastapi uvicorn python-jose authlib starlette itsdangerous python-dotenv httpx

EXPOSE 8000


CMD ["uvicorn", "auth_server:app", "--host", "0.0.0.0", "--port", "8000"]