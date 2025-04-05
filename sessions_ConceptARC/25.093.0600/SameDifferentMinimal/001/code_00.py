import numpy as np
from typing import List, Set, Tuple

"""
Transforms an input grid based on the number of unique non-zero colors present.

1. Identify all unique non-zero color values in the input grid.
2. Count the number of these unique colors.
3. Determine the single output color based on the count:
   - If the count is 1, the output color is 4.
   - If the count is 2, the output color is 5.
4. Create an output grid of the same dimensions as the input.
5. For each cell:
   - If the input cell value is 0, the output cell value is 0.
   - If the input cell value is non-zero, the output cell value is the determined output color.
"""

def find_unique_non_zero_colors(grid: np.ndarray) -> Set[int]:
    """Finds all unique non-zero values in a grid."""
    unique_values = set(np.unique(grid))
    # Remove 0 if it exists
    unique_values.discard(0)
    return unique_values

def determine_output_color(unique_color_count: int) -> int:
    """Determines the output color based on the count of unique input colors."""
    if unique_color_count == 1:
        return 4
    elif unique_color_count == 2:
        return 5
    else:
        # Define a default or error case if needed, though based on examples,
        # counts are only 1 or 2. Let's default to 0 or raise an error.
        # For now, sticking to observed patterns.
        # Returning -1 to indicate an unexpected count based on training data.
        # A more robust solution might raise ValueError.
        print(f"Warning: Unexpected number of unique colors: {unique_color_count}")
        return -1 # Or handle as appropriate for the broader context

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the color transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # 1. Identify unique non-zero colors
    unique_colors = find_unique_non_zero_colors(input_array)

    # 2. Count the unique colors
    unique_color_count = len(unique_colors)

    # 3. Determine the target output color
    output_color = determine_output_color(unique_color_count)
    
    # Handle the case where the count wasn't 1 or 2
    if output_color == -1:
        # Decide how to handle this - return input? return error grid?
        # For now, returning a copy of the input might be safest.
        print("Returning input grid due to unexpected unique color count.")
        return input_grid

    # 4. Create the output grid (start with a copy, then modify)
    # Using np.copy ensures we don't modify the original input array if it's passed elsewhere
    output_array = np.copy(input_array)

    # 5. Iterate and transform: Replace non-zero values with the output color
    # Use boolean indexing for efficiency: find where the input array is not zero
    non_zero_mask = input_array != 0
    output_array[non_zero_mask] = output_color

    # Convert the numpy array back to a list of lists for the expected output format
    output_grid = output_array.tolist()

    return output_grid
