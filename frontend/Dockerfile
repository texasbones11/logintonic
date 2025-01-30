# Use the official Node.js image.
FROM node:16

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the app
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Serve the application
CMD ["npx", "serve", "-s", "build"]
