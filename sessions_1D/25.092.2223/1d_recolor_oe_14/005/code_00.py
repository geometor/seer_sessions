import numpy as np

"""
Transforms a 1xN input grid by changing the color of contiguous runs of maroon (9) pixels based on the parity of their length.
White (0) pixels remain unchanged.
- Runs of maroon pixels with even length become blue (1).
- Runs of maroon pixels with odd length become azure (8).
The output grid has the same 1xN shape as the input grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D NumPy array (expected shape 1xN) representing the input grid.

    Returns:
        A 2D NumPy array with the same shape as the input, containing the transformed grid.
    """
    # Store the original shape of the input grid
    original_shape = input_grid.shape
    
    # Flatten the input grid to a 1D array for easier run processing
    # Using [0] assumes the input is always 1xN as seen in examples
    # A more robust way would be input_grid.flatten(), but we follow the observed pattern.
    if original_shape[0] != 1:
        # This case isn't expected based on examples, but handle defensively
        # print(f"Warning: Expected input shape 1xN, got {original_shape}. Flattening.")
        input_sequence = input_grid.flatten()
    else:
         # Directly access the first (and only) row
        input_sequence = input_grid[0]

    # Create a mutable copy for the output sequence
    output_sequence = list(input_sequence) 
    n = len(output_sequence)
    
    # Initialize index to iterate through the sequence
    i = 0
    while i < n:
        # Get the color of the current pixel and start index of the run
        current_color = output_sequence[i]
        start_index = i
        
        # Find the end of the current contiguous run of the same color
        j = i + 1
        while j < n and output_sequence[j] == current_color:
            j += 1
        
        # Calculate the length of the run
        run_length = j - start_index
        
        # Apply transformation logic ONLY if the run color is maroon (9)
        if current_color == 9:
            # Determine the output color based on run length parity
            # Blue (1) for even length, Azure (8) for odd length
            output_color = 1 if run_length % 2 == 0 else 8
            
            # Fill the corresponding segment in the output sequence with the new color
            for k in range(start_index, j):
                output_sequence[k] = output_color
                
        # If the color is white (0), no action is needed as the output_sequence
        # was initialized with these values.
        
        # Move the index to the start of the next run
        i = j
        
    # Convert the list back to a NumPy array
    output_array_1d = np.array(output_sequence)
    
    # Reshape the 1D array back to the original 2D shape
    output_grid = output_array_1d.reshape(original_shape)
        
    return output_grid