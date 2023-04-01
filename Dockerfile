FROM jupyter/scipy-notebook:python-3.8.13
RUN conda install xgboost
RUN conda install boto3
RUN conda install s3fs
RUN conda install lime
RUN conda install hyperopt
RUN conda install graphviz
RUN pip install torch torchvision torchtext --extra-index-url https://download.pytorch.org/whl/cpu
RUN conda install yellowbrick
RUN pip install mlflow
RUN pip install psycopg2-binary
ENV PYTHONPATH "${PYTHONPATH}:/home/jovyan/work"
WORKDIR /home/jovyan/work

