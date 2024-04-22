FROM python:3.9-slim
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
CMD streamlit run main.py --server.port $PORT --server.enableCORS=false