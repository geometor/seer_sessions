"""
Processes an input NumPy array of digits. For each element in the input array:
- If the element is 0, the corresponding output element is 0.
- If the element is non-zero (1-9), the corresponding output element is 5.
The output array maintains the same shape as the input.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule (0->0, non-zero->5) element-wise to a NumPy array.

    Args:
        input_grid: A NumPy array containing integer digits (0-9).

    Returns:
        A NumPy array of the same shape where non-zero elements are replaced by 5.
    """

    # Apply the conditional mapping using np.where
    # Condition: input_grid == 0
    # Value if true: 0
    # Value if false: 5
    output_grid = np.where(input_grid == 0, 0, 5)

    # Return the transformed NumPy array
    return output_grid
