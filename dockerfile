FROM node:14

WORKDIR /app

# Copy and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your project files
COPY . .

# Start your project
CMD node--version && python--version && pip --version && ["npm", "start"]
