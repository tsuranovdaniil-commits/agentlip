# Base image
FROM alpine:latest

# Set working directory
WORKDIR /app

# Copy application files
COPY README.md /app/README.md

# Default command
CMD ["cat", "/app/README.md"]
