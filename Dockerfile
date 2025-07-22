FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

# Install Xvfb (virtual display)
RUN apt-get update && apt-get install -y xvfb

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Set permissions for entrypoint
RUN chmod +x entrypoint.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set display environment variable
ENV DISPLAY=:99

# Expose HTTP server port
EXPOSE 8080

# Entrypoint
CMD ["./entrypoint.sh"]
