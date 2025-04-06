import math

"""
Identify the row consisting entirely of the digit 5 (separator line). 
Isolate the portion of the input grid below this separator line.
Count occurrences of digit 2 (count_2) and digit 4 (count_4) within this lower portion.
Calculate the absolute difference: diff = abs(count_2 - count_4).
Determine the fill value for the output grid:
- If diff <= 1, the fill value is 2.
- If diff > 1 and count_4 > count_2, the fill value is 4.
- Otherwise (if diff > 1 and count_2 > count_4), the fill value is 2.
Construct a 2x2 output grid filled entirely with the determined fill value.
"""

def find_separator_row(grid: list[list[int]]) -> int:
    """Finds the index of the row containing only 5s."""
    for r_idx, row in enumerate(grid):
        # Check if all elements in the row are 5
        if all(cell == 5 for cell in row):
            return r_idx
    # Return -1 if no separator row is found (should not happen based on examples)
    return -1 

def count_digit_in_region(grid: list[list[int]], digit: int, start_row: int) -> int:
    """Counts occurrences of a specific digit in the grid rows starting from start_row."""
    count = 0
    # Ensure start_row is within grid bounds
    if start_row >= len(grid): 
        return 0
    # Iterate through rows from start_row to the end
    for r_idx in range(start_row, len(grid)):
        # Iterate through cells in the current row
        for cell in grid[r_idx]:
            if cell == digit:
                count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on comparing counts of 2s and 4s below the separator line,
    considering the absolute difference between counts.
    """
    # Find the separator row (the row of 5s)
    separator_idx = find_separator_row(input_grid)
    
    # If no separator is found, return an empty grid or handle error appropriately
    # Based on examples, a separator always exists.
    if separator_idx == -1:
        return [] 

    # Define the region below the separator
    # Start counting from the row immediately after the separator
    start_row_for_counting = separator_idx + 1

    # Count occurrences of 2 below the separator
    count_2 = count_digit_in_region(input_grid, 2, start_row_for_counting)

    # Count occurrences of 4 below the separator
    count_4 = count_digit_in_region(input_grid, 4, start_row_for_counting)

    # Calculate the absolute difference between counts
    diff = abs(count_2 - count_4)

    # Determine the fill value for the output grid based on the revised logic
    fill_value = 0
    if diff <= 1:
        # If the difference is 0 or 1, the output is 2
        fill_value = 2
    else:
        # If the difference is greater than 1, the output depends on which count is larger
        if count_4 > count_2:
            fill_value = 4
        else: # count_2 > count_4 (since diff > 1, they cannot be equal)
            fill_value = 2

    # Create the 2x2 output grid
    output_grid = [
        [fill_value, fill_value],
        [fill_value, fill_value]
    ]

    return output_grid