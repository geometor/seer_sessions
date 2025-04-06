"""
Transforms a 5x5 input grid into a 3x3 output grid based on the most frequent 
non-zero number (1, 2, or 3) present in the input. Each dominant number 
maps to a specific predefined 3x3 pattern composed of 0s and 5s:
- 1 maps to a '+' pattern.
- 2 maps to a 'T' pattern.
- 3 maps to an 'L' pattern (bottom-right).
"""

from collections import Counter
import numpy as np # Using numpy for easier grid handling and counting

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 5x5 list of lists containing integers.

    Returns:
        A 3x3 list of lists representing the output pattern.
    """

    # Define the predefined output patterns corresponding to dominant numbers
    pattern_map = {
        1: [[0, 5, 0], [5, 5, 5], [0, 5, 0]],  # '+' pattern
        2: [[5, 5, 5], [0, 5, 0], [0, 5, 0]],  # 'T' pattern
        3: [[0, 0, 5], [0, 0, 5], [5, 5, 5]],  # 'L' pattern
    }

    # Convert input grid to a numpy array for easier processing
    grid_array = np.array(input_grid)

    # Flatten the grid and count the occurrences of each number
    counts = Counter(grid_array.flatten())

    # Remove the count for 0, as we only care about non-zero numbers
    if 0 in counts:
        del counts[0]
        
    # Check if there are any non-zero numbers left
    if not counts:
        # Handle the case where the input grid only contains 0s or is empty.
        # Based on examples, this seems unlikely, but return a default 
        # or raise an error. Let's return a default grid of 0s.
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]] # Or choose a default pattern


    # Identify the most frequent non-zero number (the dominant number)
    # most_common(1) returns a list of tuples [(number, count)]
    dominant_number, _ = counts.most_common(1)[0]

    # Select the corresponding output pattern based on the dominant number
    output_grid = pattern_map.get(dominant_number)

    # Check if the dominant number was unexpected (not 1, 2, or 3)
    if output_grid is None:
        # Handle unexpected dominant numbers if necessary.
        # For now, assume input guarantees 1, 2, or 3 will be dominant if non-zeros exist.
        # Returning a default grid of 0s as a fallback.
         return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


    return output_grid