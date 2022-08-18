FROM python:slim
ADD python.py /
RUN python -m ensurepip --upgrade
RUN python -m pip install requests
RUN python -m pip install boto3
ENV AWS_DEFAULT_REGION=eu-central-1
CMD [ "python", "./python.py" ]
