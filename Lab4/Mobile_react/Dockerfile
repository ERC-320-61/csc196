# Use a Node.js base image
FROM node:18

# Install Android dependencies
RUN apt-get update && \
    apt-get install -y default-jdk wget unzip && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip -O cmdline-tools.zip && \
    unzip cmdline-tools.zip -d /cmdline-tools && \
    rm cmdline-tools.zip && \
    mkdir -p /android/cmdline-tools && \
    mv /cmdline-tools/cmdline-tools /android/cmdline-tools/latest && \
    yes | /android/cmdline-tools/latest/bin/sdkmanager --licenses && \
    /android/cmdline-tools/latest/bin/sdkmanager "platform-tools" "platforms;android-30"

# Set environment variables
ENV ANDROID_HOME=/android
ENV PATH=$PATH:/android/platform-tools:/android/cmdline-tools/latest/bin

# Set working directory
WORKDIR /app

# Initialize a new React Native project
RUN npx react-native init mobileCalculator

# Change directory to the newly created project
WORKDIR /app/mobileCalculator

# Copy package.json and yarn.lock, then install all project dependencies
COPY package.json yarn.lock ./
RUN yarn install

# Debug: Check if react-native-svg-transformer is installed
RUN ls node_modules | grep 'react-native-svg-transformer' || echo 'react-native-svg-transformer not found'

# Copy the rest of the application code
COPY . .

# Copy metro.config.js to the mobileCalculator directory
COPY ../metro.config.js /app/mobileCalculator/

# Expose Metro Bundler port
EXPOSE 8081

# Start the Metro Bundler
CMD ["yarn", "start"]
