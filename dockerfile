# Use a Node.js base image
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the project files to the working directory
COPY . .

# Install Python and necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir zbar opencv-python-headless numpy Pillow pyaadhaar xmltodict pytesseract psutil deepface pyzbar

# Expose the port on which your Express application runs (replace 3000 with your desired port)
EXPOSE 8000

# Specify the command to run your application
CMD [ "npm", "start" ]
