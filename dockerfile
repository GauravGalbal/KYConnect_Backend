# Use the official Node.js 14 image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Install Python 3.7 and pip
RUN apt-get update && apt-get install software-properties-common && add-apt-repository ppa:deadsnakes/ppa
# Install py39 from deadsnakes repository
RUN apt-get install python3.9
# Install pip from standard ubuntu packages
RUN apt-get install python3-pip

# Install Node.js packages
COPY package*.json ./
RUN npm install

# Install Python libraries
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the working directory
COPY . .

# Set the default command to run 'npm start'
CMD ["npm", "start"]
