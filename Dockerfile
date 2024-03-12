# # Gunakan image resmi Python
# FROM python:3.9-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set working directory di dalam container
# WORKDIR /app

# # Install dependensi proyek
# COPY requirements.txt /app/requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Install gunicorn
# RUN pip install gunicorn

# # Tambahkan direktori instalasi Gunicorn ke dalam PATH
# ENV PATH="/usr/local/bin:${PATH}"

# # Copy seluruh kode proyek ke dalam container
# COPY . /app

# # Menjalankan aplikasi Flask
# CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]

FROM continuumio/miniconda3:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy environment file
COPY environment.yaml /app/environment.yaml

# Add conda-forge channel
RUN conda config --add channels conda-forge

# Add main and R channels
RUN conda config --add channels defaults
RUN conda config --add channels r

# Install conda environment
RUN conda env create -f environment.yaml

# Activate the created environment
SHELL ["conda", "run", "-n", "flask-template", "/bin/bash", "-c"]

# Copy the entire project code into the container
COPY . /app

# Install gunicorn using pip
RUN pip install gunicorn

# Install flask-sieve using pip
RUN pip install flask-sieve==2.0.1

# Install python-dateutil using pip
RUN pip install python-dateutil==2.9.0.post0

# Install flask-sqlalchemy using pip
RUN pip install flask-sqlalchemy==3.1.1

# Expose the port
EXPOSE 9090

# Run the Flask application
CMD ["conda", "run", "-n", "flask-template", "gunicorn", "-b", "0.0.0.0:9090", "run:app"]


