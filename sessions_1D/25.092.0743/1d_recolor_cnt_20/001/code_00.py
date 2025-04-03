import numpy as np

"""
This transformation rule identifies contiguous horizontal segments of azure pixels (8) 
in a 1D input grid and replaces them with segments of the same length but with a 
new color determined by the length of the original azure segment. 
White pixels (0) remain unchanged.

Mapping Rule:
- Azure segment of length 1 -> Magenta (6)
- Azure segment of length 2 -> Red (2)
- Azure segment of length 3 -> Blue (1)
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by recoloring azure segments based on their length.

    Args:
        input_grid: A numpy array representing the input grid (assumed 1xN).

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input to preserve non-azure pixels
    output_grid = np.copy(input_grid)
    
    # Get the dimensions (height will be 1 for these examples)
    height, width = input_grid.shape
    
    # Since the examples are 1D, we iterate through the single row
    # (though the code structure could handle multiple rows if needed)
    for i in range(height):
        j = 0  # Column index
        while j < width:
            # Check if the current pixel is azure (8)
            if input_grid[i, j] == 8:
                # Found the start of a potential azure segment
                start_j = j
                
                # Find the end of the contiguous azure segment
                end_j = start_j
                while end_j < width and input_grid[i, end_j] == 8:
                    end_j += 1
                
                # Calculate the length of the segment
                length = end_j - start_j
                
                # Determine the replacement color based on the length
                replacement_color = 0 # Default just in case
                if length == 1:
                    replacement_color = 6  # Magenta
                elif length == 2:
                    replacement_color = 2  # Red
                elif length == 3:
                    replacement_color = 1  # Blue
                else:
                    # If length is not 1, 2, or 3, keep the original color(s) 
                    # (already copied) or handle differently if needed.
                    # For this task, we only expect lengths 1, 2, 3.
                    # We'll just skip the update for unexpected lengths,
                    # effectively leaving the original azure pixels.
                     pass 

                # Fill the corresponding segment in the output grid if a replacement color was determined
                if replacement_color != 0: # Check if a valid length was found
                   output_grid[i, start_j:end_j] = replacement_color
                
                # Move the main index past the processed segment
                j = end_j
            else:
                # If the pixel is not azure, move to the next column
                j += 1
                
    return output_grid
