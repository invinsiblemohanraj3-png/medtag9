import pickle
import numpy as np
import cv2
from PIL import Image
import io
import math
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import Model

# ================= LOAD PKL =================
PKL_PATH = "implant_embeddings_resnet.pkl"

with open(PKL_PATH, "rb") as f:
    data = pickle.load(f)

EMBEDDINGS_DB = data["embeddings"]   # (N, 2048)
METADATA = data["metadata"]

# ================= LOAD RESNET MODEL (ONCE) =================
base_model = ResNet50(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D()
])

model.trainable = False

# ================= UTIL =================
def safe_float(value):
    if value is None or math.isnan(value) or math.isinf(value):
        return 0.0
    return float(value)

# ================= COSINE SIMILARITY =================
def cosine_similarity_tf(a, b):
    """
    a: (1, 2048)
    b: (N, 2048)
    """
    a = tf.nn.l2_normalize(a, axis=1)
    b = tf.nn.l2_normalize(b, axis=1)
    return tf.matmul(a, b, transpose_b=True)

# ================= IMAGE → EMBEDDING =================
def extract_embedding(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = np.array(image)

    image = cv2.resize(image, (224, 224))
    image = preprocess_input(image.astype(np.float32))
    image = np.expand_dims(image, axis=0)

    embedding = model(image, training=False).numpy()
    return embedding  # (1, 2048)

# ================= PREDICT =================
def predict_implant(image_bytes):
    query_embedding = extract_embedding(image_bytes)

    similarities = cosine_similarity_tf(
        query_embedding,
        tf.convert_to_tensor(EMBEDDINGS_DB)
    ).numpy()

    best_index = int(np.argmax(similarities))
    best_score = safe_float(similarities[0][best_index])

    result = METADATA[best_index]

    return {
        "model": result["model"].strip(),
        "manufacturer": result["manufacturer"].strip(),
        "confidence": best_score
    }
