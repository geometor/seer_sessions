import numpy as np

"""
Transforms a NumPy array of digits element-wise: if the input digit is 0, the output digit is 0; otherwise (if the input digit is 1-9), the output digit is 5.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms a NumPy array of digits according to the rule:
    0 maps to 0, non-zero maps to 5.

    Args:
        input_grid: A NumPy array containing single digits (0-9).

    Returns:
        A NumPy array containing the transformed digits (0 or 5).
    """
    # Create an output grid of the same shape and data type as the input, initialized with zeros.
    # This handles the case where input elements are 0, as they will remain 0.
    output_grid = np.zeros_like(input_grid)

    # Identify the indices where the input grid elements are not equal to 0.
    non_zero_mask = (input_grid != 0)

    # For all elements where the input was non-zero, set the corresponding element in the output grid to 5.
    output_grid[non_zero_mask] = 5

    # Return the transformed grid.
    return output_grid
