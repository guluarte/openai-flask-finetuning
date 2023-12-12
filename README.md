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

## Testing

This application uses unit tests for testing. Run the tests using `python -m unittest`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)