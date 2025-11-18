# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port your FastAPI application runs on
EXPOSE 8001


# Command to run the application using Uvicorn
# The --host 0.0.0.0 makes the server accessible from outside the container
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
CMD ["/bin/bash", "-c", "cd app  && uvicorn main:app --host 0.0.0.0 --port 8001"]