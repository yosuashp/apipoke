# # Use the official Python image as base image
# FROM python:3.9-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container at /app
# COPY requirements.txt /app/

# # Install any needed dependencies specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code into the container
# COPY . /app/

# # Expose port 5000 to the outside world
# EXPOSE 5000

# # Command to run the application
# CMD ["python", "manage.py", "runserver", "-h", "0.0.0.0", "-p", "5000"]

# Gunakan image resmi Python
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory di dalam container
WORKDIR /app

# Install dependensi proyek
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Tambahkan direktori instalasi Gunicorn ke dalam PATH
ENV PATH="/usr/local/bin:${PATH}"

# Copy seluruh kode proyek ke dalam container
COPY . /app

# Copy konfigurasi New Relic
COPY newrelic.ini /app/newrelic.ini

# Menjalankan aplikasi Flask dengan New Relic
CMD ["newrelic-admin", "run-program", "gunicorn", "-b", "0.0.0.0:8080", "run:app"]

