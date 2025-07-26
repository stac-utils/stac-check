FROM python:3.9-slim

WORKDIR /app

# Install build tools and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Install the package in development mode with dev and docs extras
RUN pip install -e ".[dev,docs]"

CMD ["stac_check"]