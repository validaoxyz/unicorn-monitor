# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY exporter/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the exporter script
COPY exporter/validator_exporter.py .

# Expose the port the exporter listens on
EXPOSE 9300

# Set the entrypoint command
CMD ["python", "validator_exporter.py"]
