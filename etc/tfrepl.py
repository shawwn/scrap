# https://github.com/prompt-toolkit/ptpython
import sys
import os
import code
import numpy as np
import tensorflow as tf
import tensorflow.compat.v1 as tf1

from tensorflow.python.tpu import tpu as tpu_ops
from tensorflow.compiler.tf2xla.python import xla
from tensorflow.compiler.tf2xla.ops import gen_xla_ops

from tensorflow.core.protobuf import config_pb2
import tensorflow as tf
import numpy as np

from tensorflow.python.platform import test

mock = test.mock

from contextlib import contextmanager

@contextmanager
def monkeypatch(cls, method_name, new_method):
  pass

def interact():
  code.InteractiveConsole(locals=globals()).interact()



session_config = config_pb2.ConfigProto(allow_soft_placement=True, isolate_session_state=True)
master = None
cluster = None
cluster_spec = None
if 'TPU_NAME' in os.environ:
  res = resolver.TPUClusterResolver(os.environ['TPU_NAME'])
  master = res.get_master()
  cluster_spec = res.cluster_spec()
if cluster_spec:
  cluster = cluster_spec.as_cluster_def()
  session_config.cluster_def.CopyFrom(cluster_spec.as_cluster_def())
graph = tf.Graph()
sess = tf.compat.v1.InteractiveSession(master, graph=graph, config=session_config)
devices = sess.list_devices()
num_cores = len([x for x in devices if ':TPU:' in x.name])
print(cluster)
print('ip: %s', master, num_cores)
r = sess.run
s = sess
g = sess.graph



# try:
#     from ptpython.repl import embed
# except ImportError:
#     print("ptpython is not available: falling back to standard prompt")

# else:
#     sys.exit(embed(globals(), locals()))

