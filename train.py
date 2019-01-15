#!/usr/bin/env python

import os
import time

import tensorflow as tf
import coref_model as cm
import util
import numpy as np

if __name__ == "__main__":
  config = util.initialize_from_env()

  report_frequency = config["report_frequency"]
  eval_frequency = config["eval_frequency"]

  model = cm.CorefModel(config)
  saver = tf.train.Saver()

  log_dir = config["log_dir"]
  writer = tf.summary.FileWriter(log_dir, flush_secs=20)

  max_f1 = 0

  #tf_config = tf.ConfigProto(device_count = {'GPU': 0})
  gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)

  min_loss = 100000.0
  not_updated = 0
  with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as session:
    session.run(tf.global_variables_initializer())
    model.start_enqueue_thread(session)
    accumulated_loss = 0.0
    accumulated_origin_loss = 0.0
    accumulated_teacher_loss = 0.0


    ckpt = tf.train.get_checkpoint_state(log_dir)
    if ckpt and ckpt.model_checkpoint_path:
      print("Restoring from: {}".format(ckpt.model_checkpoint_path))
      saver.restore(session, ckpt.model_checkpoint_path)

    initial_time = time.time()
    while True:
      predictions, tf_loss, tf_global_step, _ = session.run([model.predictions, model.loss, model.global_step, model.train_op])

      #candidate_starts, candidate_ends, top_span_starts, top_span_ends, top_antecedents, top_antecedent_scores, teacher_loss, origin_loss, logic_value, top_antecedent_prob_with_logic, top_span_speaker_ids, top_span_fpronouns, top_antecedent_prob = predictions
      # logic_value, top_antecedent_prob_with_logic, top_span_speaker_ids, top_span_fpronouns = predictions
      '''
      np.set_printoptions(precision=2)
      print ('#top_antecedents')
      print (top_antecedents[0:9, 0:9])

      print ('#top_span_speaker_ids')
      print (top_span_speaker_ids[0:9])

      print ('#top_span_fpronouns')
      print (top_span_fpronouns[0:9])

      print ('#logic_value')
      print (logic_value[0:9, 0:10])


      print ('#top_antecedent_prob')
      print (top_antecedent_prob[0:9, 0:10])

      print ('#top_antecedent_prob_with_logic')
      print (top_antecedent_prob_with_logic[0:9, 0:10])

      print ('\n------\n')
      '''

      accumulated_loss += tf_loss

      origin_loss = predictions[-1]
      teacher_loss = predictions[-2]

      accumulated_origin_loss += origin_loss
      accumulated_teacher_loss += teacher_loss

      if tf_global_step % report_frequency == 0:
        total_time = time.time() - initial_time
        steps_per_second = tf_global_step / total_time

        average_loss = accumulated_loss / report_frequency
        average_origin_loss = accumulated_origin_loss / report_frequency
        average_teacher_loss = accumulated_teacher_loss / report_frequency

        print("[{}] loss={:.2f}, origin_loss={:.2f}, teacher_loss={:.2f}, steps/s={:.2f}".format(tf_global_step, average_loss, average_origin_loss, average_teacher_loss, steps_per_second))
        writer.add_summary(util.make_summary({"loss": average_loss}), tf_global_step)
        accumulated_loss = 0.0
        accumulated_origin_loss = 0.0
        accumulated_teacher_loss = 0.0

      if tf_global_step % eval_frequency == 0:
        saver.save(session, os.path.join(log_dir, "model"), global_step=tf_global_step)
        eval_summary, eval_f1, eval_loss = model.evaluate(session)

        if eval_f1 > max_f1 or eval_loss < min_loss:
          if eval_f1 > max_f1:
            max_f1 = eval_f1
          if eval_loss < min_loss:
            min_loss = eval_loss
          util.copy_checkpoint(os.path.join(log_dir, "model-{}".format(tf_global_step)), os.path.join(log_dir, "model.max.ckpt"))
          not_updated = 0
        else:
          not_updated += 1

        writer.add_summary(eval_summary, tf_global_step)
        writer.add_summary(util.make_summary({"max_eval_f1": max_f1}), tf_global_step)

        print("[{}] evaL_f1={:.2f}, max_f1={:.2f}".format(tf_global_step, eval_f1, max_f1))
        print("[{}] evaL_loss={:.2f}, min_loss={:.2f}".format(tf_global_step, eval_loss, min_loss))
        print("")

      if (not_updated == 20):
        break
      
      if (tf_global_step == 4500):
        break
