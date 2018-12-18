# ImageClassification API
# authored by Scott Queen
# start date: 12/15/18
#
#
# Using snippets from Tensorflow code that is
# licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np
import tensorflow as tf
from flask import Flask, Response, request
from flask_basicauth import BasicAuth

import threading
import datetime
import time
import json


def timestamp_for_logging():
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    return ts


# App Globals (do not edit)
app = Flask(__name__)


@app.route('/health')
def health_check():
    print(timestamp_for_logging(), ': request made to health_check')
    response = {'service': 'PestClassifierService',
                'time': timestamp_for_logging(),
                'status': 'All Good Here!'}
    return Response(json.dumps(response), status=200)


@app.route('/ci', methods=['POST'])
def classify_image():
    print(timestamp_for_logging(), ': request made to classify_image')

    image = request.data
    print(timestamp_for_logging(), ': received image')

    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    input_layer = "Placeholder"
    output_layer = "final_result"

    t = read_tensor_from_image_file(
        image,
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

    print(timestamp_for_logging(), ': successfully created tensor from image data')

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: t
        })
    results = np.squeeze(results)

    top_k = results.argsort()[-3:][::-1]

    response = {}
    probabilities = {}
    for i in top_k:
        print(labels[i], results[i])
        probabilities[labels[i]] = "{0:.3f}".format((results[i]))

    response['probabilities'] = probabilities
    return Response(json.dumps(response), status=200)


def load_graph(model_file):
    print(timestamp_for_logging(), ': loading image-classification graph')
    g = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with g.as_default():
        tf.import_graph_def(graph_def)

    return g


def read_tensor_from_image_file(image,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):

    image_reader = tf.image.decode_image(image)
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)

    return result


def load_labels(label_file):
    print(timestamp_for_logging(), ': loading labels')
    labels_list = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        labels_list.append(l.rstrip())
    return labels_list


def run_web_server():
    print(timestamp_for_logging(), ': starting the web server')
    app.run(host='0.0.0.0', debug=False)


if __name__ == "__main__":
    global graph
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", help="graph/model to be executed")
    parser.add_argument("--labels", help="name of file containing labels")
    args = parser.parse_args()

    if args.graph:
        model_file = args.graph
    if args.labels:
        label_file = args.labels

    graph = load_graph(model_file)
    print(timestamp_for_logging(),': loaded image-classification graph')
    labels = load_labels(label_file)
    print(timestamp_for_logging(),': loaded image-classification labels')

    t = threading.Thread(target=run_web_server, args=())
    t.daemon = True
    t.start()

    # keep the app running so the web-server thread will stay alive
    while True:
        time.sleep(1)
