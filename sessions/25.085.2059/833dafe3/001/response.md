```python
import numpy as np

def transform(input_grid):
    """
    Creates an output grid by arranging four transformed versions of the input grid in a 2x2 layout.
    The bottom-right quadrant is the original input grid.
    The bottom-left quadrant is a horizontal reflection of the input.
    The top-right quadrant is a vertical reflection of the input.
    The top-left quadrant is a horizontal and vertical reflection (180-degree rotation) of the input.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get the height (H) and width (W) of the input grid
    H, W = input_np.shape

    # Calculate the dimensions of the output grid
    output_H = H * 2
    output_W = W * 2

    # Initialize the output grid with zeros (or any default background color)
    # Using the same dtype as the input array
    output_grid = np.zeros((output_H, output_W), dtype=input_np.dtype)

    # --- Populate the quadrants ---

    # 1. Bottom-right quadrant: Copy the original input grid
    output_grid[H:output_H, W:output_W] = input_np

    # 2. Bottom-left quadrant: Place the horizontally reflected input grid
    # np.fliplr flips the array left-to-right
    horizontally_reflected = np.fliplr(input_np)
    output_grid[H:output_H, 0:W] = horizontally_reflected

    # 3. Top-right quadrant: Place the vertically reflected input grid
    # np.flipud flips the array top-to-bottom
    vertically_reflected = np.flipud(input_np)
    output_grid[0:H, W:output_W] = vertically_reflected

    # 4. Top-left quadrant: Place the horizontally and vertically reflected input grid
    # This is equivalent to a 180-degree rotation
    # Can be achieved by flipping the vertically reflected grid horizontally,
    # or flipping the horizontally reflected grid vertically,
    # or flipping the original grid both ways.
    rotated_180 = np.flipud(np.fliplr(input_np))
    # Alternative: rotated_180 = np.rot90(input_np, 2)
    output_grid[0:H, 0:W] = rotated_180

    # Convert the numpy array back to a list of lists if required by the environment
    # return output_grid.tolist() 
    # Assuming the environment expects numpy arrays based on common ARC practices
    return output_grid

```