import math
import numpy as np
import collections

"""
Transforms an input sequence (list of integers) based on the following rule:
1. Identify all unique non-zero integer values present in the input sequence.
2. For each unique non-zero value:
   a. Find the index of its first occurrence and the index of its last occurrence in the input sequence.
   b. In the output sequence (initially a copy of the input), set all elements from the first index to the last index (inclusive) to this non-zero value.
3. Return the modified sequence.
"""

def find_indices_of_value(sequence, value):
    """Helper function to find all indices of a specific value in a sequence."""
    return [i for i, x in enumerate(sequence) if x == value]

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (sequence).

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = list(input_grid)
    
    # Find unique non-zero values in the input sequence
    # Using a set automatically handles uniqueness and order doesn't matter here
    non_zero_values = set(x for x in input_grid if x != 0)
    
    # Process each unique non-zero value
    for value in non_zero_values:
        # Find all indices where the current non-zero value appears
        indices = find_indices_of_value(input_grid, value)
        
        # If the value exists in the input (should always be true based on how non_zero_values is generated)
        if indices:
            # Determine the first (min) and last (max) occurrence index
            min_index = min(indices)
            max_index = max(indices)
            
            # Fill the range in the output_grid with the current non-zero value
            for i in range(min_index, max_index + 1):
                output_grid[i] = value
                
    # Return the modified output grid
    return output_grid
