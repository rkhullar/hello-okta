FROM python:3.9-slim
WORKDIR /root
COPY Pipfile ./
RUN pip install pipenv                           \
    && pipenv lock                               \
    && pipenv requirements > requirements.txt    \
    && pip install -r requirements.txt           \
    && rm requirements.txt
COPY *.py ./
COPY util/ util/
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
