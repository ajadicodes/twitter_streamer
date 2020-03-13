# twitter_streamer

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Organisation](#project-organization)

## About

Used to download twitter messages in real time into mongodb.

## Getting Started

### Prerequisites

- anaconda
- .env file

#### Content of .env file

```text
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your access_token_secret

DB_NAME=your_preferred_database_name
```

## Usage

### Running the pipleine for the first time

```bash
make create_environment
```

```bash
conda activate twitter_streamer
```

### Update Python Dependencies

After update(s) to the requirement.yml:

```bash
make requirements
```

### Run Twitter Streamer

Keyword File format

sample.txt

```text
football
premier league
postponed
#livtot
```

```bash
make data keywords_file=sample.txt
```

--------

Project based on the [cookiecutter data science project template](https://github.com/gidigidiolu/cookiecutter-data-science).
