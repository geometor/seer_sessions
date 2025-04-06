"""
Transforms an input grid by identifying a background color, pattern colors, a trigger color (max of pattern colors), and a fill color (min of pattern colors). 
It then iterates through the grid. If a cell has the background color AND is adjacent (including diagonals) to a cell with the trigger color in the original input grid AND is NOT adjacent (including diagonals) to a cell with the fill color in the original input grid, its color in the output grid is changed to the fill color. Otherwise, the cell retains its original color.
"""

import numpy as np
from collections import Counter
import itertools

def _find_colors(grid: np.ndarray) -> tuple[int | None, set[int], int | None, int | None]:
    """
    Identifies the background color (most frequent), pattern colors (others),
    trigger color (max pattern), and fill color (min pattern).
    
    Args:
        grid: The input grid as a numpy array.
        
    Returns:
        A tuple containing:
        - background_color (int or None if grid is empty)
        - pattern_colors (set of int)
        - trigger_color (int or None if no pattern)
        - fill_color (int or None if no pattern)
    """
    if grid.size == 0:
        return None, set(), None, None
        
    flat_grid = grid.flatten()
    counts = Counter(flat_grid)
    
    # Assume background color is the most frequent one
    background_color = counts.most_common(1)[0][0]
    
    # Pattern colors are all colors except the background
    pattern_colors = set(counts.keys()) - {background_color}
    
    trigger_color = None
    fill_color = None
    if pattern_colors:
        trigger_color = max(pattern_colors)
        fill_color = min(pattern_colors)
        
    return background_color, pattern_colors, trigger_color, fill_color

def _get_neighbor_colors(grid: np.ndarray, r: int, c: int) -> set[int]:
    """
    Gets the set of unique colors of the 8 neighbors of cell (r, c).
    
    Args:
        grid: The input grid (numpy array).
        r: Row index of the cell.
        c: Column index of the cell.
        
    Returns:
        A set containing the unique integer colors of the valid neighbors.
    """
    rows, cols = grid.shape
    neighbor_colors = set()
    # Iterate through all 8 neighbors (Moore neighborhood) including diagonals
    for dr, dc in itertools.product([-1, 0, 1], repeat=2):
        if dr == 0 and dc == 0:  # Skip the cell itself
            continue
            
        nr, nc = r + dr, c + dc
        
        # Check boundary conditions
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbor_colors.add(grid[nr, nc])
                
    return neighbor_colors

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A 2D list representing the input grid.
        
    Returns:
        A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input case
    if input_array.size == 0:
        return []
        
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array) 
    rows, cols = input_array.shape

    # Identify background, pattern, trigger, and fill colors
    background_color, pattern_colors, trigger_color, fill_color = _find_colors(input_array)

    # If there are no pattern colors, or necessary colors are missing, return the original grid
    if not pattern_colors or trigger_color is None or fill_color is None or background_color is None:
        return input_grid 

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell has the background color
            if input_array[r, c] == background_color:
                # Get the colors of all neighbors in the *original* input grid
                neighbor_colors = _get_neighbor_colors(input_array, r, c)
                
                # Check condition: Is adjacent to trigger_color?
                is_adj_trigger = trigger_color in neighbor_colors
                
                # Check condition: Is adjacent to fill_color?
                is_adj_fill = fill_color in neighbor_colors
                
                # Apply transformation rule: Change if adjacent to trigger AND NOT adjacent to fill
                if is_adj_trigger and not is_adj_fill:
                    # If yes, change the corresponding cell in the output grid to the fill color
                    output_array[r, c] = fill_color

    # Convert the result back to a list of lists
    output_grid = output_array.tolist()
    return output_grid