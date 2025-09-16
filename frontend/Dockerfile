# Use Node.js 24
FROM node:24-alpine

# Set working directory in container
WORKDIR /app

# Copy package
COPY package*.json ./

# install
RUN npm install

# Copy all project code
COPY . .

# port 5173 
EXPOSE 5173

# start Vite dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]