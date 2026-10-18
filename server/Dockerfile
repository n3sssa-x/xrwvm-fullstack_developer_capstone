FROM python:3.12.0-slim-bookworm
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP=/app
# Change the workdir.
WORKDIR $APP
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential libpq-dev git && rm -rf /var/lib/apt/lists/*
# Copy requirements and install
COPY requirements.txt $APP/
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
# Copy the rest of the files
COPY . $APP
EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi:application"]
