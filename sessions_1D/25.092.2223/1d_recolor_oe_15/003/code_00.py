import numpy as np

"""
Transforms the input grid by processing horizontal segments of green (3) pixels.
Iterates through each row, identifies contiguous horizontal segments of green pixels.
If a segment has an even length, its pixels are changed to blue (1) in the output.
If a segment has an odd length, its pixels are changed to gray (5) in the output.
White (0) pixels remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule based on horizontal green segment length parity.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    rows, cols = input_np.shape
    
    # Define target and output colors
    target_color = 3 # green
    even_len_color = 1 # blue
    odd_len_color = 5 # gray

    # Iterate through each row
    for r in range(rows):
        c = 0
        while c < cols:
            # Check if the current pixel is the start of a green segment
            if input_np[r, c] == target_color:
                start_c = c
                # Find the end of the contiguous green segment in this row
                while c < cols and input_np[r, c] == target_color:
                    c += 1
                end_c = c
                
                # Calculate the length of the segment
                segment_length = end_c - start_c
                
                # Determine the output color based on the parity of the length
                if segment_length % 2 == 0: # Even length
                    output_color = even_len_color
                else: # Odd length
                    output_color = odd_len_color
                    
                # Update the corresponding pixels in the output grid for this segment
                output_grid[r, start_c:end_c] = output_color
            else:
                # Move to the next column if not a target color pixel
                c += 1
                
    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()
