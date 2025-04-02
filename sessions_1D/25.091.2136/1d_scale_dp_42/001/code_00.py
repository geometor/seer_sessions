import numpy as np

"""
Processes a 1D sequence of pixels (represented as a 1xN or Nx1 grid).
Iterates through the sequence, maintaining a 'current fill color' state, initialized to white (0).
If a non-white, non-magenta pixel is encountered before a magenta pixel, it updates the 'current fill color'.
If a white pixel is encountered before a magenta pixel, it is replaced with the 'current fill color'.
The process stops updating/filling once the first magenta pixel (color 6) is encountered.
All pixels from the magenta pixel onwards, the magenta pixel itself, and the original non-white pixels remain unchanged.
"""

def transform(input_grid):
    """
    Applies a color fill transformation bounded by the magenta color (6).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.
                                       Expected to be effectively 1D (1xN or Nx1).

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input grid to a NumPy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # Determine if the grid is 1xN or Nx1 and flatten accordingly
    if input_array.shape[0] == 1:
        flat_sequence = input_array[0, :]
        is_row = True
    elif input_array.shape[1] == 1:
        flat_sequence = input_array[:, 0]
        is_row = False
    else:
        # Assuming 1xN if not strictly 1xN or Nx1, based on examples
        # This might need adjustment if other shapes appear
        if input_array.shape[0] > 1 and input_array.shape[1] > 1:
             # Defaulting to row-major flatten if ambiguous, but this case seems unlikely based on examples
             flat_sequence = input_array.flatten()
             # Need to reconstruct shape later. Store original shape.
             original_shape = input_array.shape 
             # This fallback might be incorrect if the task isn't strictly 1D
             # However, given the provided examples, it seems safe to assume 1xN or Nx1.
             # Reverting to assuming 1xN if shape[0] > 1 but shape[1] > 1 doesn't make sense.
             # Let's stick to the explicit 1xN or Nx1 check and raise error otherwise for clarity
             raise ValueError("Input grid shape is not 1xN or Nx1")
        elif input_array.shape[0] == 1:
             flat_sequence = input_array[0, :]
             is_row = True
        else: # input_array.shape[1] == 1
             flat_sequence = input_array[:, 0]
             is_row = False


    # Initialize the output sequence as a copy of the flat sequence
    output_sequence = flat_sequence.copy()

    # Initialize state variables
    current_fill_color = 0  # Start with white
    magenta_seen = False
    
    # Iterate through the sequence
    for i, pixel_color in enumerate(flat_sequence):
        
        # Check if magenta has been seen already
        if magenta_seen:
            # If magenta boundary passed, do nothing, just keep original pixel
            continue 
            
        # Check if the current pixel is magenta
        if pixel_color == 6:
            magenta_seen = True
            # Magenta pixel itself is unchanged, and processing stops here
            continue 
            
        # If magenta has not been seen yet:
        # Check if the pixel is white
        if pixel_color == 0:
            # Change the white pixel to the current fill color
            output_sequence[i] = current_fill_color
        # Check if the pixel is non-white and non-magenta
        elif pixel_color != 6: # Already handled 0 above, so this covers 1,2,3,4,5,7,8,9
            # Update the fill color
            current_fill_color = pixel_color
            # This pixel itself remains unchanged
            
    # Reshape the output sequence back into the original grid format
    if is_row:
        output_grid = output_sequence.reshape(1, -1).tolist()
    else:
        output_grid = output_sequence.reshape(-1, 1).tolist()
        
    return output_grid