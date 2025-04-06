
## train_1

**input:**
```
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
4 4 4 8 8 8 8 8
4 4 4 8 8 8 8 8
4 4 4 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8
8 8 8 8 8 8
8 8 8 8 9 8
8 8 8 8 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```


**output:**
```
8 8 8 8 9 9
8 8 8 8 9 9
8 8 8 8 9 9
8 8 8 8 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```


## train_3

**input:**
```
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 6 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
```


**output:**
```
6 6 6 8 8 8 8 8
6 6 6 8 8 8 8 8
6 6 6 8 8 8 8 8
6 6 6 8 8 8 8 8
6 6 6 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
```


## train_4

**input:**
```
8 8 6 8
8 8 8 8
8 8 8 8
8 8 8 8
```


**output:**
```
8 8 6 6
8 8 8 8
8 8 8 8
8 8 8 8
```

## Perception of Task Elements

1.  **Input/Output:** Both inputs and outputs are 2D grids of numerical digits.
2.  **Grid Cells:** Each cell contains a single digit, likely representing a color or state.
3.  **Background Color:** The digit '8' appears to be the default or background color, filling most of the grid in the inputs.
4.  **Foreground Color:** In each input grid, there is exactly one cell with a color different from '8' (e.g., '4', '9', '6'). This seems to be the significant 'foreground' color/pixel.
5.  **Transformation:** The core transformation involves the single foreground pixel. Its presence in the input determines the pattern in the output.
6.  **Output Pattern:** The output grids consist of the background color ('8') and a solid 3x3 square filled with the foreground color from the input.
7.  **Pattern Placement:** The position of the 3x3 square in the output grid is related to the position of the single foreground pixel in the input grid. Specifically, the output square occupies the 3x3 block (aligned to a conceptual 3x3 grid tiling) that contains the original foreground pixel.

## YAML Facts Documentation


```yaml
task_description: Identify a unique non-background pixel in the input grid and fill the corresponding 3x3 block in the output grid with that pixel's color, setting the rest to the background color.

grid_properties:
  cell_content: single digits (representing colors)
  background_color: '8' # Based on consistent observation across examples
  foreground_color: Any digit other than the background color. Only one such digit exists per input grid.

objects:
  - name: input_grid
    type: 2D array of digits
  - name: output_grid
    type: 2D array of digits (same dimensions as input)
  - name: background_pixel
    properties:
      color: '8'
  - name: foreground_pixel
    properties:
      color: C (variable, e.g., '4', '9', '6')
      location: (r, c) - row and column index in the input grid
  - name: output_block
    properties:
      size: 3x3
      color: C (same as foreground_pixel)
      location: Top-left corner (TL_r, TL_c) in the output grid

relationships:
  - type: identity
    description: Output grid has the same dimensions as the input grid.
  - type: determination
    description: The color and location (r, c) of the single foreground_pixel in the input_grid determine the output_grid content.
  - type: calculation
    description: The top-left corner (TL_r, TL_c) of the output_block is derived from the foreground_pixel's location (r, c).
    formula: TL_r = (r // 3) * 3, TL_c = (c // 3) * 3
  - type: construction
    description: The output_grid is constructed by filling the output_block area with the foreground color C and all other cells with the background_color.

actions:
  - name: find_foreground_pixel
    inputs: input_grid, background_color
    outputs: foreground_color C, location (r, c)
    description: Scan the input grid to locate the single pixel whose color is not the background color.
  - name: calculate_block_location
    inputs: foreground_pixel location (r, c)
    outputs: output_block top-left location (TL_r, TL_c)
    description: Apply integer division and multiplication by 3 to find the containing 3x3 block's origin.
  - name: generate_output_grid
    inputs: grid_dimensions, output_block (location and color), background_color
    outputs: output_grid
    description: Create a grid, fill the 3x3 output_block area with its specified color, and fill the rest with the background color.

```


## Natural Language Program

1.  Identify the background color, which is '8'.
2.  Scan the input grid row by row, then column by column, to find the coordinates `(r, c)` and the color `C` of the single cell that does not contain the background color '8'.
3.  Determine the top-left coordinates `(TL_r, TL_c)` of the 3x3 grid block that contains the cell `(r, c)`. Calculate these coordinates using integer division: `TL_r = (r // 3) * 3` and `TL_c = (c // 3) * 3`.
4.  Create a new output grid with the same height and width as the input grid.
5.  Fill every cell `(i, j)` in the output grid according to the following rule:
    *   If the cell's row `i` is between `TL_r` (inclusive) and `TL_r + 3` (exclusive), AND the cell's column `j` is between `TL_c` (inclusive) and `TL_c + 3` (exclusive), set the cell's color to `C`.
    *   Otherwise, set the cell's color to the background color '8'.
6.  Return the generated output grid.
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
