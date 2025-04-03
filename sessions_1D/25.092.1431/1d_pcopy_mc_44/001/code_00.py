import copy

"""
Transforms a 1D sequence of colors based on the following rules:
1. Identifies existing horizontal blocks of three identical, non-white pixels in the input sequence.
2. Identifies single non-white pixels in the input sequence that are surrounded by white (0) pixels on both sides.
3. Initializes an output sequence of the same length as the input, filled with white (0).
4. Copies the identified 3-pixel blocks from the input directly to the output sequence.
5. For each identified single pixel of color 'C' at input index 'i', writes the color 'C' to the output sequence at indices 'i-1', 'i', and 'i+1', effectively expanding the single pixel into a 3-pixel block shifted one position left relative to the original single pixel's position.
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
    # Initialize output_grid with the same length as input_grid, filled with white (0)
    output_grid = [0] * n 
    
    # Step 1 & 4: Identify and copy existing 3-pixel blocks
    # Iterate through the input sequence to find blocks of three identical non-white pixels
    i = 0
    while i <= n - 3:
        # Check for a block of three identical non-white pixels
        if input_grid[i] != 0 and input_grid[i] == input_grid[i+1] == input_grid[i+2]:
            # Copy the block to the output grid
            output_grid[i] = input_grid[i]
            output_grid[i+1] = input_grid[i+1]
            output_grid[i+2] = input_grid[i+2]
            # Skip the next two positions as they are part of the block
            i += 3 
        else:
            i += 1

    # Step 2, 3, 5: Identify single pixels and expand them in the output
    # Iterate through the input sequence, checking pixels from index 1 to n-2
    for i in range(1, n - 1):
        pixel_color = input_grid[i]
        # Check if the current pixel is non-white and surrounded by white pixels
        if pixel_color != 0 and input_grid[i-1] == 0 and input_grid[i+1] == 0:
            # Found a single pixel. Expand it into a 3-pixel block in the output grid.
            # The block covers indices i-1, i, and i+1.
            output_grid[i-1] = pixel_color
            output_grid[i] = pixel_color
            output_grid[i+1] = pixel_color
            
    # Return the completed output sequence
    return output_grid