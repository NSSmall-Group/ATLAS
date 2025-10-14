import tensorflow as tf
from tensorflow.python.compiler.tensorrt import trt_convert as trt

print("Loading model...")
model = tf.keras.models.load_model("output/ori_model.h5")



print("Saving as SavedModel format...")
model.save("output/saved_model", save_format="tf")

# 设置 TF-TRT 参数
print("Setting TF-TRT conversion parameters...")
params = trt.DEFAULT_TRT_CONVERSION_PARAMS._replace(
    precision_mode='FP16',
    max_workspace_size_bytes=1 << 28  # 256MB
)

# 创建转换器
saved_model_dir = "output/saved_model"
trt_model_dir = "output/trt_model"
print("Starting TF-TRT conversion...")

converter = trt.TrtGraphConverterV2(input_saved_model_dir=saved_model_dir, conversion_params=params)
converter.convert()

# 可选：提前构建 engine，避免第一次推理构建
def input_fn():
    yield tf.random.uniform([256, 400],minval=0, maxval=31, dtype=tf.float32)  # 替换为你的输入尺寸

converter.build(input_fn)

# 保存 TF-TRT 模型
converter.save(trt_model_dir)
print("TF-TRT model saved to:", trt_model_dir)

