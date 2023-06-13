# Stage 1: Node.js build
FROM node:14 AS node_builder

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the project files to the working directory
COPY . .

# Stage 2: Python runtime
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the built Node.js application from the previous stage
COPY --from=node_builder /app /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your Express application runs (replace 3000 with your desired port)
EXPOSE 3000

# Specify the command to run your application
CMD [ "npm", "start" ]
