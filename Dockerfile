FROM tensorflow/tensorflow:latest-py3

# update the package installer
RUN pip3 install flask flask-basicauth

COPY --chown=root:root code/classify_image_api.py /tmp/
COPY --chown=root:root IncV3_Retr_artifacts/pestsClassifier/* /tmp/

EXPOSE 5000
CMD ["python","/tmp/classify_image_api.py","--graph","/tmp/pests_IncV3_2.pb","--labels","/tmp/pests_IncV3_2_labels.txt"]