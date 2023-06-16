FROM node:latest

# Install Python 3.9
RUN apt update
RUN apt install python3 -y

RUN apt-get -y install python3-pip

RUN pip3 install -r requirements.txt

WORKDIR /app

# Copy and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your project files
COPY . .

# Start your project
CMD node --version && python3 --version && pip3 --version && ["npm", "start"]
