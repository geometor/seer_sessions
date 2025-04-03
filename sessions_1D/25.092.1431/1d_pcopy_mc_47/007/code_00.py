import numpy as np

"""
Transforms a 1xN input grid based on pixel patterns.

The transformation iterates through the input row pixel by pixel:
1. Checks if the current non-background pixel is the start of a 3-pixel block of the same color.
   - If yes: The 3-pixel block is appended to the output, and the input index advances by 3.
2. If it's not a 3-pixel block, checks if the current non-background pixel is preceded by a background pixel (0).
   - If yes: The preceding background pixel (which would have just been added to the output) is removed, and a 3-pixel block of the current pixel's color is appended. The input index advances by 1.
3. If the current pixel is background (0), or if it's a non-background pixel that doesn't meet conditions 1 or 2 (e.g., at the start, or preceded by another color), the pixel is simply appended to the output, and the input index advances by 1.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): A 1xN grid.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    # Input handling and extraction of the single row
    if isinstance(input_grid, np.ndarray):
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
            input_row = input_grid.tolist()[0]
        else:
            return [[]] # Handle unexpected numpy array shape
    elif isinstance(input_grid, list) and input_grid and isinstance(input_grid[0], list):
        input_row = input_grid[0]
    else:
        return [[]] # Return empty grid for invalid input format

    width = len(input_row)
    if width == 0:
        return [[]] # Handle empty row case

    # Initialize output row list
    output_row = []
    # Initialize index for iterating through the input row
    i = 0

    # Iterate through the input row
    while i < width:
        current_color = input_row[i]

        # Check for non-background color
        if current_color != 0:
            # Condition 1: Check for existing 3-pixel block
            is_three_block = False
            if i + 2 < width: # Check bounds first
                if input_row[i+1] == current_color and input_row[i+2] == current_color:
                    is_three_block = True
            
            if is_three_block:
                # Append the block and advance index by 3
                output_row.extend([current_color, current_color, current_color])
                i += 3
                continue # Continue to next iteration

            # Condition 2: Check for single pixel preceded by background (0) for shift-left expansion
            # Ensure output_row is not empty and the last element added corresponds to input_row[i-1] which was 0
            # Note: This check implies i > 0, which is implicitly handled by checking output_row
            elif output_row and input_row[i-1] == 0: # Check input[i-1] directly
                 # Check if the last element added to output was indeed that 0.
                 # This requires careful tracking or assumptions. A safer check is i > 0 and input_row[i-1]==0
                 if i > 0 and input_row[i-1] == 0: 
                    # Check if the last element in output_row is 0 before popping
                    if output_row and output_row[-1] == 0:
                         output_row.pop() # Remove the preceding 0 from output
                    
                    # Append the expanded block
                    output_row.extend([current_color, current_color, current_color])
                    i += 1 # Advance index by 1 (only consumed the single pixel)
                    continue # Continue to next iteration

        # Condition 3 / Default: Append the current pixel and advance by 1
        # This handles:
        # - Background pixels (0)
        # - Non-background pixels at index 0
        # - Non-background pixels not part of a 3-block and not preceded by 0
        output_row.append(current_color)
        i += 1

    # Return the output row wrapped in a list
    return [output_row]