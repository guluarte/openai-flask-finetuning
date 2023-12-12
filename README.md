# Flask OpenAI

Flask application designed to streamline the process of preparing and submitting fine-tuning jobs to OpenAI. The application accepts POST requests containing user information and a dataset file stored in an AWS S3 bucket. It then prepares the data for fine-tuning, submits the fine-tuning job to OpenAI, and returns the responses from OpenAI. The application is designed to handle individual user datasets separately, ensuring data integrity and isolation.

## Features

- Root endpoint (`/`) that returns a JSON message.
- Health check endpoint (`/flask-health-check`) that returns a success message.
- Error handler for 404 errors.
- `/prepare` endpoint that accepts POST requests and processes JSON data.
- `/sync-wandb` endpoint that syncs with Weights & Biases (wandb) and returns the output of the sync command.

## Environment Variables

- `SENTRY_DNS`: Your Sentry DSN for error tracking.

## Setup

1. Clone the repository.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Set the environment variables.
4. Run the application using `python app.py`.

## Docker Setup

1. Build the Docker image from the Dockerfile:

```bash
docker build -t openaituneprep .

```

2. Run the Docker container:

```bash
docker run -p 5000:5000 openaituneprep
```
This will start the application and expose it on port 5000.

Please ensure Docker is installed and running on your machine before executing these commands.

### Environment Variables
When running the Docker container, you can pass environment variables using the -e option:

```bash
docker run -p 5000:5000 -e SENTRY_DNS=<your_sentry_dns> -e AWS_BUCKET=<your_aws_bucket> -e OPENAI_API_KEY=<your_openai_api_key> openaituneprep
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)