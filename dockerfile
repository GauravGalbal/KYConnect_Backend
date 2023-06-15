FROM node:latest

# Install Python 3.9
RUN apt update
RUN apt install python3.9 -y

# Install pip for Python 3.9
# RUN apt-get install -y python3.9-distutils
# RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# RUN python3.9 get-pip.py && rm get-pip.py
RUN apt install python3.9-distutils
RUN python3.9 get-pip.py --user

WORKDIR /app

# Copy and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your project files
COPY . .

# Start your project
CMD node --version && python3 --version && pip3 --version && ["npm", "start"]
