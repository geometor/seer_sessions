```python
import numpy as np

"""
1. Initialize the output grid as a copy of the input grid.
2. Identify the two distinct non-white colors present in the input grid (let them be Color A and Color B).
3. Iterate through each pixel `(r, c)` in the input grid.
4. Let the color of the current pixel be `CurrentColor = input[r][c]`.
5. If `CurrentColor` is not white (i.e., it is either Color A or Color B):
    a. Check all 8 neighbors (adjacent and diagonal) of the pixel `(r, c)`.
    b. Search for a neighbor `(nr, nc)` whose color `NeighborColor = input[nr][nc]` is the *other* non-white color (i.e., `NeighborColor` is not white and `NeighborColor != CurrentColor`).
    c. If such a neighbor is found:
        i. This pixel `(r, c)` is an intersection point.
        ii. Update the color of the pixel in the output grid: `output[r][c] = NeighborColor`.
6. Return the final output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by changing the color of pixels belonging to one non-white object 
    to the color of an adjacent (including diagonal) pixel belonging to the *other* non-white object.
    """
    # Convert input list of lists to a numpy array
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # Find the unique non-white colors
    unique_colors = np.unique(input_array)
    non_white_colors = unique_colors[unique_colors != 0]

    # Check if we have exactly two non-white colors (as observed in examples)
    if len(non_white_colors) != 2:
        # If not exactly two, return the original grid or handle error appropriately
        # For now, just return the copy. Might need refinement if test cases differ.
        return output_array.tolist() 
        
    color_a, color_b = non_white_colors

    # Define the 8 neighbor offsets (row, col)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            current_color = input_array[r, c]

            # Process only non-white pixels
            if current_color == color_a or current_color == color_b:
                
                # Determine the 'other' non-white color
                other_color = color_b if current_color == color_a else color_a

                # Check all 8 neighbors
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_color = input_array[nr, nc]

                        # If a neighbor has the 'other' non-white color
                        if neighbor_color == other_color:
                            # Update the output grid pixel with the neighbor's color
                            output_array[r, c] = neighbor_color
                            # Once found, no need to check other neighbors for this pixel
                            break 

    # Convert the numpy array back to a list of lists before returning
    return output_array.tolist()
```