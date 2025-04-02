```python
import numpy as np

"""
Identify the two non-background (non-zero) colors in the input grid.
Count the pixels of each of these two colors.
Determine the 'dominant' color (CD) as the one with the strictly higher count, 
and the 'recessive' color (CR) as the one with the strictly lower count.
Create an output grid initialized as a copy of the input grid.
Iterate through each pixel of the input grid. 
If a pixel has the recessive color (CR) and has at least one neighbor 
(orthogonal or diagonal) with the dominant color (CD) in the input grid, 
change the color of that corresponding pixel in the output grid to the dominant color (CD).
Otherwise, the pixel retains its original color in the output grid.
If the counts of the two active colors are equal, no changes are made.
Return the modified output grid.
"""

def get_neighbors(grid_shape, r, c):
    """Gets the coordinates of the 8 neighbors of a cell within grid bounds."""
    height, width = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def has_dominant_neighbor(input_grid, r, c, dominant_color):
    """Checks if any neighbor of (r, c) in the input_grid has the dominant color."""
    neighbor_coords = get_neighbors(input_grid.shape, r, c)
    for nr, nc in neighbor_coords:
        if input_grid[nr, nc] == dominant_color:
            return True
    return False

def transform(input_grid):
    """
    Applies the color transformation based on neighbor dominance determined by counts.
    The color with the lower count changes to the color with the higher count 
    if adjacent (including diagonal) to the higher count color.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # Step 1: Identify Active Colors (non-background)
    unique_colors = np.unique(input_np)
    active_colors = unique_colors[unique_colors != 0]

    # If there are less than two active colors, no transformation is possible/needed
    if len(active_colors) < 2:
        return output_grid.tolist() 

    # Assuming exactly two active colors based on examples
    color1 = active_colors[0]
    color2 = active_colors[1]

    # Step 2: Count Active Colors
    count1 = np.count_nonzero(input_np == color1)
    count2 = np.count_nonzero(input_np == color2)

    # Step 3: Determine Dominant and Recessive Colors
    # If counts are equal, return the original grid (no change)
    if count1 == count2:
        return output_grid.tolist() 
        
    if count1 > count2:
        dominant_color = color1
        recessive_color = color2
    else: # count2 > count1
        dominant_color = color2
        recessive_color = color1

    # Step 4 & 5: Iterate and Update
    # Iterate through each cell in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the *input* grid has the recessive color
            if input_np[r, c] == recessive_color:
                # Check if any neighbor in the *input* grid has the dominant color
                if has_dominant_neighbor(input_np, r, c, dominant_color):
                    # If yes, change the corresponding cell in the *output* grid
                    output_grid[r, c] = dominant_color
            # Otherwise (pixel is not recessive or has no dominant neighbor), 
            # the output_grid cell retains its initially copied value.

    # Step 6: Final Output
    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist() 
```