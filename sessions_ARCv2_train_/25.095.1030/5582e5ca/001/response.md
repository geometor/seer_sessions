```python
"""
Transforms a 3x3 input grid of digits into a 3x3 output grid where every cell is filled with the digit that appeared most frequently in the input grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Takes a 3x3 grid of digits, finds the most frequent digit, and returns a 
    new 3x3 grid filled entirely with that digit.

    Args:
        input_grid (list of lists or np.ndarray): The input 3x3 grid of digits.

    Returns:
        np.ndarray: A 3x3 grid filled with the most frequent digit from the input.
    """
    # Convert input to a numpy array for easier handling
    grid_np = np.array(input_grid)
    
    # Flatten the grid into a 1D list of digits
    flat_list = grid_np.flatten().tolist()
    
    # Count the frequency of each digit
    digit_counts = Counter(flat_list)
    
    # Find the digit with the highest frequency
    # most_common(1) returns a list of tuples [(element, count)], so we take the first element [0] and its item [0]
    most_frequent_digit = digit_counts.most_common(1)[0][0]
    
    # Get the dimensions of the input grid
    rows, cols = grid_np.shape
    
    # Initialize the output grid with the same dimensions
    # Fill the output grid with the most frequent digit
    output_grid = np.full((rows, cols), most_frequent_digit, dtype=int)

    return output_grid.tolist() # Return as list of lists if that's preferred, or keep as numpy array

```