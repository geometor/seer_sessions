"""
Transforms an input numpy grid containing 12 integer digits by first flattening it into a 1D sequence. 
It then counts the number of non-zero elements ('N') in this sequence. 
Finally, it generates a 1D numpy array of length 12, where the first 'N' elements are 1 and the remaining (12 - N) elements are 0.
"""

import numpy as np

# Helper function to count non-zero elements in a flattened array
def count_non_zero_flat(grid):
  """Counts non-zero elements in a flattened version of the input grid."""
  return np.count_nonzero(grid.flatten())

def transform(input_grid):
    """
    Transforms the input grid based on the count of its non-zero elements.

    Args:
        input_grid (np.ndarray): A numpy array (potentially multi-dimensional)
                                 containing 12 integer digits.

    Returns:
        np.ndarray: A 1D numpy array of length 12 containing a sequence of 1s
                    followed by 0s. The number of 1s equals the count of
                    non-zero elements in the input_grid.
    """
    # Define the expected total number of elements and output sequence length
    total_elements = 12

    # Flatten the input grid to a 1D array and count non-zero elements
    non_zero_count = count_non_zero_flat(input_grid)

    # Initialize the output grid as a 1D array of zeros
    output_grid = np.zeros(total_elements, dtype=int)

    # Set the first 'non_zero_count' elements to 1
    # Slicing handles the case where non_zero_count is 0 correctly (selects nothing)
    output_grid[:non_zero_count] = 1

    # The remaining elements are already 0 from initialization

    return output_grid