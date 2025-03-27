```python
import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by creating a larger grid (2x height, 2x width) tiled with the input grid and its reflections.
    The output grid is composed of four quadrants:
    - Top-left: 180-degree rotation of the input grid.
    - Top-right: Vertical reflection of the input grid.
    - Bottom-left: Horizontal reflection of the input grid.
    - Bottom-right: The original input grid.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    H, W = input_np.shape

    # Create the output grid with double the dimensions, initialized with zeros (or any placeholder)
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)

    # Generate the necessary transformations
    # Original grid (bottom-right)
    original = input_np 
    
    # Horizontal reflection (reverse columns) (bottom-left)
    horizontal_reflection = input_np[:, ::-1] 
    
    # Vertical reflection (reverse rows) (top-right)
    vertical_reflection = input_np[::-1, :]
    
    # 180-degree rotation (reverse both rows and columns) (top-left)
    rotated_180 = input_np[::-1, ::-1]

    # Place the transformations into the correct quadrants of the output grid
    # Top-left quadrant (rows 0 to H-1, cols 0 to W-1)
    output_grid[0:H, 0:W] = rotated_180
    
    # Top-right quadrant (rows 0 to H-1, cols W to 2W-1)
    output_grid[0:H, W:2*W] = vertical_reflection
    
    # Bottom-left quadrant (rows H to 2H-1, cols 0 to W-1)
    output_grid[H:2*H, 0:W] = horizontal_reflection
    
    # Bottom-right quadrant (rows H to 2H-1, cols W to 2W-1)
    output_grid[H:2*H, W:2*W] = original

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```