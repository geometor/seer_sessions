```python
import copy

"""
Iterate through each row of the grid independently. Within each row, identify 
contiguous horizontal blocks of gray (5) pixels. Calculate the length of each 
gray block. If a block's length is 3 or less, change all its pixels to red (2) 
in the output grid. If a block's length is greater than 3, change all its 
pixels to azure (8) in the output grid. All pixels that are not part of a gray 
block are copied directly to the output grid.
"""

def find_and_process_gray_blocks_in_row(input_row):
    """
    Finds contiguous blocks of gray pixels in a single row and returns a new 
    row with blocks replaced according to length rules.

    Args:
        input_row (list): A list of integers representing a single row of pixels.

    Returns:
        list: The transformed row.
    """
    output_row = list(input_row) # Start with a copy of the input row
    n = len(input_row)
    col_index = 0

    while col_index < n:
        # Check if the current pixel is gray (5)
        if input_row[col_index] == 5:
            start_col_index = col_index
            
            # Find the end of the contiguous gray block
            end_col_index = start_col_index + 1
            while end_col_index < n and input_row[end_col_index] == 5:
                end_col_index += 1
            
            # Block found from start_col_index to end_col_index - 1
            length = end_col_index - start_col_index
            
            # Determine the replacement color based on length
            if length <= 3:
                replacement_color = 2 # red
            else: # length > 3
                replacement_color = 8 # azure
                
            # Update the output row for the pixels in this block
            for k in range(start_col_index, end_col_index):
                output_row[k] = replacement_color
                
            # Move the main column iterator past the processed block
            col_index = end_col_index
        else:
            # If not gray, just move to the next pixel
            col_index += 1
            
    return output_row

def transform(input_grid):
    """
    Transforms the input grid by processing each row independently. Finds 
    horizontal blocks of gray (5) pixels and changes their color based on length.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Initialize output_grid as an empty list
    output_grid = []

    # Iterate through each row of the input grid
    for row_index in range(len(input_grid)):
        input_row = input_grid[row_index]
        
        # Process the current row to find and replace gray blocks
        transformed_row = find_and_process_gray_blocks_in_row(input_row)
        
        # Append the transformed row to the output grid
        output_grid.append(transformed_row)

    # Return the completed output grid
    return output_grid
```