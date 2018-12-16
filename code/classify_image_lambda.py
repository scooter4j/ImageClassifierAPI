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

import numpy as np
import tensorflow as tf

import datetime
import json
import os
import base64


def timestamp_for_logging():
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    return ts


def health_check():
    print(timestamp_for_logging(), ': request made to health_check')
    response = {}
    response['status'] = 'All Good Here!'
    return response


def load_graph(model_file):
    print(timestamp_for_logging(), ': loading image-classification graph')
    g = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with g.as_default():
        tf.import_graph_def(graph_def)

    return g


def load_labels(label_file):
    print(timestamp_for_logging(), ': loading labels')
    labels_list = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        labels_list.append(l.rstrip())
    return labels_list


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


def classify_image(image):
    print(timestamp_for_logging(), ': invoking classify_image')
    graph = load_graph('/var/task/classification_model/pests_IncV3_2.pb')
    print(timestamp_for_logging(), ': loaded image-classification graph')
    labels = load_labels('/var/task/classification_model/pests_IncV3_2_labels.txt')
    print(timestamp_for_logging(), ': loaded image-classification labels')

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
    return response


def classify_image(event, context):
    LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))
    CURR_BIN_DIR = os.path.join(LAMBDA_TASK_ROOT, 'bin')
    os.environ['PATH'] = os.environ['PATH'] + ':' + CURR_BIN_DIR

    print("LAMBDA_TASK_ROOT: ", LAMBDA_TASK_ROOT)
    print("CURR_BIN_DIR: ", CURR_BIN_DIR)
    print("path: ", os.environ['PATH'])
    base64_encoded_image = event.b64image
    print("base64_encoded_image: ", base64_encoded_image)

    print(timestamp_for_logging(), ': decoding received image')
    image = base64.b64decode(base64_encoded_image)

    print(timestamp_for_logging(), ': classifying image')
    classification = classify_image(image)
    response = json.dumps(classification)
    print(timestamp_for_logging(), ': results of image classification: ', response)
    return response
