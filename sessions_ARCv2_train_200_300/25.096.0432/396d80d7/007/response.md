```python
"""
Transforms an input grid by identifying a background color (most frequent), 
pattern colors (others), a trigger color (max of pattern colors), and a 
fill color (min of pattern colors). It then iterates through the grid. 
If a cell has the background color AND is adjacent (including diagonals) 
to a cell with the trigger color in the original input grid AND is NOT 
adjacent (including diagonals) to a cell with the fill color in the 
original input grid, its color in the output grid is changed to the 
fill color. Otherwise, the cell retains its original color.
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
        - background_color (int or None if grid is empty/invalid)
        - pattern_colors (set of int)
        - trigger_color (int or None if no pattern)
        - fill_color (int or None if no pattern)
    """
    # Handle empty grid case
    if grid.size == 0:
        return None, set(), None, None
        
    flat_grid = grid.flatten()
    counts = Counter(flat_grid)
    
    # Handle case where Counter might be empty (though unlikely with size check)
    if not counts: 
        return None, set(), None, None
        
    # Assume background color is the most frequent one
    background_color = counts.most_common(1)[0][0]
    
    # Pattern colors are all colors except the background
    pattern_colors = set(counts.keys()) - {background_color}
    
    trigger_color = None
    fill_color = None
    # Determine trigger and fill colors only if pattern colors exist
    if pattern_colors:
        trigger_color = max(pattern_colors)
        fill_color = min(pattern_colors)
        
    return background_color, pattern_colors, trigger_color, fill_color

def _get_neighbor_colors(grid: np.ndarray, r: int, c: int) -> set[int]:
    """
    Gets the set of unique colors of the 8 neighbors (Moore neighborhood) of cell (r, c).
    
    Args:
        grid: The input grid (numpy array).
        r: Row index of the cell.
        c: Column index of the cell.
        
    Returns:
        A set containing the unique integer colors of the valid neighbors.
    """
    rows, cols = grid.shape
    neighbor_colors = set()
    # Iterate through all 8 relative neighbor coordinates
    for dr, dc in itertools.product([-1, 0, 1], repeat=2):
        # Skip the cell itself (dr=0, dc=0)
        if dr == 0 and dc == 0:  
            continue
            
        # Calculate absolute neighbor coordinates
        nr, nc = r + dr, c + dc
        
        # Check if neighbor coordinates are within grid boundaries
        if 0 <= nr < rows and 0 <= nc < cols:
            # Add the neighbor's color to the set
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
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input case immediately
    if input_array.size == 0:
        return []
        
    # Initialize output_grid as a copy of the input. Cells will be modified directly in this copy.
    output_array = np.copy(input_array) 
    rows, cols = input_array.shape

    # Identify background, pattern, trigger, and fill colors using the helper function
    background_color, pattern_colors, trigger_color, fill_color = _find_colors(input_array)

    # If essential colors couldn't be determined (e.g., only background color exists), return the original grid
    if not pattern_colors or trigger_color is None or fill_color is None or background_color is None:
        return input_grid 

    # Iterate through each cell of the input grid by row and column index
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the *input* grid has the background color
            if input_array[r, c] == background_color:
                
                # Get the set of colors present in the neighbors of the current cell (in the *input* grid)
                neighbor_colors = _get_neighbor_colors(input_array, r, c)
                
                # Check condition 1: Is the cell adjacent to the trigger_color?
                is_adj_trigger = trigger_color in neighbor_colors
                
                # Check condition 2: Is the cell adjacent to the fill_color?
                is_adj_fill = fill_color in neighbor_colors
                
                # Apply the transformation rule: 
                # Change the cell in the output if it's a background cell, 
                # AND it is adjacent to the trigger color, 
                # AND it is NOT adjacent to the fill color.
                if is_adj_trigger and not is_adj_fill:
                    # If all conditions are met, update the corresponding cell in the output grid to the fill color
                    output_array[r, c] = fill_color
            
            # If the cell is not background color or the conditions are not met, 
            # the output_array cell retains its originally copied value from the input_array.

    # Convert the final NumPy array back to a list of lists for the expected output format
    output_grid = output_array.tolist()
    return output_grid
```