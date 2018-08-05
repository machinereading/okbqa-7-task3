from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow as tf
import coref_model as cm
import util

if __name__ == "__main__":
  config = util.initialize_from_env()
  model = cm.CorefModel(config)
  #tf_config = tf.ConfigProto(device_count = {'GPU': 0})
  gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
  with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as session:
    model.restore(session)
    model.evaluate(session, official_stdout=True)
