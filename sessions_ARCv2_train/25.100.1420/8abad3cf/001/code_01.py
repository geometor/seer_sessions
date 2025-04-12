"""
Transforms the input grid by finding the most frequent element, identifying the 
bounding box of all other elements, extracting this subgrid, and rotating it 
90 degrees counter-clockwise.
"""

import numpy as np
from collections import Counter

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Finds the subgrid containing non-most-frequent elements, extracts it, 
    rotates it 90 degrees counter-clockwise, and returns the result.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)

    # Find the most frequent element
    # Flatten the grid, count element occurrences, and find the most common one
    counts = Counter(grid.flatten())
    # Handle cases where the grid might be empty or have multiple most frequent elements (takes the first one)
    if not counts:
        return [] # Return empty list for empty input
    most_frequent_element = counts.most_common(1)[0][0]

    # Find the indices of elements *not* equal to the most frequent element
    non_frequent_indices = np.argwhere(grid != most_frequent_element)

    # If all elements are the same, there's nothing to extract/rotate
    if non_frequent_indices.size == 0:
         # Determine behavior for grids with only one type of element.
         # Based on examples, seems like it should return an empty grid or handle based on specific rules not fully clear yet.
         # Let's return an empty grid for now.
         return []


    # Determine the bounding box of these elements
    min_row = np.min(non_frequent_indices[:, 0])
    max_row = np.max(non_frequent_indices[:, 0])
    min_col = np.min(non_frequent_indices[:, 1])
    max_col = np.max(non_frequent_indices[:, 1])

    # Extract the subgrid defined by the bounding box
    # Note: slicing includes the start index but excludes the end index, so add 1 to max values
    subgrid = grid[min_row : max_row + 1, min_col : max_col + 1]

    # Rotate the extracted subgrid 90 degrees counter-clockwise
    # k=1 specifies one counter-clockwise rotation
    rotated_subgrid = np.rot90(subgrid, k=1)

    # Convert the resulting numpy array back to a list of lists
    output_grid = rotated_subgrid.tolist()

    return output_grid