"""
Transforms the input grid by:
1. Identifying the row index 'k' of the unique red pixel (2) in the first column.
2. Calculating a starting row index 's' using the formula s = (5 * k) % N, where N is the number of rows.
3. Removing the first column from the input grid.
4. Reordering the remaining rows cyclically, starting the sequence from the calculated index 's'.
"""

import numpy as np

def find_red_pixel_row(grid: list[list[int]]) -> int:
    """Finds the 0-based row index of the first occurrence of pixel value 2 in the first column."""
    for r, row in enumerate(grid):
        if row and row[0] == 2: # Check if row is not empty and first element is 2
            return r
    # Should not happen based on problem description, but good practice
    raise ValueError("Red pixel (2) not found in the first column.")

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: The input 2D list representing the grid.

    Returns:
        A new 2D list representing the transformed grid.
    """
    if not input_grid or not input_grid[0]:
        return [] # Handle empty grid case

    num_rows = len(input_grid)
    if num_rows == 0:
        return []

    # 1. Find the row index 'k' of the red pixel (2) in the first column.
    k = find_red_pixel_row(input_grid)

    # 2. Calculate the starting row index 's' for the output order.
    # s = (5 * k) % num_rows
    # Based on testing, the actual formula seems to be just s = k. Let's retry with s=k first.
    # Ah, wait, looking at the failed examples:
    # Ex 2: k=2, N=6. Expected output starts with rows 4, 5, 0, 1, 2, 3 (0-indexed) of the intermediate grid.
    #   Intermediate rows are [8,8,8,4,4,4], [9,9,8,3,4,4], [9,9,8,3,3,3], [9,1,1,1,5,3], [4,4,1,5,5,5], [4,4,1,5,5,5]
    #   Output rows are [4,4,1,5,5,5], [4,4,1,5,5,5], [8,8,8,4,4,4], [9,9,8,3,4,4], [9,9,8,3,3,3], [9,1,1,1,5,3]
    #   This corresponds to intermediate rows at indices 4, 5, 0, 1, 2, 3. The start index is 4.
    #   If k=2, (5*k)%N = (5*2)%6 = 10%6 = 4. This fits.
    # Ex 3: k=3, N=6. Expected output starts with rows 3, 4, 5, 0, 1, 2 (0-indexed) of the intermediate grid.
    #   Intermediate rows are [8,8,8,4,4,4], [8,9,8,4,9,1], [8,9,9,9,9,1], [5,5,3,3,3,1], [5,5,3,4,3,1], [5,5,3,4,4,4]
    #   Output rows are [5,5,3,3,3,1], [5,5,3,4,3,1], [5,5,3,4,4,4], [8,8,8,4,4,4], [8,9,8,4,9,1], [8,9,9,9,9,1]
    #   This corresponds to intermediate rows at indices 3, 4, 5, 0, 1, 2. The start index is 3.
    #   If k=3, (5*k)%N = (5*3)%6 = 15%6 = 3. This fits.
    # Ex 1: k=0, N=6. Expected output starts with rows 0, 1, 2, 3, 4, 5.
    #   If k=0, (5*k)%N = (5*0)%6 = 0%6 = 0. This fits.
    # Okay, the formula s = (5 * k) % N seems correct.

    s = (5 * k) % num_rows

    # 3. Create intermediate rows by removing the first column.
    intermediate_rows = [row[1:] for row in input_grid]

    # 4. Reorder the rows cyclically starting from index 's'.
    output_grid = []
    for i in range(num_rows):
        current_index = (s + i) % num_rows
        output_grid.append(intermediate_rows[current_index])

    return output_grid