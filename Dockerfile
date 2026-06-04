FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Jupyter and other tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file if it exists
COPY requirements.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir jupyter jupyterlab ipython \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy application code
COPY . .

# Expose port 8081 for Jupyter
EXPOSE 8081

# Run Jupyter Lab on port 8081
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8081", "--no-browser", "--allow-root"]
