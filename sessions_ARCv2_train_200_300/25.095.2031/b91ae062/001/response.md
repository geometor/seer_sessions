```python
"""
The transformation rule scales an input grid based on the count of unique non-zero digits present in it.
Each cell in the input grid is expanded into a square block of identical digits in the output grid.
The size of this square block (the scaling factor 'S') is determined by the number of unique non-zero digits found in the entire input grid.
The dimensions of the output grid are S times the dimensions of the input grid.
Specifically:
1. Identify all unique non-zero digits in the input grid.
2. Count these unique non-zero digits to get the scaling factor 'S'.
3. Create an output grid with dimensions (input_rows * S) x (input_cols * S).
4. For each cell (r, c) containing digit 'd' in the input grid, fill the corresponding S x S block starting at output grid coordinates (r * S, c * S) with the digit 'd'.
"""

import math  # Not strictly necessary for this solution, but good practice to include common math lib

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the block scaling transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid of digits.

    Returns:
        A list of lists representing the scaled output grid.
    """

    # --- Determine Scaling Factor ---
    unique_digits = set()
    # Flatten the grid and find unique non-zero digits
    for row in input_grid:
        for digit in row:
            if digit != 0:
                unique_digits.add(digit)

    scale_factor = len(unique_digits)

    # Handle edge case where input might be all zeros (though not in examples)
    # If the input grid has dimensions but contains only zeros, 
    # the scale_factor would be 0 based on the rule. 
    # An output grid of size 0x0 is problematic.
    # Let's default to a scale_factor of 1 if the calculated factor is 0 but the grid is not empty.
    # However, observing train_3 and train_5, zero rows/cols in input become zero blocks in output,
    # scaled by the factor derived from non-zero elements. So a factor of 0 isn't reached in examples.
    # If scale_factor is naturally 0, perhaps return an empty grid or the original?
    # Sticking to the observed behavior: scale_factor is derived from non-zeros.
    # If there are non-zero digits, scale_factor will be >= 1.
    
    # If grid is empty or scale_factor becomes 0 unexpectedly, return empty or handle appropriately.
    if not input_grid or not input_grid[0]:
         return [] # Return empty for empty input
    if scale_factor == 0:
         # If all input digits were 0, scale_factor is 0.
         # Let's decide what to do. Maybe return a grid of same size but all 0s?
         # Or maybe scale by 1? Let's replicate the input in this case.
         # Example 3 has a row of 0s, output has a scaled block of 0s.
         # This implies 0s are scaled just like other numbers, using the global scale factor.
         # A truly all-zero grid would lead to scale=0. What should output be?
         # Let's assume scale_factor must be at least 1 for a non-empty grid.
         # But based on the rule "Count the number of unique non-zero digits", it *should* be 0.
         # Let's follow the rule precisely and see. Output dimensions would be 0x0.
         # This seems unlikely to be the desired behavior for ARC tasks.
         # Let's assume scale_factor should be 1 if no non-zero digits are found (all zeros input).
         scale_factor = 1 # Default to 1 if input grid is all zeros but not empty.


    # --- Get Input Dimensions ---
    input_rows = len(input_grid)
    input_cols = len(input_grid[0]) # Assume non-empty, rectangular grid

    # --- Calculate Output Dimensions ---
    output_rows = input_rows * scale_factor
    output_cols = input_cols * scale_factor

    # --- Initialize Output Grid ---
    # Create a grid filled with a placeholder (e.g., 0) initially.
    output_grid = [[0 for _ in range(output_cols)] for _ in range(output_rows)]

    # --- Populate Output Grid ---
    # Iterate through each cell of the input grid
    for r in range(input_rows):
        for c in range(input_cols):
            # Get the digit from the input cell
            digit_to_replicate = input_grid[r][c]

            # Determine the top-left corner of the block in the output grid
            start_row = r * scale_factor
            start_col = c * scale_factor

            # Fill the corresponding scale_factor x scale_factor block in the output grid
            for out_r in range(start_row, start_row + scale_factor):
                for out_c in range(start_col, start_col + scale_factor):
                    # Ensure we don't go out of bounds (shouldn't happen with correct logic)
                    if 0 <= out_r < output_rows and 0 <= out_c < output_cols:
                        output_grid[out_r][out_c] = digit_to_replicate

    return output_grid

```