import numpy as np

def find_unique_non_white_color(grid):
    """
    Finds the unique non-white color in the grid.
    Assumes there is exactly one non-white color.
    Returns 0 if only white is present or if multiple non-white colors exist (error case).
    """
    unique_colors = np.unique(grid)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) == 1:
        return non_white_colors[0]
    elif len(non_white_colors) == 0:
        # Handle case where input is all white - return white as fill color?
        # Based on examples, this shouldn't happen, but default to 0.
        return 0 
    else:
        # Handle error: multiple non-white colors found.
        # Based on examples, this shouldn't happen. Returning 0 as a fallback.
        print(f"Warning: Found multiple non-white colors {non_white_colors}. Using 0.")
        return 0 


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by scaling it 3x. 
    For each white pixel in the input, a specific 4-pixel pattern is drawn 
    in the corresponding 3x3 output block using the unique non-white color 
    found in the input grid. Blocks corresponding to non-white input pixels 
    remain white.

    The pattern coordinates relative to the top-left of the 3x3 block are:
    (0, 2), (1, 0), (2, 0), (2, 2).
    """
    # 1. Determine input dimensions
    input_height, input_width = input_grid.shape

    # 2. Calculate output dimensions
    output_height = input_height * 3
    output_width = input_width * 3

    # 3. Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=input_grid.dtype)

    # 4. Identify the unique non-white color in the input grid
    fill_color = find_unique_non_white_color(input_grid)
    
    # If fill_color is 0 (meaning input was all white or error), the output will remain all white.
    if fill_color == 0:
        return output_grid # Early exit if no pattern color

    # Define the pattern relative offsets
    pattern_offsets = [(0, 2), (1, 0), (2, 0), (2, 2)]

    # 5. Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # 6a. Check if the input pixel is white
            if input_grid[r, c] == 0:
                # 6b. If white, apply the pattern in the corresponding output block
                
                # Calculate the top-left corner of the 3x3 output block
                block_r_start = r * 3
                block_c_start = c * 3

                # Place the pattern using fill_color
                for r_off, c_off in pattern_offsets:
                    out_r = block_r_start + r_off
                    out_c = block_c_start + c_off
                    # Basic bounds check (though unlikely needed with 3x scaling)
                    if 0 <= out_r < output_height and 0 <= out_c < output_width:
                        output_grid[out_r, out_c] = fill_color
            
            # 6c. If the input pixel is not white, do nothing (output block stays white)

    # 7. Return the completed output grid
    return output_grid