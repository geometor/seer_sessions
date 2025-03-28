import numpy as np

def find_background_color(grid):
    """Finds the dominant non-white color in the grid."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    # Sort by count descending
    sorted_indices = np.argsort(-counts)
    for idx in sorted_indices:
        color = unique_colors[idx]
        if color != 0: # 0 is white
            return color
    # Default fallback if only white is present (shouldn't happen based on examples)
    return 0 

def transform(input_grid):
    """
    Transforms a 15x15 input grid into a 3x3 output grid.

    The transformation involves downscaling the input grid by a factor of 5.
    Each 5x5 block in the input grid maps to a single pixel in the output grid.
    If a 5x5 block in the input contains at least one white pixel (0), the 
    corresponding pixel in the output grid becomes white (0). Otherwise, 
    the output pixel takes the background color of the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get input dimensions
    input_height, input_width = input_np.shape
    
    # Determine output dimensions (fixed at 3x3 based on examples)
    output_height = 3
    output_width = 3
    
    # Calculate the scaling factor
    scale_factor_h = input_height // output_height
    scale_factor_w = input_width // output_width
    
    # Ensure the scaling factor is consistent (5x5 in this case)
    if scale_factor_h != 5 or scale_factor_w != 5 or input_height % output_height != 0 or input_width % output_width != 0:
        # Handle potential errors or different scaling scenarios if needed
        # For this specific task, we assume 15x15 -> 3x3 with scale 5
        print(f"Warning: Unexpected input dimensions or scaling factor. Assuming 15x15 input and 5x5 blocks.")
        scale_factor = 5
    else:
        scale_factor = scale_factor_h # or scale_factor_w, they are the same

    # Identify the background color (the dominant non-white color)
    background_color = find_background_color(input_np)

    # Initialize the output grid with the background color
    output_np = np.full((output_height, output_width), background_color, dtype=int)

    # Iterate through the output grid cells
    for out_r in range(output_height):
        for out_c in range(output_width):
            # Determine the corresponding 5x5 block boundaries in the input grid
            start_r = out_r * scale_factor
            end_r = start_r + scale_factor
            start_c = out_c * scale_factor
            end_c = start_c + scale_factor

            # Extract the 5x5 block from the input grid
            input_block = input_np[start_r:end_r, start_c:end_c]

            # Check if any pixel in the block is white (0)
            if np.any(input_block == 0):
                # If a white pixel is found, set the corresponding output pixel to white
                output_np[out_r, out_c] = 0
            # Else: the output pixel remains the background color (already initialized)

    # Convert the output numpy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid