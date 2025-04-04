```python
"""
Identifies a horizontal pattern (motif) in the input grid formed by non-background (non-white/0) pixels. 
This motif is defined by the rows containing any non-background pixels.
The output grid is generated by vertically tiling this extracted motif, starting from the top row and repeating downwards until the entire output grid (which has the same dimensions as the input) is filled.
"""

import numpy as np

def find_non_background_rows(grid_np, background_color=0):
    """
    Finds the minimum and maximum row indices containing non-background pixels.

    Args:
        grid_np (np.array): The input grid as a numpy array.
        background_color (int): The value representing the background color.

    Returns:
        tuple: (min_row, max_row) indices, or (None, None) if no non-background pixels found.
    """
    # Find rows that contain at least one pixel different from the background color
    non_background_rows = np.where(np.any(grid_np != background_color, axis=1))[0]
    
    if len(non_background_rows) == 0:
        # Handle the case where the grid might be entirely background or empty
        return None, None 
        
    min_row = np.min(non_background_rows)
    max_row = np.max(non_background_rows)
    return min_row, max_row

def extract_motif(grid_np, min_row, max_row):
    """
    Extracts the motif slice (rows from min_row to max_row) from the grid.
    Based on the examples, the motif spans the full width of the grid within these rows.

    Args:
        grid_np (np.array): The input grid as a numpy array.
        min_row (int): The starting row index of the motif.
        max_row (int): The ending row index of the motif.

    Returns:
        np.array: The extracted motif.
    """
    if min_row is None or max_row is None:
        # Return an empty array if no valid rows were found
        return np.array([[]], dtype=int) 
        
    # Slice the grid to get the rows defining the motif
    motif = grid_np[min_row : max_row + 1, :]
    return motif

def tile_vertically(motif, output_height, output_width):
    """
    Creates a new grid by vertically tiling the provided motif.

    Args:
        motif (np.array): The pattern to tile.
        output_height (int): The desired height of the output grid.
        output_width (int): The desired width of the output grid.

    Returns:
        np.array: The resulting grid tiled with the motif.
    """
    motif_height = motif.shape[0]
    
    # Handle cases with empty motif or zero height
    if motif_height == 0 or motif.size == 0:
        # Return a grid filled with a default color, like background (0)
        return np.zeros((output_height, output_width), dtype=int)

    # Initialize the output grid
    # Ensure it matches the motif's width, assuming output_width matches input's
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # Fill the output grid by repeating the motif rows
    for r in range(output_height):
        # Calculate the corresponding row index in the motif using modulo
        source_row_index = r % motif_height
        # Copy the motif row to the output grid row
        # Ensure motif width matches output_width, otherwise this might error or broadcast unexpectedly.
        # Based on examples, motif width == grid width, so this should be fine.
        if motif.shape[1] == output_width:
             output_grid[r, :] = motif[source_row_index, :]
        else:
             # Handle potential width mismatch if necessary, though not expected from examples
             # For now, assume widths match
             print(f"Warning: Motif width {motif.shape[1]} does not match output width {output_width}. Tiling might be incorrect.")
             # Simple approach: Tile using the motif's width, potentially leaving parts of output grid empty/zero
             copy_width = min(motif.shape[1], output_width)
             output_grid[r, :copy_width] = motif[source_row_index, :copy_width]


    return output_grid

def transform(input_grid):
    """
    Transforms the input grid by extracting a horizontal pattern (motif) 
    and tiling it vertically to fill the output grid.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_grid_np.shape

    # Define the background color (assumed to be 0 based on examples)
    background_color = 0

    # 1. Identify the rows containing the non-background pattern
    min_row, max_row = find_non_background_rows(input_grid_np, background_color)

    # Handle case where no pattern is found (e.g., all background)
    if min_row is None:
        # Return a grid of zeros with the same dimensions
        return np.zeros_like(input_grid_np).tolist() 

    # 2. Extract the motif from the identified rows
    motif = extract_motif(input_grid_np, min_row, max_row)

    # 3. Create the output grid by tiling the motif vertically
    output_grid_np = tile_vertically(motif, input_height, input_width)

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```