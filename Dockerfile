FROM python:3.4-alpine
ENV IS_DOCKER=1
ADD . /todo
WORKDIR /todo
RUN pip install -r requirements.txt
RUN pip install pymongo

EXPOSE 80
EXPOSE 27017
EXPOSE 4000
CMD ["python","-u", "app.py"]