
## train_1

**input:**
```
3 3 3 3 3 4
4 3 3 3 3 3
3 3 3 4 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 4 3 3
```


**output:**
```
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
```


## train_2

**input:**
```
6 6 6 6 8 6
8 6 6 3 6 6
6 6 6 6 6 6
6 6 8 6 3 6
3 6 6 6 6 6
6 6 6 6 6 6
```


**output:**
```
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
```


## train_3

**input:**
```
0 5 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 5 0
0 2 2 2 2 2 2 2 2 0
5 2 2 2 2 2 2 2 2 0
0 2 2 5 2 2 5 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 5 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0
```

**Perception of the Elements:**

1.  **Input/Output Grids:** Both input and output are grids of pixels with colors represented by integers 0-9.
2.  **Dominant Color:** In each example, there is a color that occupies the majority of the pixels in the input grid, or within a specific region of it.
3.  **Minority Colors:** There are other colors present in the input grid, occupying fewer pixels than the dominant color.
4.  **Transformation:** The transformation simplifies the input grid by replacing the minority colors. The replacement rule depends on the grid structure.
5.  **Grid Structure (Border vs. No Border):**
    *   Example `train_3` shows a distinct, uniform border (color white - 0). The transformation preserves this border and fills the *interior* region with the dominant color found *within* that interior (color red - 2). The minority color (gray - 5) inside the border is replaced by red. The minority color (gray - 5) *on* the border is replaced by the border color (white - 0), effectively becoming part of the border.
    *   Examples `train_1` and `train_2` do not have a uniform border. In these cases, the entire grid is treated as a single region. All pixels are replaced by the single most frequent color found across the entire input grid (green - 3 in `train_1`, magenta - 6 in `train_2`).

**YAML Facts:**


```yaml
task_description: Replace minority colors with the dominant color, potentially respecting border structures.

elements:
  - element: grid
    description: A 2D array of pixels representing colors.
  - element: pixel
    description: A single cell in the grid with a color value (0-9).
  - element: color
    description: An integer value 0-9 associated with each pixel.
  - element: region
    description: A contiguous area within the grid. Can be the entire grid or sub-parts like a border or the interior enclosed by a border.
  - element: dominant_color
    description: The color that appears most frequently within a specific region (either the whole grid or the interior).
  - element: minority_color
    description: Colors that are not the dominant color within a region.
  - element: border
    description: The outermost layer of pixels (row 0, last row, col 0, last col). Identified as a structural element if all perimeter pixels share the same color.

relationships:
  - type: frequency
    description: Colors have frequencies (counts) within a region.
  - type: spatial
    description: Pixels have positions (row, column) and neighbors. A border encloses an interior region.

actions:
  - action: identify_border
    description: Check if all pixels on the grid perimeter (row 0, last row, col 0, last col) have the same color.
  - action: identify_dominant_color
    description: Count pixel colors within a specified region (either the whole grid or the interior excluding the border) and find the color with the highest count.
  - action: replace_pixels
    description: Change the color of pixels based on the identified structure and dominant color.
    conditions:
      - if: uniform border exists
        effect: Preserve border pixels, replace all interior pixels with the dominant color of the interior.
      - if: no uniform border
        effect: Replace all pixels in the grid with the overall dominant color of the whole grid.

```


**Natural Language Program:**

1.  Receive the input grid.
2.  Check if the grid has a uniform border: Examine all pixels on the perimeter (first row, last row, first column, last column). If they all share the same single color, a uniform border exists.
3.  **If a uniform border exists:**
    a.  Identify the border color.
    b.  Define the interior region as all pixels *not* part of the border.
    c.  Count the frequency of each color within the interior region.
    d.  Identify the `dominant_interior_color` (the color with the highest frequency in the interior). If there's a tie, a consistent tie-breaking rule might be needed (e.g., lowest color index), but the examples don't necessitate this yet.
    e.  Create the output grid with the same dimensions as the input.
    f.  Fill the border pixels in the output grid with the `border_color`.
    g.  Fill all interior pixels in the output grid with the `dominant_interior_color`.
4.  **If no uniform border exists:**
    a.  Count the frequency of each color across the *entire* input grid.
    b.  Identify the `overall_dominant_color` (the color with the highest frequency). Handle ties if necessary.
    c.  Create the output grid with the same dimensions as the input.
    d.  Fill *all* pixels in the output grid with the `overall_dominant_color`.
5.  Return the resulting output grid.
```python
"""
Checks if the input grid has a uniform border (all perimeter pixels are the same color).
If a uniform border exists:
  - The border pixels in the output grid retain the border color.
  - All interior pixels (not on the border) in the output grid are filled with the most frequent color found within the interior region of the input grid.
If no uniform border exists:
  - The entire output grid is filled with the single most frequent color found across the entire input grid.
"""

import numpy as np
from collections import Counter

def find_dominant_color(pixels: np.ndarray) -> int:
    """
    Finds the most frequent color in a flattened array of pixels.
    Handles ties by returning the smallest color index.
    """
    if pixels.size == 0:
        # Handle empty region case if necessary, though unlikely based on examples
        return 0 # Default to white or raise error? Defaulting for now.
    
    counts = Counter(pixels.flatten())
    # Find the maximum count
    max_count = 0
    for color, count in counts.items():
        if count > max_count:
            max_count = count
            
    # Get all colors with the maximum count
    dominant_colors = [color for color, count in counts.items() if count == max_count]
    
    # Return the smallest color index in case of a tie
    return min(dominant_colors)

def has_uniform_border(grid: np.ndarray) -> tuple[bool, int | None]:
    """
    Checks if the grid has a uniform border.
    Returns (True, border_color) if uniform, otherwise (False, None).
    Handles 1xN and Nx1 grids.
    """
    height, width = grid.shape
    
    # Handle trivial cases (1x1 grid has a 'uniform' border)
    if height == 1 and width == 1:
        return True, grid[0, 0]
        
    border_color = grid[0, 0]
    
    # Check top and bottom rows
    if height > 0:
        for c in range(width):
            if grid[0, c] != border_color:
                return False, None
            if height > 1 and grid[height - 1, c] != border_color:
                 return False, None
                 
    # Check left and right columns (excluding corners already checked)
    if width > 0:
        for r in range(1, height - 1): # Exclude corners
            if grid[r, 0] != border_color:
                 return False, None
            if width > 1 and grid[r, width - 1] != border_color:
                return False, None

    return True, border_color

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on border detection and dominant color filling.
    """
    # Convert input list of lists to a NumPy array for easier slicing and operations
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    
    # Initialize output_grid as a NumPy array of the same shape
    output_grid_np = np.zeros_like(grid_np)

    # Check for a uniform border
    is_uniform, border_color = has_uniform_border(grid_np)

    if is_uniform and border_color is not None:
        # Case 1: Uniform border exists
        
        # Define the interior region (handle grids smaller than 3x3)
        if height > 2 and width > 2:
            interior_region = grid_np[1:-1, 1:-1]
        elif height <= 2 or width <= 2 : # No interior if height/width is 1 or 2
             interior_region = np.array([]) # empty interior
        # else: # This logic seems redundant given the check for <=2 above. Simplified.
        #     interior_region = np.array([]) # Should not happen if is_uniform is True unless 1xN or Nx1 with H,W > 2? No, handled above.

        # Find the dominant color in the interior
        # If interior is empty (e.g., 2xN grid), dominant color doesn't matter as it won't be used.
        # Default to border color if interior is empty to avoid errors, though fill logic handles this.
        dominant_interior_color = find_dominant_color(interior_region) if interior_region.size > 0 else border_color

        # Create the output grid: Fill interior first
        output_grid_np.fill(dominant_interior_color)
        
        # Apply the border color to the perimeter
        if height > 0:
            output_grid_np[0, :] = border_color  # Top row
            if height > 1:
                output_grid_np[height - 1, :] = border_color # Bottom row
        if width > 0:
             output_grid_np[:, 0] = border_color  # Left column
             if width > 1:
                output_grid_np[:, width - 1] = border_color # Right column
                
    else:
        # Case 2: No uniform border
        
        # Find the dominant color across the entire grid
        overall_dominant_color = find_dominant_color(grid_np)
        
        # Fill the entire output grid with the overall dominant color
        output_grid_np.fill(overall_dominant_color)

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()
    
    return output_grid

```
