FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt --upgrade

EXPOSE ${PORT}

COPY app/ ${LAMBDA_TASK_ROOT}/app
COPY resources/ ${LAMBDA_TASK_ROOT}/resources
COPY .env ${LAMBDA_TASK_ROOT}/.env

ENV PYTHONPATH=${LAMBDA_TASK_ROOT}:${LAMBDA_TASK_ROOT}/app

CMD ["app.api.handler"]
