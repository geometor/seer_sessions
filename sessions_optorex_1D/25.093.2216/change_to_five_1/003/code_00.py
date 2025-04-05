"""
Transforms a 1D NumPy array by replacing every non-zero element with 5 and leaving 0 elements unchanged.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1-dimensional NumPy array containing integers.

    Returns:
        A 1-dimensional NumPy array where non-zero elements are replaced by 5.
    """

    # Use numpy.where for efficient element-wise conditional replacement.
    # Check the condition: is the element equal to 0?
    # If the condition (element == 0) is True, keep the element as 0.
    # If the condition (element == 0) is False (meaning the element is non-zero), replace the element with 5.
    output_grid = np.where(input_grid == 0, 0, 5)

    # Return the resulting transformed array
    return output_grid