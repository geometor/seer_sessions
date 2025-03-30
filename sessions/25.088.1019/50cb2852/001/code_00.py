import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by changing the color of interior pixels of solid,
    non-white rectangular objects to azure (8). An interior pixel is defined as a
    non-white pixel whose four cardinal neighbors (up, down, left, right) are
    all the same color as the pixel itself. The border pixels of the rectangles
    and the background pixels remain unchanged.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    height, width = input_grid.shape
    
    # Iterate through each pixel P in the input grid, excluding the outermost border
    # The outermost border pixels cannot have 4 neighbors of the same color by definition
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Get the color of the current pixel P
            current_color = input_grid[r, c]
            
            # Check if the pixel is not white (background color 0)
            if current_color != 0:
                # Check the colors of the four cardinal neighbors
                neighbor_up = input_grid[r - 1, c]
                neighbor_down = input_grid[r + 1, c]
                neighbor_left = input_grid[r, c - 1]
                neighbor_right = input_grid[r, c + 1]
                
                # If all four neighbors have the same color as the current pixel
                if (neighbor_up == current_color and
                    neighbor_down == current_color and
                    neighbor_left == current_color and
                    neighbor_right == current_color):
                    # Change the color of the corresponding pixel in the output grid to azure (8)
                    output_grid[r, c] = 8
                    
    # Return the modified output grid
    return output_grid