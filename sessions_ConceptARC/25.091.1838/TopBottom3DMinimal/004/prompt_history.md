
## train_1

**input:**
```
2 2 2 2 2 0 0 0
2 0 3 3 2 3 3 0
2 0 3 3 2 3 3 0
2 0 3 3 2 3 3 0
2 2 2 2 2 3 3 0
0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 0 0 0
2 0 3 3 3 3 3 0
2 0 3 3 3 3 3 0
2 0 3 3 3 3 3 0
2 2 3 3 3 3 3 0
0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 6 6 6 6
0 0 7 7 7 7 7 6
0 0 7 0 6 6 7 6
0 0 7 7 7 7 7 6
0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 6 6 6
0 0 7 7 6 6 6 6
0 0 7 0 6 6 6 6
0 0 7 7 6 6 6 6
0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

## Perception

1.  **Grid Structure:** Both examples operate on 8x8 grids.
2.  **Colors:** Each example involves three colors: a background color (white/0) and two other distinct colors.
    *   Example 1: white(0), red(2), green(3)
    *   Example 2: white(0), magenta(6), orange(7)
3.  **Transformation Focus:** The core transformation involves changing the color of *some* pixels from one non-background color to the other non-background color. The background color remains unchanged.
4.  **Stability:** One of the two non-background colors appears "stable" or "dominant" – its pixels never change color. The other non-background color is "recessive" – some of its pixels may change into the dominant color.
5.  **Mechanism:** The change occurs at the interface between the two non-background colors. Specifically, a pixel of the recessive color changes to the dominant color if it is adjacent (including diagonally) to *any* pixel of the dominant color in the input grid.
6.  **Determining Dominance:** Comparing the two examples, the dominant color appears to be the one that has a higher count of pixels in the input grid.
    *   Example 1: Input has 14 red(2) pixels and 21 green(3) pixels. Green(3) is dominant. Red pixels adjacent to green pixels change to green.
    *   Example 2: Input has 18 orange(7) pixels and 20 magenta(6) pixels. Magenta(6) is dominant. Orange pixels adjacent to magenta pixels change to magenta.
7.  **Simultaneity:** The transformation seems to happen based solely on the state of the input grid. Changes don't cascade within the transformation step; all pixels are evaluated based on their input neighbors.

## Facts


```yaml
task_type: pixel_color_change
components:
  - type: grid
    properties:
      - background_color: always color 0 (white)
      - active_colors: exactly two non-background colors per task example
  - type: pixel
    properties:
      - color: integer 0-9
      - position: (row, column) coordinates
      - neighbors: set of 8 adjacent pixels (orthogonal and diagonal)

relationships:
  - type: color_counts
    description: The total number of pixels for each of the two active colors in the input grid.
  - type: color_dominance
    based_on: color_counts
    rule: The color with the strictly greater pixel count is the 'dominant' color (CD). The other is the 'recessive' color (CR).
    notes: Assumes no ties in counts based on examples. If counts are equal, behavior is undefined by these examples.
  - type: adjacency_interaction
    between: recessive_pixel (pixel with color CR)
    and: dominant_neighbor (neighboring pixel with color CD)
    condition: A recessive_pixel has at least one neighbor (orthogonal or diagonal) that is a dominant_neighbor in the input grid.

actions:
  - type: color_conversion
    target: recessive_pixel
    condition: adjacency_interaction is true for the pixel in the input grid.
    result: The target pixel's color in the output grid becomes the dominant color (CD).
  - type: color_preservation
    target: all other pixels (background, dominant color pixels, recessive pixels not meeting the adjacency condition)
    result: The target pixel's color in the output grid remains the same as in the input grid.
```


## Natural Language Program

1.  **Identify Colors:** Scan the input grid to find the background color (which is always white/0) and the two distinct non-background colors present. Let these be C1 and C2.
2.  **Count Colors:** Count the total number of pixels of color C1 and the total number of pixels of color C2 in the input grid.
3.  **Determine Dominant Color:** Compare the counts. Identify the color with the strictly greater count as the Dominant Color (CD) and the color with the lesser count as the Recessive Color (CR).
4.  **Initialize Output Grid:** Create a new grid of the same dimensions as the input grid, initially identical to the input grid.
5.  **Iterate and Update:** For each pixel at position (row, column) in the input grid:
    a.  Check if the pixel's color is the Recessive Color (CR).
    b.  If it is CR, examine all its 8 neighbors (orthogonal and diagonal) *in the input grid*.
    c.  Check if any of these neighbors have the Dominant Color (CD).
    d.  If at least one neighbor has the Dominant Color (CD), change the color of the pixel at (row, column) *in the output grid* to the Dominant Color (CD).
    e.  If the pixel's color is not CR, or if it is CR but has no neighbors with color CD, its color in the output grid remains unchanged (it was already copied in step 4).
6.  **Final Output:** The completed output grid is the result of the transformation.
```python
import numpy as np

"""
Identify the two non-background (non-zero) colors in the input grid.
Count the pixels of each of these two colors.
Determine the 'dominant' color (CD) as the one with the strictly greater count, 
and the 'recessive' color (CR) as the one with the lesser count.
Create an output grid initialized as a copy of the input grid.
Iterate through each pixel of the input grid. 
If a pixel has the recessive color (CR) and has at least one neighbor 
(orthogonal or diagonal) with the dominant color (CD) in the input grid, 
change the color of that corresponding pixel in the output grid to the dominant color (CD).
Otherwise, the pixel retains its original color in the output grid.
Return the modified output grid.
"""

def get_neighbors(grid, r, c):
    """Gets the coordinates of the 8 neighbors of a cell."""
    height, width = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def has_dominant_neighbor(grid, r, c, dominant_color):
    """Checks if any neighbor of (r, c) has the dominant color."""
    neighbor_coords = get_neighbors(grid, r, c)
    for nr, nc in neighbor_coords:
        if grid[nr, nc] == dominant_color:
            return True
    return False

def transform(input_grid):
    """
    Applies the color transformation based on neighbor dominance.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find unique non-zero colors
    unique_colors = np.unique(input_grid)
    active_colors = unique_colors[unique_colors != 0]

    # Handle cases with less than two active colors (though not in examples)
    if len(active_colors) < 2:
        return output_grid # No transformation possible/needed

    color1 = active_colors[0]
    color2 = active_colors[1]

    # Count occurrences of each active color
    count1 = np.count_nonzero(input_grid == color1)
    count2 = np.count_nonzero(input_grid == color2)

    # Determine dominant and recessive colors
    # If counts are equal, no transformation occurs based on the rule derived
    if count1 == count2:
        return output_grid 
        
    if count1 > count2:
        dominant_color = color1
        recessive_color = color2
    else:
        dominant_color = color2
        recessive_color = color1

    # Iterate through each cell in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell has the recessive color
            if input_grid[r, c] == recessive_color:
                # Check if any neighbor has the dominant color
                if has_dominant_neighbor(input_grid, r, c, dominant_color):
                    # If yes, change the corresponding cell in the output grid
                    output_grid[r, c] = dominant_color
            # Otherwise, the output_grid cell retains its copied value

    return output_grid.tolist() # Return as list of lists
```
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
