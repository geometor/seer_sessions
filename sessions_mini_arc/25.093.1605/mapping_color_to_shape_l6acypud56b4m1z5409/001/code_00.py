"""
Transforms an input grid based on the dominant non-zero digit present.

1.  Analyzes the input grid to find the non-zero digit (1, 2, or 3) that appears most frequently.
2.  Creates an output grid of the same dimensions, initially filled with zeros.
3.  If the dominant digit is 1, places the digit 5 along the main diagonal of the output grid.
4.  If the dominant digit is 2, places the digit 5 along the anti-diagonal of the output grid.
5.  If the dominant digit is 3, places the digit 5 along the top row of the output grid.
6.  Returns the resulting output grid.
"""

import numpy as np
from collections import Counter

def find_dominant_nonzero(grid):
    """
    Finds the non-zero digit (1, 2, or 3) that occurs most frequently in the grid.
    Returns None if no non-zero digits are found or if there's a tie between relevant digits.
    """
    # Flatten the grid and filter out zeros
    non_zeros = [cell for row in grid for cell in row if cell != 0]
    
    if not non_zeros:
        return None # No non-zero digits found

    # Count occurrences of each non-zero digit
    counts = Counter(non_zeros)
    
    # Find the most common digit among 1, 2, 3 specifically, if they exist
    relevant_counts = {digit: counts.get(digit, 0) for digit in [1, 2, 3]}
    
    # Find the digit with the maximum count
    max_count = 0
    dominant_digit = None
    tie = False
    
    for digit, count in relevant_counts.items():
        if count > max_count:
            max_count = count
            dominant_digit = digit
            tie = False
        elif count == max_count and max_count > 0:
            # This handles potential ties, though not observed in examples
            # For this problem's constraints, we can assume a unique dominant digit
            # If a tie *could* occur, the desired behavior would need clarification
            pass 

    # Return the dominant digit if found and count > 0
    return dominant_digit if max_count > 0 else None


def transform(input_grid):
    """
    Applies the transformation rule based on the dominant non-zero digit.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid with zeros, same shape as input
    output_grid = np.zeros_like(input_np)

    # Find the dominant non-zero digit in the input grid
    dominant_number = find_dominant_nonzero(input_grid)

    # Apply the pattern based on the dominant number
    if dominant_number == 1:
        # Place 5s along the main diagonal (i == j)
        # Ensure we don't go out of bounds for non-square grids (though examples are square)
        for i in range(min(height, width)):
            output_grid[i, i] = 5
            
    elif dominant_number == 2:
        # Place 5s along the anti-diagonal (i + j == height - 1)
        # Ensure we don't go out of bounds
        for i in range(height):
            j = (width - 1) - i # Calculate corresponding column index for anti-diagonal
            if 0 <= j < width: # Check if the column index is valid
                 output_grid[i, j] = 5
                 
    elif dominant_number == 3:
        # Place 5s along the top row (row index 0)
        if height > 0: # Check if grid has rows
            for j in range(width):
                output_grid[0, j] = 5

    # Convert back to list of lists if necessary for the environment
    return output_grid.tolist()
