import numpy as np

def apply_gravity_to_segment(segment: np.ndarray) -> np.ndarray:
    """Applies gravity column by column within a segment."""
    if segment is None or segment.size == 0:
        return segment
    rows, cols = segment.shape
    new_segment = np.zeros_like(segment)
    for c in range(cols):
        col_data = segment[:, c]
        non_zeros = col_data[col_data != 0]
        if len(non_zeros) > 0:
            new_segment[rows - len(non_zeros):rows, c] = non_zeros
    return new_segment