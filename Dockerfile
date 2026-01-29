# Use a specific Python 3.12 image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the app with Uvicorn (Shell form for variable expansion)
CMD uvicorn aap.main:app 