import insightface
import cv2
import numpy as np

# Initialize model once
model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=-1)  # CPU

def get_embedding(image_path_or_file):
    """
    Input: path to image or file-like object
    Output: 512-d embedding list or None
    """
    # Read image
    if hasattr(image_path_or_file, 'read'):  # InMemoryUploadedFile
        file_bytes = np.frombuffer(image_path_or_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_path_or_file.seek(0)  # reset pointer for Django ImageField
    else:
        img = cv2.imread(image_path_or_file)

    if img is None:
        return None

    faces = model.get(img)
    if faces:
        # Return first face embedding
        return faces[0].embedding.tolist()
    return None
