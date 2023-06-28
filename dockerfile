FROM node:latest

# Install Python 3.9
RUN apt update
RUN apt install python3 -y

RUN apt-get -y install python3-pip

RUN pip install pip==22.3.1 --break-system-packages

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

WORKDIR /app

# Copy and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your project files
COPY . .

CMD python --version

# Start your project
CMD ["npm", "start"]
