FROM node:latest

# Install Python 3.9
RUN apt update
RUN apt install python3 -y

RUN apt-get -y install python3-pip

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app

# Copy and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your project files
COPY . .

# Start your project
CMD ["npm", "start"]
