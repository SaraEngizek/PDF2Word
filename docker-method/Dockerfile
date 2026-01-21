# OCR Converter - Fully Portable Docker Image
# Build once, run anywhere (Windows, macOS, Linux)

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tur \
    tesseract-ocr-eng \
    tesseract-ocr-deu \
    tesseract-ocr-fra \
    tesseract-ocr-spa \
    tesseract-ocr-ita \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libqt6widgets6 \
    libqt6gui6 \
    libqt6core6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY src/ ./src/
COPY assets/ ./assets/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set display for GUI
ENV DISPLAY=:0

# Run application
CMD ["python", "src/main.py"]
