# Base image
FROM python:3.x

# Set environment variables
ARG SCRAPEOPS_API_KEY
ARG OPENAI_API_KEY
ENV SCRAPEOPS_API_KEY=$SCRAPEOPS_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["python", "precedent_parser.py"]
