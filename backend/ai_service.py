import os
import cv2
import numpy as np
import base64
from collections import defaultdict
from insightface.app import FaceAnalysis

INSIGHTFACE_MODEL_NAME = os.getenv("INSIGHTFACE_MODEL_NAME", "buffalo_l")
INSIGHTFACE_DET_SIZE = int(os.getenv("INSIGHTFACE_DET_SIZE", "320"))


def init_face_analyzer():
    """
    Initialize the InsightFace analyzer once so kiosk scans do not pay the
    full model startup cost on the first recognition request.
    """
    app = FaceAnalysis(name=INSIGHTFACE_MODEL_NAME, providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(INSIGHTFACE_DET_SIZE, INSIGHTFACE_DET_SIZE))
    return app


def warmup_face_analyzer(app):
    """
    Run one blank inference to pre-load runtime kernels and reduce first-scan
    latency in kiosk mode.
    """
    if app is None:
        return

    try:
        blank_frame = np.zeros((INSIGHTFACE_DET_SIZE, INSIGHTFACE_DET_SIZE, 3), dtype=np.uint8)
        app.get(blank_frame)
    except Exception:
        # Warmup is best-effort only; real requests should still proceed.
        pass

# Singleton for the analyzer
try:
    face_analyzer = init_face_analyzer()
    warmup_face_analyzer(face_analyzer)
except Exception as e:
    print(f"Warning: InsightFace could not be initialized. Please ensure models are downloaded. Error: {e}")
    face_analyzer = None

def base64_to_image(base64_str: str) -> np.ndarray:
    """Convert base64 string to OpenCV image format."""
    # Remove header if present
    if "base64," in base64_str:
        base64_str = base64_str.split("base64,")[1]
    
    img_data = base64.b64decode(base64_str)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def extract_face_embedding(img: np.ndarray):
    """
    Given an image, extract the primary face embedding.
    Returns the embedding vector as a list of floats (size 512).
    """
    if face_analyzer is None:
        return None
        
    faces = face_analyzer.get(img)
    if not faces:
        return None
        
    # Assume the largest/most centered face is the one to enroll/recognize
    # InsightFace already mostly sorts by confidence or size. 
    # Grab the first face found.
    primary_face = faces[0]
    
    # embedding is a numpy array of 512 dimensions for ArcFace
    embedding = primary_face.normed_embedding
    return embedding.tolist()

def compare_embeddings(emb1: list, emb2: list) -> float:
    """
    Compute Cosine Similarity between two embeddings.
    InsightFace embeddings are normalized, so dot product is cosine similarity.
    """
    vec1 = np.array(emb1)
    vec2 = np.array(emb2)
    similarity = np.dot(vec1, vec2)
    return float(similarity)

def rank_user_matches(query_embedding: list, all_user_embeddings: list):
    """
    Collapse multiple stored embeddings per user into a single best score.
    This helps recognition stay stable when some samples differ slightly,
    such as with glasses or small pose changes.
    """
    grouped_scores = defaultdict(list)

    for user_id, db_emb in all_user_embeddings:
        grouped_scores[user_id].append(compare_embeddings(query_embedding, db_emb))

    ranked = sorted(
        (
            (
                user_id,
                max(scores),
                float(sum(scores) / len(scores)),
            )
            for user_id, scores in grouped_scores.items()
        ),
        key=lambda item: (item[1], item[2]),
        reverse=True,
    )
    return ranked


def find_best_match(
    query_embedding: list,
    all_user_embeddings: list,
    threshold: float = 0.4,
    min_margin: float = 0.03,
):
    """
    Given a list of tuples (user_id, database_embedding), find the best match.
    Uses the best score per user plus a small margin check so we can be a bit
    more tolerant without accepting ambiguous matches.
    """
    ranked_matches = rank_user_matches(query_embedding, all_user_embeddings)
    if not ranked_matches:
        return None, -1.0

    best_match_id, highest_similarity, _ = ranked_matches[0]
    second_best_similarity = ranked_matches[1][1] if len(ranked_matches) > 1 else -1.0

    if highest_similarity < threshold:
        return None, highest_similarity

    if second_best_similarity >= 0 and (highest_similarity - second_best_similarity) < min_margin:
        return None, highest_similarity

    return best_match_id, highest_similarity
