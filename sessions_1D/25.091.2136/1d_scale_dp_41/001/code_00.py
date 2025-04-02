import numpy as np

"""
Fill white pixels (0) found between the end of the first contiguous block 
of a non-white, non-yellow color and the first occurrence of a yellow pixel (4) 
that appears after that block. The white pixels are replaced with the color 
of the identified block. The transformation is applied to the first row if the
input grid has multiple rows, or to the first column if the input grid has
multiple rows but only one column.
"""

def find_primary_block(vector: np.ndarray):
    """
    Finds the color and end index of the first non-white (0), non-yellow (4) 
    contiguous block in a 1D numpy array.

    Args:
        vector: A 1D numpy array representing a row or column.

    Returns:
        A tuple (primary_color, end_block_idx):
        - primary_color: The color (int) of the found block.
        - end_block_idx: The index of the last pixel of the block.
        Returns (None, -1) if no such block is found.
    """
    primary_color = None
    start_block_idx = -1
    end_block_idx = -1
    n = len(vector)

    for i in range(n):
        pixel = vector[i]
        # State 1: Looking for the start of the block
        if start_block_idx == -1:
            # Check if the pixel is neither white (0) nor yellow (4)
            if pixel != 0 and pixel != 4:  
                primary_color = pixel
                start_block_idx = i
                end_block_idx = i # Initialize end index
        # State 2: Inside a potential block, check if it continues
        elif pixel == primary_color:
            end_block_idx = i  # Extend block
        # State 3: Block has ended (pixel != primary_color) or different block found
        elif start_block_idx != -1:
            # We only care about the *first* contiguous block identified.
            # Once it ends (current pixel is different), stop searching.
            break 
            
    if start_block_idx != -1:
        # Return the identified color and the index of the last pixel of the block
        return primary_color, end_block_idx
    else:
        # No suitable primary block was found
        return None, -1

def find_marker(vector: np.ndarray, start_index: int, marker_color: int = 4):
    """
    Finds the index of the first occurrence of marker_color in a 1D numpy array,
    starting the search from start_index.

    Args:
        vector: A 1D numpy array representing a row or column.
        start_index: The index from where to begin the search.
        marker_color: The color value (int) to search for (default is 4, yellow).

    Returns:
        The index (int) of the first occurrence of marker_color, or -1 if not found.
    """
    n = len(vector)
    for i in range(start_index, n):
        if vector[i] == marker_color:
            return i
    return -1 # Marker not found

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by finding the first non-white/non-yellow block 
    and the subsequent yellow marker in the relevant row/column, then filling 
    any white pixels between them with the block's color.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Ensure input is a numpy array and create a copy to modify
    input_grid_np = np.array(input_grid)
    output_grid = np.copy(input_grid_np)

    # Check for empty grid
    if input_grid_np.shape[0] == 0 or input_grid_np.shape[1] == 0:
        return output_grid 

    # Determine if we process a row or a column based on shape
    # Prioritize column if it's Nx1 (N>1), otherwise process first row (index 0)
    is_column = False
    if input_grid_np.shape[1] == 1 and input_grid_np.shape[0] > 1:
        # It's a column vector (Nx1)
        vector_to_process = input_grid_np[:, 0] 
        is_column = True
    else:
        # It's a row vector (1xN) or a multi-row grid (MxN)
        # In MxN case, process the first row (index 0) as per examples
        row_index = 0
        vector_to_process = input_grid_np[row_index, :]

    # 1. Find the primary color block in the extracted vector
    primary_color, end_block_idx = find_primary_block(vector_to_process)

    # If no primary block found, no transformation needed
    if primary_color is None:
        return output_grid

    # 2. Find the yellow marker (4) positioned *after* the primary block ends
    # Start searching from the index immediately following the block's end
    search_start_idx = end_block_idx + 1
    yellow_idx = find_marker(vector_to_process, search_start_idx, marker_color=4)

    # 3. Check if a valid gap exists for filling
    # The yellow marker must be found (yellow_idx != -1)
    # There must be at least one index between the block and the marker (yellow_idx > search_start_idx)
    if yellow_idx == -1 or yellow_idx <= search_start_idx:
        # No marker found, or marker is immediately adjacent to the block (no gap)
        return output_grid 

    # 4. Fill the gap in the output grid
    # Iterate through the indices strictly between the end of the block and the yellow marker
    if is_column:
         # Modify the corresponding column in the output grid
         for i in range(search_start_idx, yellow_idx):
             # Check if the pixel at this position in the original grid is white (0)
             if output_grid[i, 0] == 0: 
                 output_grid[i, 0] = primary_color # Fill with primary color
    else: 
        # Modify the corresponding row (assumed index 0) in the output grid
        row_index = 0 # Explicitly state we're working on the first row
        for i in range(search_start_idx, yellow_idx):
             # Check if the pixel at this position in the original grid is white (0)
             if output_grid[row_index, i] == 0: 
                 output_grid[row_index, i] = primary_color # Fill with primary color

    # 5. Return the modified grid
    return output_grid