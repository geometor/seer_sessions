import copy

"""
Transforms a 1D input array by identifying isolated non-white pixels (pattern 0 C 0) 
and expanding them into a block of three identical pixels (C C C) in the output array. 
All other pixels, including existing blocks of three identical non-white pixels (C C C), 
are copied directly from the input to the output.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (represented as a 1D list).

    Args:
        input_grid: A list of integers representing the input 1D pixel array.

    Returns:
        A list of integers representing the transformed 1D pixel array.
    """
    
    # Ensure input is treated as a list if it's not already (e.g., if passed as a tuple)
    input_list = list(input_grid)
    n = len(input_list)
    
    # Initialize output_grid as a deep copy of the input_grid
    # This ensures that parts of the grid not matching the transformation pattern are preserved.
    output_grid = copy.deepcopy(input_list)

    # Iterate through the input list, checking for the '0 C 0' pattern
    # We iterate from the second element (index 1) to the second-to-last element (index n-2)
    # to ensure we can safely access neighbors at i-1 and i+1.
    for i in range(1, n - 1):
        # Get the current pixel and its neighbors
        left_neighbor = input_list[i-1]
        current_pixel = input_list[i]
        right_neighbor = input_list[i+1]

        # Check if the pattern '0 C 0' exists:
        # left neighbor is white (0), current pixel is non-white (C != 0), right neighbor is white (0)
        if left_neighbor == 0 and current_pixel != 0 and right_neighbor == 0:
            # If the pattern is found, apply the transformation to the output grid:
            # Replace the '0 C 0' sequence with 'C C C' in the output grid.
            output_grid[i-1] = current_pixel
            output_grid[i]   = current_pixel
            output_grid[i+1] = current_pixel

    # Return the modified output grid
    return output_grid