```python
import numpy as np

"""
Identify the two non-background (non-zero) colors in the input grid.
Count the pixels of each of these two colors.
Determine the 'dominant' color (CD) as the one with the strictly higher count, 
and the 'recessive' color (CR) as the one with the strictly lower count.
If counts are equal or fewer than two active colors exist, return the input grid unchanged.
Create an output grid initialized as a copy of the input grid.
Iterate through each pixel of the input grid. 
If a pixel has the recessive color (CR) and has 3 or more neighbors 
(orthogonal or diagonal) with the dominant color (CD) in the input grid, 
change the color of that corresponding pixel in the output grid to the dominant color (CD).
Otherwise, the pixel retains its original color in the output grid.
Return the modified output grid.
"""

def get_neighbors_coords(grid_shape, r, c):
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

def count_dominant_neighbors(input_grid, r, c, dominant_color):
    """Counts how many neighbors of (r, c) in the input_grid have the dominant color."""
    count = 0
    neighbor_coords = get_neighbors_coords(input_grid.shape, r, c)
    for nr, nc in neighbor_coords:
        if input_grid[nr, nc] == dominant_color:
            count += 1
    return count

def transform(input_grid):
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
    dominant_color = -1 # Placeholder
    recessive_color = -1 # Placeholder
    
    # If counts are equal, return the original grid (no change)
    if count1 == count2:
        return output_grid.tolist() 
        
    if count1 > count2:
        dominant_color = color1
        recessive_color = color2
    else: # count2 > count1
        dominant_color = color2
        recessive_color = color1

    # Step 4 & 5: Iterate and Update based on input grid state
    # Iterate through each cell in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the *input* grid has the recessive color
            if input_np[r, c] == recessive_color:
                # Count dominant neighbors in the *input* grid
                dominant_neighbor_count = count_dominant_neighbors(input_np, r, c, dominant_color)
                
                # Apply the transformation rule: >= 3 dominant neighbors
                if dominant_neighbor_count >= 3:
                    # If condition met, change the corresponding cell in the *output* grid
                    output_grid[r, c] = dominant_color
            # Otherwise (pixel is not recessive or has < 3 dominant neighbors), 
            # the output_grid cell retains its initially copied value.

    # Step 6: Final Output
    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()
```