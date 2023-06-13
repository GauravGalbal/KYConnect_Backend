# Stage 1: Node.js build
FROM node:14 AS node_builder

# Set the working directory for Node.js build
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the project files to the working directory
COPY . .

# Stage 2: Python build
FROM python:3.9 AS python_builder

# Set the working directory for Python build
WORKDIR /app

# Copy the Python dependencies files to the working directory
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built Node.js application from the previous stage
COPY --from=node_builder /app .

# Stage 3: Application runtime
FROM node:14

# Set the working directory for the application runtime
WORKDIR /app

# Copy the built application from the previous stages
COPY --from=python_builder /app .

# Expose the port on which your Express application runs (replace 8000 with your desired port)
EXPOSE 8000

# Specify the command to run your application
CMD [ "npm", "start" ]
