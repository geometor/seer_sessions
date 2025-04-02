"""
The transformation rule selects a specific color from an input grid based on frequency and position within the flattened grid.
1. Flatten the input 2D grid into a 1D list (preserving row-major order).
2. Count the frequency of each distinct color in the flattened list.
3. Identify the set of colors that appear exactly once in the flattened list. Let this set be S.
4. Determine the output based on the size of S:
    - Case A (Size of S == 1): The single color in S is the output.
    - Case B (Size of S > 1): 
        - Find the first index (position) of each color from S in the flattened list.
        - Collect these indices into a list.
        - Sort the list of indices in ascending order.
        - Identify the median index from this sorted list. For an even number n of indices, use the index at position floor((n-1)/2) in the sorted list (the lower median index). Let this be the `target_index_value`.
        - The color located at the `target_index_value` in the original flattened list is the output.
    - Case C (Size of S == 0): (Not observed) Raise an error as the rule is undefined.
"""

import numpy as np
from collections import Counter
import math

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D NumPy array representing the input grid.

    Returns:
        An integer representing the output color.
    """

    # Step 1: Flatten the input 2D grid into a 1D list
    # Convert to list for easier index finding later
    flat_list = input_grid.flatten().tolist()

    # Step 2: Count the frequency of each distinct color
    color_counts = Counter(flat_list)

    # Step 3: Identify colors that appear exactly once
    unique_colors = [color for color, count in color_counts.items() if count == 1]

    # Step 4: Determine the output based on the number of unique colors
    num_unique = len(unique_colors)

    if num_unique == 1:
        # Case A: Only one color appears exactly once
        output_color = unique_colors[0]
    elif num_unique > 1:
        # Case B: Multiple colors appear exactly once
        
        # Find the first index (position) of each unique color in the flattened list
        first_indices = []
        for color in unique_colors:
            try:
                # list.index() finds the first occurrence
                index = flat_list.index(color)
                first_indices.append(index)
            except ValueError:
                 # This case should technically not be reachable if color is from unique_colors derived from flat_list
                 # Include for robustness or potential edge cases not covered in examples
                 print(f"Warning: Color {color} from unique_colors not found in flat_list. Skipping.")
                 continue

        # Sort the list of indices in ascending order
        first_indices.sort()

        # Identify the median index value from the sorted list of indices
        # Using floor((n-1)/2) for the position in the sorted list
        n = len(first_indices)
        if n == 0: # Check if finding indices failed for all unique colors (highly unlikely)
             raise ValueError("Could not find indices for any unique colors.")
             
        median_index_position = math.floor((n - 1) / 2)
        target_index_value = first_indices[median_index_position]

        # The output is the color located at the target_index_value in the original flattened list
        output_color = flat_list[target_index_value]
    else:
        # Case C: No color appears exactly once (Size of S == 0)
        # This case was not observed in the training examples.
        raise ValueError("No color appears exactly once in the input grid.")

    # The function needs to return a single integer value, not a grid
    return output_color