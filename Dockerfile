# Build stage using Alpine
FROM docker.io/library/alpine:latest as builder

# Install git, npm, python3, and pip3
RUN apk add --no-cache git npm python3 py3-pip

# Install Python packages
RUN pip3 install uvicorn[standard] fastapi pydantic gunicorn

# Clone the repository and set the working directory
RUN git clone https://github.com/roar-emaus/bjorligames_react.git
WORKDIR /bjorligames_react/project

# Install npm dependencies and build the project
RUN npm install
RUN npm run build

# Final stage using Alpine
FROM docker.io/library/alpine:latest

# Install python3 and pip3
RUN apk add --no-cache python3 py3-pip

# Install Python packages
RUN pip3 install uvicorn[standard] fastapi pydantic gunicorn

# Copy necessary files from the build stage
COPY --from=builder /bjorligames_react/project/dist /bjorligames_react/project/dist
COPY --from=builder /bjorligames_react/data /bjorligames_react/data
COPY --from=builder /bjorligames_react/api.py /bjorligames_react/api.py

# Set the working directory and default command
WORKDIR /bjorligames_react
ENV DATA_PATH=/bjorligames_react/data/

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "api:app", "--bind", "0.0.0.0:80"]
