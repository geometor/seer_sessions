"""
Transforms an input grid of integers into an output grid of the same dimensions.
The output grid is uniformly filled with the single integer that appears most
frequently (the mode) in the input grid.
"""

from collections import Counter
import itertools

def _count_frequencies(grid: list[list[int]]) -> Counter:
    """Counts the frequency of each number in the grid."""
    # Flatten the grid into a single list of numbers
    flat_list = list(itertools.chain.from_iterable(grid))
    # Count the occurrences of each number
    return Counter(flat_list)

def _find_mode(counts: Counter) -> int:
    """Finds the number with the highest frequency (mode)."""
    # Find the number(s) with the maximum count
    # most_common(1) returns a list of tuples [(element, count)]
    # We just need the element (the number)
    if not counts:
        # Handle empty input grid case if necessary, though examples suggest 3x3
        return 0 # Or raise an error, or return a default
    mode_tuple = counts.most_common(1)[0]
    return mode_tuple[0]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: find the most frequent number in the
    input grid and create an output grid of the same size filled with that number.
    """
    # Validate input grid dimensions (optional but good practice)
    if not input_grid or not all(isinstance(row, list) for row in input_grid):
        raise ValueError("Input must be a non-empty list of lists.")
    
    num_rows = len(input_grid)
    if num_rows == 0:
         return [] # Handle empty grid case
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return [[] for _ in range(num_rows)] # Handle grid with empty rows


    # Count the occurrences of each number in the input grid
    frequency_counts = _count_frequencies(input_grid)

    # Identify the number that has the highest frequency (the mode)
    fill_value = _find_mode(frequency_counts)

    # Create a new output grid with the same dimensions as the input grid
    # Fill every cell of the new output grid with the most frequent number
    output_grid = [[fill_value for _ in range(num_cols)] for _ in range(num_rows)]

    # Return the filled output grid
    return output_grid
