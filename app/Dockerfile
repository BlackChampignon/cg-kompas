######## base ########
FROM python:3.12 AS base

# Installing required header packages
RUN apt update && apt install -y \
  python3-dev \
  libpq-dev  \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copying only the files required at this stage.
# The rest will be copied only for the prod environment
# since for dev env, the entire app directory
# will be mapped to the host file system.
COPY requirements-frozen.txt .
COPY docker-entrypoint-dev.sh .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r ./requirements-frozen.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000


######## dev ########
FROM base AS dev
# RUN chmod +x /app/docker-entrypoint-dev.sh
ENTRYPOINT ["./docker-entrypoint-dev.sh"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]


######## build ########
FROM base AS build
COPY ./ /app/
#RUN python manage.py collectstatic --noinput


######## prod ########
FROM build AS prod
COPY --from=build /app /app
ENTRYPOINT ["./docker-entrypoint-prod.sh"]
# CMD ["gunicorn", "sams.wsgi:application", "--workers", "2", "--bind", "0.0.0.0:8000"]
