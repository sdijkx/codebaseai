# Use an official Python image
FROM python:3.11-slim

#Install 
RUN apt update
RUN apt install -y astyle

# Set working directory inside container
WORKDIR /app
RUN mkdir -p /app/project
RUN mkdir -p /app/java_project
RUN mkdir -p /app/reports

# Copy installation and run script for testing
COPY ./install-and-run.sh /app/
RUN chmod +x /app/install-and-run.sh

# Default command runs a shell, you can override when running
CMD ["bash"]

