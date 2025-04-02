import numpy as np # Using numpy for potential array operations, though lists suffice here

"""
Identify the main contiguous sequence of pixels whose color is not white (0) and not red (2). 
Record its color (`fill_color`) and the index of its last pixel (`end_index`).
Identify the index of the single red pixel (color 2) (`boundary_index`).
Iterate through the indices from `end_index + 1` up to (but not including) `boundary_index`.
For each index in this range, change the color of the pixel at that index to `fill_color`.
Leave all other pixels unchanged. The resulting sequence is the output.
"""

def transform(input_grid):
    """
    Transforms the input grid (represented as a 1D list) by finding a colored 
    sequence (not white or red) and extending it to the right until it reaches 
    a red boundary pixel.

    Args:
        input_grid (list): A 1D list of integers representing the input grid pixels.
                           It could also be a numpy array or a list of lists 
                           representing a single row, which will be flattened.

    Returns:
        list: A 1D list representing the transformed output grid pixels.
    """
    
    # --- Data Handling: Ensure input is a flat list ---
    # The examples strongly suggest a 1D structure. This handles common formats.
    if isinstance(input_grid, np.ndarray):
        # Flatten numpy array to list
        flat_input = input_grid.flatten().tolist()
    elif isinstance(input_grid, list) and input_grid and isinstance(input_grid[0], list):
        # Flatten list of lists (assuming it represents a single row or needs flattening)
        # For this specific task, seems like it's always one row.
        if len(input_grid) == 1:
             flat_input = input_grid[0]
        else:
             # If truly multi-row, the logic might need reconsideration,
             # but based on examples, flatten seems appropriate.
             flat_input = [item for sublist in input_grid for item in sublist]
    else:
        # Assume it's already a flat list
        flat_input = input_grid

    # Initialize output_grid as a copy of the input to preserve unchanged pixels
    output_grid = list(flat_input)
    
    # --- Perception: Find key elements ---
    fill_color = -1       # Color of the sequence to be extended
    end_index = -1        # Index of the last pixel of the sequence
    boundary_index = -1   # Index of the red boundary pixel (color 2)
    
    # Iterate through the input grid to find the sequence and boundary
    # We assume the relevant sequence is the last contiguous block of non-white/non-red
    # color that appears *before* the red pixel.
    for i, pixel in enumerate(flat_input):
        # Check for the boundary pixel (red = 2)
        if pixel == 2:
            boundary_index = i
            # Optimization: Once the boundary is found, we don't need to check further
            # for the sequence end, as we only care about sequences *before* it.
            # However, we continue the loop in case the red pixel appears early
            # and the sequence we care about is later (before the *actual* last red pixel).
            # For simplicity and based on examples, we assume one red pixel acts as boundary.
            
        # Check for non-background (white = 0) and non-boundary (red = 2) pixels
        elif pixel != 0: 
            # This pixel belongs to a potential fill sequence.
            # Update the color and the last seen index for this sequence type.
            # If multiple sequences exist before the boundary, this captures the color
            # and end index of the one immediately preceding the gap/boundary.
            if boundary_index == -1: # Only track sequences before the boundary is found
               fill_color = pixel
               end_index = i
            # If boundary *is* found, we stop updating sequence info.
            
    # Re-iterate to find the definitive boundary index if multiple '2's exist.
    # The rule seems to imply the first '2' after the sequence matters.
    # Let's refine: Find the first '2' *after* the 'end_index'.
    boundary_index = -1 # Reset boundary index
    if end_index != -1: # Only search for boundary if a sequence was found
        for i in range(end_index + 1, len(flat_input)):
            if flat_input[i] == 2:
                boundary_index = i
                break # Found the first boundary after the sequence

    # --- Action: Apply Transformation ---
    # Check if a valid sequence and a subsequent boundary were found
    if fill_color != -1 and boundary_index != -1 and end_index < boundary_index -1:
        # Fill the gap between the sequence end and the boundary
        # Iterate from the index immediately after the sequence ends (`end_index + 1`)
        # up to (but not including) the boundary index (`boundary_index`).
        for i in range(end_index + 1, boundary_index):
            # Change the pixel color in the output grid to the fill color
            output_grid[i] = fill_color
            
    # Return the modified grid
    return output_grid