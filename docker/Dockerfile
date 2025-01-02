FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Required to make sqlite3 work for Chroma with AWS Lambda
RUN pip install pysqlite3-binary

RUN pip install -r requirements.txt --upgrade

EXPOSE ${PORT}

ENV IS_DOCKER=True

COPY app/ ${LAMBDA_TASK_ROOT}/app
COPY resources/ ${LAMBDA_TASK_ROOT}/resources

ENV PYTHONPATH=${LAMBDA_TASK_ROOT}:${LAMBDA_TASK_ROOT}/app

CMD ["app.api.handler"]
