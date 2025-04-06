"""
1. Examine the 10x10 input grid to find the row `r5` and column `c5` where the digit '5' is located.
2. Determine the `target_digit` by identifying which non-zero digit (other than '5') occurs most frequently in the input grid.
3. Calculate the starting row and column for extraction: `start_row = r5 + 1`, `start_col = c5 - 1`.
4. Extract the 3x3 subgrid from the input grid, covering rows `start_row` to `start_row + 2` and columns `start_col` to `start_col + 2`.
5. Initialize an empty 3x3 output grid filled with '0's.
6. Iterate through each cell of the extracted 3x3 subgrid region in the input. If a cell's value is equal to the `target_digit`, place the `target_digit` in the corresponding position in the output grid. Otherwise, leave the '0'.
7. Return the final 3x3 output grid.
"""

from collections import Counter

def _find_digit_location(grid: list[list[int]], digit: int) -> tuple[int, int] | None:
    """Finds the row and column of the first occurrence of a digit."""
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == digit:
                return r, c
    return None # Should not happen based on problem description

def _find_target_digit(grid: list[list[int]], exclude_digit: int) -> int:
    """Finds the most frequent non-zero digit, excluding a specific digit."""
    counts = Counter()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
             val = grid[r][c]
             # Count non-zero digits that are not the excluded marker digit
             if val != 0 and val != exclude_digit:
                 counts[val] += 1
    
    # Find the digit with the highest count
    if not counts:
        # Handle case where only 0 and the exclude_digit are present (unlikely based on examples)
        # Or if the grid is empty or only contains 0s/exclude_digit
        return 0 # Default to 0 if no target digit candidates found
    
    # Return the digit that appeared most often
    target_digit = counts.most_common(1)[0][0] 
    return target_digit

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid by extracting a 3x3 subgrid relative to the 
    position of the digit '5' and filtering it to keep only the most 
    frequent non-zero digit (excluding '5').
    """
    
    # Constants
    MARKER_DIGIT = 5
    OUTPUT_SIZE = 3
    BACKGROUND_DIGIT = 0

    # 1. Find the location of the marker digit '5'
    marker_loc = _find_digit_location(input_grid, MARKER_DIGIT)
    if marker_loc is None:
        # Handle error case: marker not found (return empty or default grid?)
        # Based on examples, '5' is always present. Assuming valid input.
        # For robustness, returning an empty grid might be an option.
         return [[BACKGROUND_DIGIT for _ in range(OUTPUT_SIZE)] for _ in range(OUTPUT_SIZE)] 
    r5, c5 = marker_loc

    # 2. Determine the target digit (most frequent non-zero, non-5 digit)
    target_digit = _find_target_digit(input_grid, MARKER_DIGIT)

    # 3. Calculate the top-left corner for the 3x3 extraction region
    # Extraction starts one row below and one column left of the marker
    start_row = r5 + 1
    start_col = c5 - 1

    # 4. Initialize the output grid with the background digit
    output_grid = [[BACKGROUND_DIGIT for _ in range(OUTPUT_SIZE)] for _ in range(OUTPUT_SIZE)]
    
    input_rows = len(input_grid)
    input_cols = len(input_grid[0]) if input_rows > 0 else 0

    # 5. Extract and filter the 3x3 region
    for r_out in range(OUTPUT_SIZE):  # Iterate through output grid rows (0, 1, 2)
        for c_out in range(OUTPUT_SIZE): # Iterate through output grid columns (0, 1, 2)
            
            # Calculate corresponding coordinates in the input grid
            r_in = start_row + r_out
            c_in = start_col + c_out

            # Check if the calculated input coordinates are within the bounds of the input grid
            if 0 <= r_in < input_rows and 0 <= c_in < input_cols:
                # If the value at the input coordinate matches the target digit,
                # place it in the corresponding output grid cell.
                if input_grid[r_in][c_in] == target_digit:
                    output_grid[r_out][c_out] = target_digit
            # Otherwise, the output cell remains the background digit (initialized value)

    # 6. Return the transformed 3x3 grid
    return output_grid