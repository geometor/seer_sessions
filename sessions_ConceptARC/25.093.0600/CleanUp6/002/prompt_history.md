
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 3
3 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 0 0 0 0
0 1 0 0 3 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 1 0 0 3 0 0 0 0 3
0 0 0 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 1
3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 6 8 0 0 0 8 0 0 0 0 0 6 8 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 8 6 6 6 0 0 0 0 0 6 6 6 6 0 0
0 0 6 8 6 0 0 0 0 8 0 0 6 6 6 0 0
0 0 6 6 0 0 8 0 0 0 8 0 0 6 6 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 6 6 6 6 0 0 0 0 0 6 6 6 6 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task operates on 2D grids containing numerical values (colors). The background is typically color 0.
    *   Each input grid contains, besides the background color 0, two other distinct non-zero colors.
    *   One non-zero color appears significantly more frequently than the other in the input grid. This suggests identifying a 'dominant' non-zero color based on count.
    *   The other non-zero color(s) act as 'minority' colors.
    *   The transformation rule involves filtering the grid based on color dominance and spatial relationships (connectivity).
    *   Specifically, all minority colors are removed (replaced by 0).
    *   The dominant color is kept only if a cell containing it is orthogonally adjacent (shares a side - up, down, left, or right) to at least one other cell also containing the dominant color. Isolated cells of the dominant color are also removed (replaced by 0).

*   **Facts:**
    
```yaml
    task_elements:
      - item: grid
        properties:
          - type: 2D array of integers (colors)
          - background_color: 0
          - contains_multiple_non_zero_colors
      - item: cell
        properties:
          - location: (row, column)
          - value: integer (color)
      - item: color
        properties:
          - value: integer
          - frequency: count in the grid
          - role: [dominant, minority, background]
      - item: dominant_color
        derivation: the non-zero color with the highest frequency in the input grid
      - item: minority_color
        derivation: any non-zero color that is not the dominant color
      - item: orthogonal_adjacency
        definition: Two cells share an edge (not just a corner).
      - item: isolated_cell
        definition: A cell containing the dominant color with no orthogonally adjacent neighbors also containing the dominant color.
    
    transformation:
      - action: identify_colors
        inputs: input_grid
        outputs: set_of_non_zero_colors
      - action: count_frequencies
        inputs: input_grid, set_of_non_zero_colors
        outputs: color_frequencies
      - action: determine_dominant_color
        inputs: color_frequencies
        outputs: dominant_color
      - action: initialize_output_grid
        properties: same dimensions as input_grid, filled with background_color (0)
      - action: filter_grid
        steps:
          - iterate through each cell (r, c) of the input_grid
          - get current_color = input_grid[r, c]
          - if current_color == dominant_color:
            - check orthogonal neighbors (r-1, c), (r+1, c), (r, c-1), (r, c+1) within grid bounds
            - if any orthogonal neighbor also contains dominant_color:
              - set output_grid[r, c] = dominant_color
          # Implicitly, all other cells (minority colors, isolated dominant colors, background) remain 0 in the output grid
    ```


*   **Natural Language Program:**
    1.  Analyze the input grid to identify all unique non-zero colors present.
    2.  Count the frequency of occurrence for each unique non-zero color.
    3.  Determine the 'dominant' color, which is the non-zero color with the highest frequency. All other non-zero colors are 'minority' colors.
    4.  Create a new output grid of the same dimensions as the input grid, initially filled entirely with the background color (0).
    5.  Iterate through each cell of the input grid at location (row, column).
    6.  Let the color in the current input cell be `current_color`.
    7.  If `current_color` is the identified dominant color:
        a.  Examine its orthogonal neighbors (up, down, left, right).
        b.  Check if at least one of these orthogonal neighbors in the *input* grid also contains the dominant color.
        c.  If such a neighbor exists (i.e., the current cell is not isolated), set the cell at (row, column) in the *output* grid to the dominant color.
    8.  If the `current_color` is not the dominant color (i.e., it's a minority color or the background color 0), or if it is the dominant color but is isolated (no orthogonal neighbors with the dominant color), the corresponding cell in the output grid retains its initial background color (0).
    9.  Return the completed output grid.
```python
import numpy as np
from collections import Counter

def _find_dominant_color(grid_np):
    """Finds the non-zero color with the highest frequency."""
    # Flatten the grid and filter out the background color (0)
    non_zero_colors = grid_np[grid_np != 0]

    # Handle cases with no non-zero colors
    if non_zero_colors.size == 0:
        return None

    # Count frequencies
    color_counts = Counter(non_zero_colors)

    # Find the color with the maximum count
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def _has_dominant_neighbor(grid_np, r, c, dominant_color):
    """Checks if a cell has an orthogonally adjacent neighbor with the dominant color."""
    rows, cols = grid_np.shape
    # Define orthogonal neighbor offsets
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    for nr, nc in neighbors:
        # Check if neighbor is within grid bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check if the neighbor has the dominant color
            if grid_np[nr, nc] == dominant_color:
                return True
    return False

def transform(input_grid):
    """
    Filters a grid based on color dominance and connectivity.

    1. Identifies the most frequent non-zero color (dominant color).
    2. Removes all other non-zero colors (minority colors).
    3. Removes dominant color cells that do not have at least one
       orthogonally adjacent neighbor also containing the dominant color.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output_grid with zeros (background color)
    output_grid_np = np.zeros_like(input_np)

    # Find the dominant color
    dominant_color = _find_dominant_color(input_np)

    # If there's no dominant color (e.g., all zeros input), return the zero grid
    if dominant_color is None:
        return output_grid_np.tolist() # Convert back to list of lists

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            current_color = input_np[r, c]

            # Check if the current cell contains the dominant color
            if current_color == dominant_color:
                # Check if this cell has at least one orthogonal neighbor with the dominant color
                if _has_dominant_neighbor(input_np, r, c, dominant_color):
                    # If it has a dominant neighbor, keep the dominant color in the output grid
                    output_grid_np[r, c] = dominant_color
            # Cells with minority colors or isolated dominant colors remain 0 (background)

    # Convert the result back to a list of lists before returning
    return output_grid_np.tolist()
```
