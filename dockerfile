FROM node:14

RUN node --version

RUN python --version

RUN pip --version

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy and install Node.js dependencies
COPY package.json .
COPY package-lock.json .
RUN npm install

# Copy the rest of your project files
COPY . .

# Start your project
CMD ["npm", "start"]
