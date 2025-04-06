```python
import math

"""
Identifies the single non-background pixel (not '8') in the input grid. 
Determines the 3x3 block containing this pixel. 
Creates an output grid of the same dimensions, filled initially with the background color '8'.
Fills the identified 3x3 block in the output grid with the color of the non-background pixel.
"""

def find_foreground_pixel(grid: list[list[int]], background_color: int) -> tuple[int, int, int]:
    """Finds the row, column, and color of the first pixel not matching the background color."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    for r in range(height):
        for c in range(width):
            if grid[r][c] != background_color:
                return r, c, grid[r][c]
    # Should not happen based on task description, but handle defensively
    return -1, -1, -1 

def calculate_block_origin(r: int, c: int, block_size: int = 3) -> tuple[int, int]:
    """Calculates the top-left corner (TL_r, TL_c) of the block containing (r, c)."""
    tl_r = (r // block_size) * block_size
    tl_c = (c // block_size) * block_size
    return tl_r, tl_c

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the non-background pixel and filling its 
    containing 3x3 block in the output grid with its color.
    """
    
    # Define constants
    background_color = 8
    block_size = 3
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Find the single foreground pixel's location and color
    fg_r, fg_c, fg_color = find_foreground_pixel(input_grid, background_color)

    # Handle edge case where no foreground pixel is found (though unlikely given examples)
    if fg_r == -1:
        # Return a grid filled only with background color if no foreground pixel is found
        return [[background_color for _ in range(width)] for _ in range(height)]
        
    # Calculate the top-left corner of the 3x3 block containing the foreground pixel
    tl_r, tl_c = calculate_block_origin(fg_r, fg_c, block_size)

    # Initialize the output grid with the background color
    output_grid = [[background_color for _ in range(width)] for _ in range(height)]

    # Fill the 3x3 block in the output grid with the foreground color
    # Ensure the loop doesn't go out of grid bounds, although the block origin calculation 
    # combined with the foreground pixel existing should prevent this.
    for r in range(tl_r, min(tl_r + block_size, height)):
        for c in range(tl_c, min(tl_c + block_size, width)):
            output_grid[r][c] = fg_color
            
    return output_grid
```