"""
Transforms an input grid containing exactly two non-zero markers.
It draws horizontal and vertical lines corresponding to each marker's position and value onto an output grid.
The line drawing process involves overwriting.
Specific intersection points where a horizontal line from one marker crosses a vertical line from the other are marked with the value 2.
The original marker positions retain their original values.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_markers(grid: List[List[int]]) -> List[Tuple[int, int, int]]:
    """
    Finds the non-zero markers in the grid.

    Args:
        grid: The input grid.

    Returns:
        A list containing tuples of (value, row, col) for each non-zero marker found.
        Expects exactly two markers.
    """
    markers = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                markers.append((value, r, c))
    if len(markers) != 2:
        # This case might need more robust handling depending on assumptions
        # For now, we assume exactly two markers based on the examples.
        print(f"Warning: Expected 2 markers, found {len(markers)}")
    return markers

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # initialize output_grid with zeros
    output_np = np.zeros_like(input_np)

    # 1. Identify Markers
    markers = find_markers(input_grid)
    if len(markers) != 2:
        # Handle cases where the assumption of 2 markers isn't met
        # Returning the empty grid or raising an error might be options
        print("Error: Did not find exactly two markers.")
        return output_np.tolist() # Return zero grid for now

    (v1, r1, c1) = markers[0]
    (v2, r2, c2) = markers[1]

    # 3. Draw First Cross (Value v1, Row r1, Col c1)
    # Fill row r1 with v1
    output_np[r1, :] = v1
    # Fill column c1 with v1
    output_np[:, c1] = v1

    # 4. Draw Second Cross (Value v2, Row r2, Col c2)
    # Fill row r2 with v2 (overwrites previous values where applicable)
    output_np[r2, :] = v2
    # Fill column c2 with v2 (overwrites previous values where applicable)
    output_np[:, c2] = v2

    # 5. Mark Intersections with value 2
    # Set the intersection of marker 1's row and marker 2's column
    output_np[r1, c2] = 2
    # Set the intersection of marker 2's row and marker 1's column
    output_np[r2, c1] = 2

    # 6. Restore Originals
    # Ensure the original position of marker 1 has its value v1
    output_np[r1, c1] = v1
    # Ensure the original position of marker 2 has its value v2
    output_np[r2, c2] = v2

    # Convert back to list of lists for the return type
    output_grid = output_np.tolist()

    return output_grid