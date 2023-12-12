import openai
import json
import boto3
import os
import sentry_sdk
from flask import Flask, request, jsonify, make_response


sentry_sdk.init(
    dsn=os.environ['SENTRY_DNS'],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)

app = Flask(__name__)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route('/flask-health-check')
def flask_health_check():
    return "success"


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


@app.route("/prepare", methods=['POST'])
def prepare():
    # https://platform.openai.com/docs/guides/fine-tuning
    data = request.get_json()
    bucket_name = os.environ['AWS_BUCKET']
    openai.api_key = os.environ['OPENAI_API_KEY']

    print(data, flush=True)

    file_key = data['file_key']
    user_id = data['user_id']
    base_model = data['model']

    base_dir = "/tmp/{}".format(str(user_id))

    os.system("rm {} -rf".format(base_dir))

    os.system("mkdir -p {}".format(base_dir))

    train_file_base = "dataset-{}".format(str(user_id))
    train_file = "{}/{}.csv".format(base_dir, train_file_base)

    # Create an S3 client
    s3 = boto3.client('s3')

    # Download the file
    response = s3.get_object(Bucket=bucket_name, Key=file_key)

    # Get the file content
    file_content = response['Body'].read()

    # write it to a local file
    with open(train_file, 'wb') as file:
        file.write(file_content)

    prepare_command = "openai tools fine_tunes.prepare_data -f \"{}\" -q".format(
        train_file)

    print(prepare_command, flush=True)

    prepare_command_stream = os.popen(prepare_command)
    prepare_command_output = prepare_command_stream.read()

    print(prepare_command_output, flush=True)

    openai_training_files_response = openai.File.create(
        file=open("{}/{}_prepared.jsonl".format(base_dir, train_file_base), "rb"),
        purpose='fine-tune'
    )

    print(openai_training_files_response, flush=True)

    openai_finetune_response = openai.FineTune.create(
        training_file=openai_training_files_response['id'],
        model=base_model,
        suffix=train_file_base
    )

    print(openai_finetune_response, flush=True)

    body = {
        "message": "Function executed successfully!",
        "file_key": file_key,
        "user_id": user_id,
        "prepare_command_output": prepare_command_output,
        "openai_training_files_response": openai_training_files_response,
        "openai_finetune_response": openai_finetune_response,
    }

    return jsonify(body)


@app.route("/sync-wandb", methods=['POST'])
def sync_wandb():

    sync_command = "openai wandb sync"

    print(sync_command, flush=True)

    sync_command_stream = os.popen(sync_command)
    sync_command_output = sync_command_stream.read()

    print(sync_command_output, flush=True)
    body = {
        "message": "Function executed successfully!",
        "sync_command_output": sync_command_output
    }

    return jsonify(body)
