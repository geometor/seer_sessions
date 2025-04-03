import copy

"""
Transforms a 1D sequence of colors based on the following rules:
1. Identifies existing horizontal blocks of three identical, non-white pixels in the input sequence. These blocks are preserved in the output.
2. Identifies single non-white pixels in the input sequence that are surrounded by white (0) pixels on both immediate sides (left and right).
3. For each identified single pixel of color 'C' at input index 'i', writes the color 'C' to the output sequence at indices 'i-1', 'i', and 'i+1', effectively expanding the single pixel into a 3-pixel block centered one position to the left of the original single pixel's position.
4. The process involves initializing an output sequence, copying the preserved blocks first, and then applying the expansion transformation for single pixels.
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input sequence.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """
    
    n = len(input_grid)
    # Initialize an output sequence of the same length as the input, filled with white (0).
    output_grid = [0] * n 
    
    # Step 1: Identify and copy existing 3-pixel blocks
    # Iterate through the input sequence using a while loop to handle skipping block indices
    i = 0
    while i <= n - 3:
        # Check if the current position starts a block of three identical non-white pixels
        if input_grid[i] != 0 and input_grid[i] == input_grid[i+1] == input_grid[i+2]:
            # If a block is found, copy it directly to the output grid
            output_grid[i] = input_grid[i]
            output_grid[i+1] = input_grid[i+1]
            output_grid[i+2] = input_grid[i+2]
            # Skip the next two positions as they are part of the copied block
            i += 3 
        else:
            # If no block starts here, move to the next position
            i += 1

    # Step 2: Identify single pixels and expand them in the output
    # Iterate through the input sequence, checking pixels from index 1 up to n-2 
    # This range ensures we can always check left (i-1) and right (i+1) neighbors.
    for i in range(1, n - 1):
        pixel_color = input_grid[i]
        # Check if the current pixel is non-white (not 0) 
        # AND its left neighbor is white (0) 
        # AND its right neighbor is white (0)
        if pixel_color != 0 and input_grid[i-1] == 0 and input_grid[i+1] == 0:
            # Found a single pixel eligible for expansion.
            # Write the pixel's color to the output grid at positions i-1, i, and i+1.
            # This overwrites whatever might have been there (including background 0s).
            # Note: Based on the problem description and examples, expansions do not 
            # overlap with preserved blocks, so this simple assignment is sufficient.
            output_grid[i-1] = pixel_color
            output_grid[i] = pixel_color
            output_grid[i+1] = pixel_color
            
    # Return the completed output sequence
    return output_grid