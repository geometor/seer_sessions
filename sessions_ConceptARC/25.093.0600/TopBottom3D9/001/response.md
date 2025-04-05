```python
import numpy as np

"""
Transformation Rule:
1. Identify all unique non-zero colors in the input grid.
2. Find the non-zero color that has at least one cell adjacent (up, down, left, right) 
   to a cell with the background color (0). This is the 'replacement_color'.
3. Identify all other non-zero colors as 'target_colors'.
4. Create the output grid by replacing every cell containing a 'target_color' 
   with the 'replacement_color'. Cells with the 'replacement_color' or the 
   background color (0) remain unchanged.
"""

def find_border_touching_color(grid, non_zero_colors):
    """Finds the non-zero color adjacent to the background (0)."""
    rows, cols = grid.shape
    background_color = 0
    
    # Check neighbors for each cell of each non-zero color
    for color in non_zero_colors:
        # Get coordinates of all cells with the current color
        coords = np.argwhere(grid == color)
        
        for r, c in coords:
            # Define potential neighbor offsets
            neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc
                
                # Check if neighbor coordinates are within grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if the neighbor cell is the background color
                    if grid[nr, nc] == background_color:
                        return color # This color touches the border
                        
    # This part should ideally not be reached if the problem assumptions hold
    # (i.e., there's always one color touching the border)
    print("Warning: No border-touching color found. Returning first non-zero color.")
    return non_zero_colors[0] if non_zero_colors else None


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies the color touching the '0' border and uses it to replace
    all other non-zero colors.
    """
    # Convert input list of lists to a numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(grid)
    
    # 1. Identify all unique non-zero colors
    unique_colors = np.unique(grid)
    non_zero_colors = unique_colors[unique_colors != 0].tolist()

    # Handle cases with no non-zero colors or only one non-zero color
    if not non_zero_colors:
        return output_grid.tolist() # No changes needed if no non-zero colors
    if len(non_zero_colors) == 1:
         return output_grid.tolist() # No changes needed if only one non-zero color

    # 2. Find the 'replacement_color' (the one touching the border)
    replacement_color = find_border_touching_color(grid, non_zero_colors)
    
    # 3. Identify 'target_colors' (all other non-zero colors)
    target_colors = [color for color in non_zero_colors if color != replacement_color]

    # 4. Replace 'target_colors' with 'replacement_color' in the output grid
    for target_color in target_colors:
        output_grid[output_grid == target_color] = replacement_color
        
    # Convert the result back to a list of lists if required by the environment,
    # but NumPy array is often convenient. Let's return list of lists.
    return output_grid.tolist()
```