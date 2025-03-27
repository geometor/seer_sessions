import numpy as np
import copy

def transform(input_grid):
    """
    Processes the input grid row by row.
    For each row, identifies the colors from the set {1 (blue), 2 (red), 3 (green), 4 (yellow)} that are present.
    Determines which colors from this set are missing in the row.
    Finds the positions (columns) of the white (0) pixels in that row.
    Fills the white pixels in the row with the missing colors, assigning them in ascending order to the white pixels sorted by their column index.
    Non-white pixels remain unchanged.
    """
    
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original non-white pixels
    output_array = np.copy(input_array)
    
    height, width = input_array.shape
    
    # Define the set of colors that should ideally be present in each row (excluding white)
    target_colors = {1, 2, 3, 4}
    
    # Iterate through each row of the grid
    for r in range(height):
        # Get the current row
        row = input_array[r, :]
        
        # Find the colors present in the row (excluding white 0)
        present_colors = set(c for c in row if c in target_colors)
        
        # Determine the colors missing from the target set for this row
        missing_colors = sorted(list(target_colors - present_colors))
        
        # Find the column indices where the pixel is white (0)
        white_pixel_indices = [c for c in range(width) if row[c] == 0]
        
        # Ensure the number of missing colors matches the number of white pixels to fill
        # This check might be useful for debugging or handling unexpected inputs,
        # although based on examples, they should match.
        if len(missing_colors) == len(white_pixel_indices):
            # Iterate through the white pixel indices and assign the missing colors
            # The missing colors are assigned in ascending order
            # The white pixels are filled based on their column order (left-to-right)
            for i, col_index in enumerate(white_pixel_indices):
                output_array[r, col_index] = missing_colors[i]
        # else:
            # Optional: Handle cases where the counts don't match, though not observed in examples
            # print(f"Warning: Row {r} has {len(white_pixel_indices)} white pixels but {len(missing_colors)} missing colors.")
            
    # Convert the numpy array back to a list of lists for the final output format
    output_grid = output_array.tolist()
    
    return output_grid
