"""
Transforms an input sequence (potentially a 2D NumPy array like shape (1, 12)) of 12 integers.
1.  Ensures the input is treated as a flat, one-dimensional sequence.
2.  Finds the first non-zero integer ('significant digit', X) in the sequence.
3.  Creates an output sequence/array of the same shape as the input.
4.  Sets the first 4 elements of the output sequence to 0.
5.  Constructs an 8-digit suffix using the pattern [X, X, X, 0, X, X, 0, X].
6.  Places this suffix into the output sequence starting from index 4.
7.  Returns the transformed output sequence/array, maintaining the original input shape.
"""

import numpy as np

def find_significant_digit_np(input_array: np.ndarray) -> int:
  """
  Finds the first non-zero integer in a NumPy array by checking flattened elements.

  Args:
    input_array: The NumPy array to search within.

  Returns:
    The first non-zero integer found.

  Raises:
    ValueError: If no non-zero digit is found in the array.
  """
  # Flatten the array to iterate through all elements regardless of original shape
  for digit in input_array.flatten():
      # Compare the element to zero
      if int(digit) != 0:
          return int(digit) # Return the first non-zero digit found
  # If no non-zero digit is found after checking all elements, raise error
  raise ValueError("No significant (non-zero) digit found in input array.")

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A NumPy array (potentially 2D, e.g., shape (1, 12)) containing 12 integers.

    Returns:
        A NumPy array with the same shape as input_grid, containing the transformed sequence.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Verify total number of elements if necessary (assuming 12 based on examples)
    if input_grid.size != 12:
        raise ValueError(f"Input array must have size 12, but got {input_grid.size}")

    # Find the significant non-zero digit (X) by looking at the flattened input
    significant_digit = find_significant_digit_np(input_grid)
    X = significant_digit # Alias for clarity

    # Initialize the output grid with zeros, preserving the original shape and data type
    output_grid = np.zeros_like(input_grid) 
    
    # Construct the output suffix pattern using the significant digit (X)
    # The pattern is [X, X, X, 0, X, X, 0, X]
    # Ensure the suffix has the correct data type
    output_suffix = np.array([X, X, X, 0, X, X, 0, X], dtype=input_grid.dtype)
    
    # Assign the constructed suffix to the correct slice of the output grid.
    # Handle potential 2D shape (like (1, 12)) by assigning to the correct slice 
    # within the first (or only) row.
    # If input_grid is 1D (12,), this slice [4:] works directly.
    # If input_grid is 2D (1, 12), this slice [0, 4:] works.
    # Using flatten() and reshape() offers a more general approach if shape varies more.
    # Let's try the flatten/reshape approach for robustness.
    output_flat = output_grid.flatten() # Get a flattened view (or copy depending on contiguity)
    output_flat[4:] = output_suffix     # Assign suffix to the flattened array indices 4-11
    
    # Reshape the modified flattened array back to the original shape
    # Note: If output_flat was a view, output_grid might already be modified. 
    # If it was a copy, we need to reshape and return the new array.
    # np.zeros_like creates a new array, so flatten likely returns a copy.
    # Reshaping the modified flat array ensures we return the correct structure.
    output_grid_transformed = output_flat.reshape(input_grid.shape)
  
    # Return the final transformed grid
    return output_grid_transformed
