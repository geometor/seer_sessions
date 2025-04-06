"""
Transforms a 10x10 input grid containing integers into a 3x3 output grid.
The transformation involves the following steps:
1. Identify all non-zero integer elements in the input grid, noting their value, original row index, and original column index.
2. Sort these non-zero elements based primarily on their column index (ascending) and secondarily on their row index (ascending).
3. Create a list containing only the values of these sorted non-zero elements.
4. If this list contains fewer than 9 elements, append zeros to the end until it has exactly 9 elements. If it has more than 9 (unlikely based on examples), truncate it to the first 9.
5. Initialize an empty 3x3 output grid.
6. Populate the first row of the output grid with the first three elements from the sorted (and padded) value list.
7. Populate the second row of the output grid with the next three elements (indices 3, 4, and 5) from the list, but placed in reverse order (element at index 5 goes to output column 0, index 4 to column 1, index 3 to column 2).
8. Populate the third row of the output grid with the last three elements (indices 6, 7, and 8) from the list.
"""

from typing import List # Use List for type hinting grids

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 10x10 list of lists containing integers.

    Returns:
        A 3x3 list of lists containing the transformed integers.
    """

    # 1. Extract non-zero elements with coordinates (value, row, col)
    # Store as (col, row, value) tuples for easier sorting later
    non_zero_elements = []
    for r, row in enumerate(input_grid):
        for c, value in enumerate(row):
            if value != 0:
                # Store column first to facilitate the primary sort key
                non_zero_elements.append((c, r, value)) 

    # 2. Sort elements primarily by column, then by row
    # Python's default tuple sort achieves this naturally
    non_zero_elements.sort() 

    # 3. Extract just the values into a list
    sorted_values = [value for c, r, value in non_zero_elements]

    # 4. Pad with zeros if fewer than 9 non-zero elements, or truncate if more
    target_length = 9
    current_length = len(sorted_values)
    
    if current_length < target_length:
        # Append the required number of zeros
        sorted_values.extend([0] * (target_length - current_length))
    elif current_length > target_length:
        # Truncate the list to the target length
        sorted_values = sorted_values[:target_length]

    # 5. Initialize the 3x3 output grid with zeros
    output_grid = [[0 for _ in range(3)] for _ in range(3)]

    # 6. Populate the first row (indices 0, 1, 2 from sorted_values)
    # Note: The padding ensures sorted_values always has 9 elements, 
    # so index checks are not strictly necessary but are good practice conceptually.
    output_grid[0][0] = sorted_values[0]
    output_grid[0][1] = sorted_values[1]
    output_grid[0][2] = sorted_values[2]

    # 7. Populate the second row (indices 3, 4, 5 from sorted_values) - reversed order
    output_grid[1][0] = sorted_values[5] # value at index 5 goes to output col 0
    output_grid[1][1] = sorted_values[4] # value at index 4 goes to output col 1
    output_grid[1][2] = sorted_values[3] # value at index 3 goes to output col 2

    # 8. Populate the third row (indices 6, 7, 8 from sorted_values)
    output_grid[2][0] = sorted_values[6]
    output_grid[2][1] = sorted_values[7]
    output_grid[2][2] = sorted_values[8]

    return output_grid