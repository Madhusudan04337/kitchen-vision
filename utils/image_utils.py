import cv2
import numpy as np
from utils.logger import get_logger

logger = get_logger(__name__)


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Resize, enhance brightness/contrast, and sharpen a pantry image.

    Args:
        image: NumPy array in RGB format (H x W x 3), uint8.

    Returns:
        Processed NumPy array in RGB format, uint8.
    """
    logger.info(f"Preprocessing image of shape {image.shape}, dtype {image.dtype}.")

    # Convert RGB to BGR for OpenCV operations
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Resize to 512x512
    bgr = cv2.resize(bgr, (512, 512), interpolation=cv2.INTER_LANCZOS4)

    # Brightness and contrast boost
    bgr = cv2.convertScaleAbs(bgr, alpha=1.2, beta=20)

    # Sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=np.float32)
    bgr = cv2.filter2D(bgr, -1, kernel)

    # CRITICAL: Clip to [0, 255] and cast to uint8.
    # filter2D may return float64 values outside valid image range.
    # Streamlit st.image() requires uint8 or float in [0.0, 1.0].
    # Values outside this range can render as a blank/black image.
    bgr = np.clip(bgr, 0, 255).astype(np.uint8)

    # Convert back to RGB for Streamlit
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    logger.info(f"Preprocessing complete. Output shape: {rgb.shape}, dtype: {rgb.dtype}.")
    return rgb