FROM python:3.10-slim AS compile-image

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY services/mailing_service/deploy/requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim AS build-image
COPY --from=compile-image /opt/venv /opt/venv

WORKDIR /app
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app"

WORKDIR /app/services/mailing_service
CMD ["python", "app.py"]
