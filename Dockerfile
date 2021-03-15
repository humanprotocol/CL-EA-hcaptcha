FROM python:alpine3.9
COPY . /app
WORKDIR /app
RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
ENV PYENV=prod
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
