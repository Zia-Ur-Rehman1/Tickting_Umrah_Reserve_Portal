# FROM node:16 AS tailwind-builder
# WORKDIR /app
# COPY . .
# RUN npm install tailwindcss postcss-cli autoprefixer
# RUN npx tailwindcss build -o output.css

# COPY ./theme/static_src/package.json postcss.config.js ./theme/static_src/tailwind.config.js ./
# RUN npm install
# COPY ./theme/static/css/dist ./static/css/dist
# RUN npm run build-css

FROM python:3.11-slim-buster


ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install -r requirements.txt
# COPY --from=tailwind-builder /app/output.css /static/css/output.css

COPY . /app
WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
# COPY . .

# COPY --from=tailwind-builder /app/static/css/dist/styles.css ./theme/static/css/dist/styles.css
# CMD python manage.py runserver 0.0.0.0:80

# CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
