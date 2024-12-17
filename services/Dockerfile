FROM python:3.11-slim

WORKDIR /app

# Instalar solo las dependencias mínimas necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Configurar variables de entorno por defecto
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Puerto por defecto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]