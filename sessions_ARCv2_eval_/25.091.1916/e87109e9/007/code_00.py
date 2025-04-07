import numpy as np
from collections import deque, Counter

"""
Transforms an input grid by performing a flood fill operation on a specific subgrid.

1.  Extracts a subgrid (canvas) from the input grid, specifically rows 6 onwards 
    and columns 1 onwards. This canvas corresponds to the output grid dimensions.
2.  Identifies the 'background color' within this canvas, defined as the most 
    frequent color excluding Azure (8).
3.  Locates all initial 'seed' pixels within the canvas, which are pixels with 
    the Azure color (8).
4.  Performs a 4-directional flood fill (Breadth-First Search) starting from the 
    seed pixels.
5.  The fill operation changes pixels matching the identified background color to 
    Azure (8).
6.  The fill stops at the canvas boundaries or when encountering pixels that do 
    not match the background color (acting as barriers).
7.  If no background color is found (e.g., the canvas only contains Azure pixels 
    or is empty after exclusion) or if there are no seed pixels, the canvas is 
    returned unmodified.
8.  The final state of the canvas after the flood fill is the output.
"""

# === Helper Functions ===

def _get_subgrid(grid, start_row, start_col):
    """
    Extracts a subgrid from the specified starting row/col to the end.

    Args:
        grid (np.ndarray): The input grid.
        start_row (int): The starting row index (inclusive).
        start_col (int): The starting column index (inclusive).

    Returns:
        np.ndarray: A copy of the extracted subgrid. Returns an empty grid if
                    start indices are out of bounds.
    """
    rows, cols = grid.shape
    if start_row >= rows or start_col >= cols or start_row < 0 or start_col < 0:
        # Return an empty array of appropriate type if start is out of bounds
        # Using shape (0, cols-start_col) or similar might be more precise, 
        # but an empty 0x0 or 0xN is sufficient to indicate no valid subgrid.
        return np.array([[]], dtype=grid.dtype).reshape(0,0) 
        
    # Ensure slicing doesn't go negative if start indices are large
    # (Python slicing handles large indices gracefully by returning empty)
    return grid[start_row:, start_col:].copy()

def _find_most_frequent_excluding(grid, exclude_value):
    """
    Finds the most frequent value in a grid, excluding a specific value.

    Args:
        grid (np.ndarray): The input grid.
        exclude_value (int): The value to exclude from frequency counting.

    Returns:
        int or None: The most frequent value, or None if no other value exists 
                     or the grid is effectively empty after exclusion.
    """
    # Check for empty grid case
    if grid.size == 0:
        return None
        
    flat_grid = grid.flatten()
    filtered_values = flat_grid[flat_grid != exclude_value]
    
    # If no values remain after filtering, return None
    if filtered_values.size == 0:
        return None

    # Count occurrences of each remaining value
    counts = Counter(filtered_values)
    
    # Check if the Counter is empty (shouldn't happen if filtered_values.size > 0, but defensive)
    if not counts: 
        return None
        
    # Find the value with the highest count
    # counts.most_common(1) returns a list like [ (value, count) ]
    most_common_value = counts.most_common(1)[0][0] 
    return most_common_value

def _find_pixels_with_color(grid, color):
    """
    Finds the coordinates of all pixels with a specific color.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color value to search for.

    Returns:
        np.ndarray: An array of coordinates [(r1, c1), (r2, c2), ...]. 
                    Returns an empty (0, 2) array if no pixels match or grid is empty.
    """
    # Check for empty grid case
    if grid.size == 0:
        return np.array([], dtype=int).reshape(0, 2) # Return empty 2D array
    return np.argwhere(grid == color)

def _flood_fill_4_direction(grid, seeds, fill_color, target_color):
    """
    Performs a 4-directional flood fill in-place on the grid.

    Args:
        grid (np.ndarray): The grid to modify.
        seeds (np.ndarray): Array of seed coordinates [(r1, c1), ...].
        fill_color (int): The color to fill with.
        target_color (int or None): The color of pixels to be filled. If None,
                                    no filling occurs.

    Returns:
        np.ndarray: The modified grid (note: the input grid is modified in-place).
    """
    # Check for conditions where no fill should occur
    if target_color is None or seeds.size == 0 or grid.size == 0:
        return grid 
        
    rows, cols = grid.shape
    
    # Visited array is crucial to prevent infinite loops and re-processing
    visited = np.zeros_like(grid, dtype=bool)
    
    # Use deque for efficient BFS queue operations
    queue = deque() 

    # Initialize queue and visited array ONLY with valid seed pixels
    for r, c in seeds:
        # Check bounds for robustness, though seeds should be within canvas
        if 0 <= r < rows and 0 <= c < cols:
           # Check if the seed pixel itself hasn't been visited
           # (useful if seeds overlap or BFS starts immediately)
           if not visited[r, c]:
               # Mark the seed as visited
               visited[r, c] = True
               # Add the seed to the queue to start the BFS
               queue.append((r, c))
               # Note: We assume seeds already have the 'fill_color' and don't need changing.
               # If seeds could potentially have the 'target_color', they should be changed here.
               # Based on the problem, seeds are defined as already being 'fill_color' (Azure).

    # Perform Breadth-First Search (BFS)
    while queue:
        r, c = queue.popleft()

        # Define the four cardinal neighbors (relative offsets)
        # neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)] # Direct calculation below
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Deltas for neighbors
            nr, nc = r + dr, c + dc

            # Check 1: Is the neighbor within the grid boundaries?
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check 2: Does the neighbor have the target (background) color?
                # Check 3: Has the neighbor NOT been visited yet?
                if grid[nr, nc] == target_color and not visited[nr, nc]:
                    # All checks pass:
                    # - Mark as visited *before* changing color/adding to queue
                    visited[nr, nc] = True 
                    # - Change the neighbor's color to the fill color
                    grid[nr, nc] = fill_color
                    # - Add the neighbor to the queue for further expansion
                    queue.append((nr, nc))
                    
    return grid # Return the modified grid

# === Main Transformation Function ===

def transform(input_grid):
    """
    Applies the flood fill transformation based on the described rules:
    Extracts a subgrid, finds the most frequent non-azure color as background,
    locates azure seeds, and flood-fills the background from the seeds.
    
    Args:
        input_grid (np.ndarray): The 2D input grid.

    Returns:
        np.ndarray: The transformed 2D output grid (the modified subgrid).
    """
    # Define constants based on problem description/observation
    HEADER_ROWS = 6 # Number of rows to skip at the top
    START_COL = 1   # Starting column index for the subgrid (0-based)
    SEED_COLOR = 8  # Azure - the color that initiates the fill and is the fill color
    # FILL_COLOR = 8 # Azure - implicit, same as SEED_COLOR

    # 1. Extract the canvas (working area) from the input
    #    Handles potential empty input grid via helper function.
    canvas = _get_subgrid(input_grid, HEADER_ROWS, START_COL)

    # If the extracted canvas is empty, return it immediately
    if canvas.size == 0:
        # Consider what an empty output should look like. 
        # Returning the empty canvas seems appropriate.
        return canvas 

    # 2. Identify the background color to be filled (target color)
    #    Exclude the seed color itself from being the background.
    background_color = _find_most_frequent_excluding(canvas, SEED_COLOR)

    # 3. Find initial seed pixels (pixels that already have the seed color)
    #    These are the starting points for the flood fill.
    seed_coords = _find_pixels_with_color(canvas, SEED_COLOR)

    # 4. Perform flood fill
    #    - The function modifies 'canvas' in-place.
    #    - It fills pixels matching 'background_color' starting from 'seed_coords'.
    #    - Handles cases where background_color is None or no seeds are found internally.
    output_grid = _flood_fill_4_direction(canvas, seed_coords, SEED_COLOR, background_color)

    # 5. Return the modified canvas as the final output grid
    return output_grid