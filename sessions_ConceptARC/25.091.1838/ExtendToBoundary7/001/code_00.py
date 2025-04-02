import numpy as np

"""
Draw lines from colored source pixels towards a central gray barrier line. 

The transformation identifies a single horizontal or vertical gray line (color 5) 
which acts as a barrier. It then finds all 'source' pixels (any color other than 
white (0) or gray (5)). For each source pixel, a line of the same color is drawn 
from the source pixel's position towards the gray barrier, stopping one pixel 
short of the barrier. If the barrier is horizontal, vertical lines are drawn. 
If the barrier is vertical, horizontal lines are drawn.
"""

def find_barrier(grid):
    """
    Finds the gray barrier line (color 5) and returns its orientation and index.
    Returns:
        tuple: ('horizontal' or 'vertical', index) or (None, None) if no barrier found.
    """
    rows, cols = grid.shape
    
    # Check for horizontal barrier
    for r in range(rows):
        if np.all(grid[r, :] == 5):
            return 'horizontal', r
            
    # Check for vertical barrier
    for c in range(cols):
        if np.all(grid[:, c] == 5):
            return 'vertical', c
            
    # Check for partial horizontal barrier (might be needed if line doesn't span full width/height)
    for r in range(rows):
        gray_indices = np.where(grid[r, :] == 5)[0]
        if len(gray_indices) > 1 and np.all(np.diff(gray_indices) == 1): # contiguous
             # Check if *only* gray and background exist in the row/col
             if np.all((grid[r, :] == 5) | (grid[r, :] == 0)):
                 return 'horizontal', r

    # Check for partial vertical barrier
    for c in range(cols):
        gray_indices = np.where(grid[:, c] == 5)[0]
        if len(gray_indices) > 1 and np.all(np.diff(gray_indices) == 1): # contiguous
            if np.all((grid[:, c] == 5) | (grid[:, c] == 0)):
                return 'vertical', c

    # If still not found, look for any line of gray
    for r in range(rows):
        if np.any(grid[r, :] == 5) and np.all(grid[r, grid[r, :] != 0] == 5):
             # More robust check for rows containing only gray and background
             unique_vals = np.unique(grid[r, :])
             if np.array_equal(np.sort(unique_vals), [0, 5]) or np.array_equal(unique_vals, [5]):
                 return 'horizontal', r

    for c in range(cols):
         if np.any(grid[:, c] == 5) and np.all(grid[grid[:, c] != 0, c] == 5):
             # More robust check for columns containing only gray and background
             unique_vals = np.unique(grid[:, c])
             if np.array_equal(np.sort(unique_vals), [0, 5]) or np.array_equal(unique_vals, [5]):
                 return 'vertical', c


    return None, None # Should not happen based on examples, but good practice

def find_sources(grid):
    """
    Finds all source pixels (not white 0 or gray 5).
    Returns:
        list: A list of tuples, where each tuple is (row, col, color).
    """
    sources = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color != 5:
                sources.append((r, c, color))
    return sources

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Find the gray barrier line
    barrier_orientation, barrier_index = find_barrier(input_np)
    
    if barrier_orientation is None:
        # If no barrier is found, return the original grid (or handle as error)
        return input_grid 
        
    # Find all source pixels
    source_pixels = find_sources(input_np)
    
    # Process each source pixel
    for r, c, color in source_pixels:
        if barrier_orientation == 'horizontal':
            # Draw vertical line towards the horizontal barrier
            if r < barrier_index: # Source is above barrier
                # Fill pixels from source row 'r' down to 'barrier_index - 1'
                output_grid[r : barrier_index, c] = color
            elif r > barrier_index: # Source is below barrier
                # Fill pixels from 'barrier_index + 1' up to source row 'r'
                # Note: range in numpy slicing is exclusive of the end, so r+1 includes r
                output_grid[barrier_index + 1 : r + 1, c] = color
                
        elif barrier_orientation == 'vertical':
            # Draw horizontal line towards the vertical barrier
            if c < barrier_index: # Source is left of barrier
                # Fill pixels from source col 'c' right to 'barrier_index - 1'
                output_grid[r, c : barrier_index] = color
            elif c > barrier_index: # Source is right of barrier
                # Fill pixels from 'barrier_index + 1' left to source col 'c'
                # Note: range in numpy slicing is exclusive of the end, so c+1 includes c
                output_grid[r, barrier_index + 1 : c + 1] = color

    # Convert the result back to a list of lists
    return output_grid.tolist()