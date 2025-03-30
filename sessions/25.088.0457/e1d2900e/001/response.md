```python
import numpy as np

"""
Transforms an input grid into an output grid based on the following rule:
Initialize the output grid as a copy of the input grid. Iterate through each pixel of the input grid. If a pixel is white (0), check its orthogonal neighbors (up, down, left, right). If the white pixel has at least one red (2) neighbor AND at least one blue (1) neighbor in the input grid, change the corresponding pixel in the output grid to blue (1). Otherwise, the pixel retains its original color.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the rule described above.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to a NumPy array for easier manipulation and copying
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = input_np.copy()
    
    height, width = input_np.shape

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is white (0)
            if input_np[r, c] == 0:
                # Initialize flags to track neighbors
                found_red_neighbor = False
                found_blue_neighbor = False
                
                # Define orthogonal neighbor offsets
                neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                
                # Examine orthogonal neighbors
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_color = input_np[nr, nc]
                        # Check for red neighbor
                        if neighbor_color == 2:
                            found_red_neighbor = True
                        # Check for blue neighbor
                        elif neighbor_color == 1:
                            found_blue_neighbor = True
                            
                    # Optimization: If both types of neighbors are found, no need to check further
                    if found_red_neighbor and found_blue_neighbor:
                        break
                        
                # If both a red and a blue neighbor were found for the white pixel
                if found_red_neighbor and found_blue_neighbor:
                    # Change the corresponding pixel in the output grid to blue (1)
                    output_grid[r, c] = 1
                    
    # Return the final transformed grid
    return output_grid.tolist() # Convert back to list of lists if required by ARC interface

```