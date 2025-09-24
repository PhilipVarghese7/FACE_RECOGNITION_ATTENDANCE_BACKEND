import numpy as np
from insightface.app import FaceAnalysis
from PIL import Image

# -----------------------------
# Initialize InsightFace model
# -----------------------------
app = FaceAnalysis(allowed_modules=["detection", "recognition"])
app.prepare(ctx_id=0)  # ctx_id=0 uses GPU, use -1 for CPU


# -----------------------------
# Convert uploaded file to RGB array
# -----------------------------
def img_to_rgb_array(file):
    image = Image.open(file)
    image = image.convert("RGB")
    return np.array(image)


# -----------------------------
# Pick the largest face from detected faces
# -----------------------------
def largest_face(faces):
    if not faces:
        return None
    # Use bounding box area to find largest face
    largest = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    return largest


# -----------------------------
# Compute cosine similarity between two embeddings
# -----------------------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
