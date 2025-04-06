"""
Transforms an input grid into an output grid with the same height and 
double the width. For each row in the input grid:
1. If the row consists entirely of zeros, the corresponding output row 
   will also consist entirely of zeros, but with double the width.
2. If the row contains non-zero elements, find the shortest repeating 
   pattern P (of length p) starting from the first element, such that the 
   entire input row is formed by repeating P cyclically.
3. Construct the corresponding output row by repeating this pattern P 
   cyclically until the row reaches double the original width.
"""

import numpy as np

def find_repeating_pattern(row: list[int]) -> tuple[list[int], int]:
    """
    Finds the shortest repeating pattern P (length p) starting at index 0
    that generates the input row r when repeated cyclically.

    Args:
        row: The input list of integers.

    Returns:
        A tuple containing the pattern (list) and its length (int).
        Returns the row itself and its length if no shorter pattern is found.
    """
    n = len(row)
    if n == 0:
        return [], 0
    
    # Iterate through possible pattern lengths p from 1 to n
    for p in range(1, n + 1):
        pattern = row[:p]
        is_repeating = True
        # Check if the entire row is formed by repeating this pattern
        for i in range(n):
            if row[i] != pattern[i % p]:
                is_repeating = False
                break
        # If a repeating pattern is found, return it and its length
        if is_repeating:
            return pattern, p
            
    # Should technically not be reached if p loop goes to n, 
    # but as a fallback, return the row itself.
    return row, n 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the pattern-based horizontal extension transformation.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert input to numpy array for easier operations
    input_array = np.array(input_grid, dtype=int)
    
    # Get input dimensions
    if input_array.size == 0:
         return []
    if input_array.ndim == 1: # Handle potential 1D input if grid is single row
        input_array = input_array.reshape(1, -1)
        
    H, W = input_array.shape
    
    # Calculate output dimensions
    output_H = H
    output_W = 2 * W
    
    # Initialize the output grid as a list
    output_grid = []

    # Process each row
    for i in range(H):
        input_row = input_array[i].tolist() # Work with list representation of the row
        
        # Check if the row is all zeros
        if all(element == 0 for element in input_row):
            # If all zeros, create an output row of zeros with double width
            output_row = [0] * output_W
        else:
            # Find the shortest repeating pattern P and its length p
            P, p = find_repeating_pattern(input_row)
            
            # Construct the output row by repeating the pattern P cyclically
            output_row = [P[k % p] for k in range(output_W)]
            
        # Append the generated output row to the output grid
        output_grid.append(output_row)

    return output_grid