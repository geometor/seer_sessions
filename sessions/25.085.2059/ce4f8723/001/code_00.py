"""
Combine information from two spatially corresponding sections of the input grid, 
separated by a horizontal yellow (4) marker line. The output pixel is green (3) 
if either of the corresponding input pixels in the top or bottom sections is 
non-white (blue(1) or red(2)). Otherwise, the output pixel is white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on combining information from sections above 
    and below a yellow separator line.
    """
    # Convert input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Identify the row index of the horizontal yellow (4) separator line.
    separator_row_index = -1
    for r in range(input_array.shape[0]):
        if np.all(input_array[r, :] == 4):
            separator_row_index = r
            break
            
    # Handle case where separator isn't found (though unlikely based on examples)
    if separator_row_index == -1:
        # Maybe return input or raise error, depending on desired behavior
        # For now, let's assume it's always present based on the task description
        print("Warning: Separator row not found.") 
        return input_grid # Or raise ValueError("Separator row not found")

    # 2. Define the 'top half' as the region above the separator line.
    top_half = input_array[0:separator_row_index, :]
    
    # 3. Define the 'bottom half' as the region below the separator line.
    # The corresponding rows start from separator_row_index + 1
    bottom_half = input_array[separator_row_index + 1:, :]

    # Ensure top and bottom halves have the same dimensions for pixel-wise comparison
    if top_half.shape != bottom_half.shape:
        # This case shouldn't happen based on the examples, but good to check
        raise ValueError("Top and bottom sections have different dimensions.")

    # 4. Create a new output grid with the same dimensions as the 'top half'.
    # Initialize with white (0) pixels.
    output_height, output_width = top_half.shape
    output_array = np.zeros((output_height, output_width), dtype=int)

    # 5. Iterate through each cell (r, c) of the 'top half'.
    for r in range(output_height):
        for c in range(output_width):
            # 6. Examine the colors of the corresponding cells.
            top_pixel = top_half[r, c]
            bottom_pixel = bottom_half[r, c]

            # 7. If both examined cells are white (0), set output to white (0).
            # 8. Otherwise (if at least one is non-white), set output to green (3).
            if top_pixel == 0 and bottom_pixel == 0:
                output_array[r, c] = 0
            else:
                # The condition is met if top_pixel is blue (1) or bottom_pixel is red (2),
                # or if top_pixel is blue(1) and bottom_pixel is white(0),
                # or if top_pixel is white(0) and bottom_pixel is red(2).
                # Essentially, if either is not white(0).
                output_array[r, c] = 3

    # 9. Return the completed output grid (convert back to list of lists).
    return output_array.tolist()