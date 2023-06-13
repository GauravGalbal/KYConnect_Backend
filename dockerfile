# Stage 1: Python build
FROM python:3.9 AS python_builder

# Set the working directory
WORKDIR /app

# Copy the Python dependencies files to the working directory
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the working directory
COPY . .

# Stage 2: Node.js runtime
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the built Python application from the previous stage
COPY --from=python_builder .

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Expose the port on which your Express application runs (replace 3000 with your desired port)
EXPOSE 8000

# Specify the command to run your application
CMD [ "npm", "start" ]
