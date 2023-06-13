# Stage 2: Node.js runtime
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Expose the port on which your Express application runs (replace 3000 with your desired port)
EXPOSE 8000

# Specify the command to run your application
CMD [ "npm", "start" ]
