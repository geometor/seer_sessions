
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 4 0 4 0 4 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 4 0 4 0 4 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The task involves identifying different colored objects within a grid and moving some of them based on the position and shape of the largest object.

1.  **Object Identification**: In both examples, the input grid contains multiple non-background objects (pixels or groups of pixels). One object is significantly larger (in terms of pixel count) than the others.
2.  **Static vs. Mobile Objects**: The largest object remains stationary in the output grid (it acts as a "wall" or "anchor"). The smaller objects ("movers") change their positions.
3.  **Movement Pattern**: The movers shift horizontally towards a specific target column determined by the wall.
4.  **Wall Type & Target Column**:
    *   If the wall is a vertical line (like the green line in train_1), the target column is the column immediately to the left of the wall.
    *   If the wall is a horizontal line (like the red line in train_2), the target column is the horizontal midpoint (center column, rounded down) of the wall.
5.  **Mover Arrangement & Final Placement**:
    *   **Co-linear Movers (train_1)**: If all movers initially lie on the same row, they are treated as a single pattern. This pattern is shifted horizontally so that its rightmost pixel lands in the target column. The original row and relative horizontal spacing are maintained.
    *   **Scattered Movers (train_2)**: If movers are scattered across different rows and columns, they are moved individually to the target column. Their final vertical positions are determined by stacking them vertically within the target column, starting one row below the lowest extent of the wall. The original top-to-bottom order of the movers is preserved, and one empty row is left between each stacked mover.
6.  **Color Preservation**: Movers retain their original colors. The wall retains its original color and position. Background pixels remain background unless replaced by a moved object.

## Facts


```yaml
Input:
  - Grid: 2D array of integer colors (0-9)
  - Background: Color 0 (white)
  - Objects: Connected components of non-background pixels

Identify Components:
  - Find all connected components (pixels of the same non-zero color adjacent horizontally or vertically).
  - Count pixels in each component.

Identify Wall and Movers:
  - Wall: The component with the largest number of pixels. It remains static.
  - Movers: All other components. They change position.

Calculate Wall Properties:
  - Bounding Box: Min/Max row and column indices (Rmin, Rmax, Cmin, Cmax).
  - Width: Cmax - Cmin + 1
  - Height: Rmax - Rmin + 1

Determine Target Column (C_target):
  - If Wall is vertical (Width == 1): C_target = Cmin - 1
  - If Wall is horizontal (Height == 1): C_target = floor((Cmin + Cmax) / 2)
  # Note: Assumes wall is strictly vertical or horizontal based on examples.

Determine Movement Strategy based on Movers' initial positions:
  - Strategy 1 (Co-linear): If all movers share the same initial row index.
  - Strategy 2 (Scattered): If movers occupy different initial rows.

Apply Movement Strategy:
  - Strategy 1 (Co-linear):
    - Find the rightmost column (max_col) occupied by any mover pixel in the shared row.
    - Calculate shift distance: shift = C_target - max_col.
    - Move all mover pixels in that row horizontally by 'shift' columns.
  - Strategy 2 (Scattered):
    - Create a list of movers, storing their original color and top row index.
    - Sort the list by the original top row index (ascending).
    - Determine starting row for stacking: Start_Row = Rmax (of Wall) + 1.
    - Initialize current row: Current_Row = Start_Row.
    - For each mover in the sorted list:
      - Place the mover's pixels in the output grid, translated so their top-left corner (or reference point) is at (Current_Row, C_target). Adjust relative positions if mover is multi-pixel. (Simpler: For single-pixel movers, place at (Current_Row, C_target)).
      - Update current row for the next mover: Current_Row = Current_Row + 2 (to leave one empty row).

Construct Output Grid:
  - Start with a background grid of the same dimensions as the input.
  - Place the Wall pixels at their original positions.
  - Place the Mover pixels at their calculated final positions.

```


## Natural Language Program

1.  Create the output grid, initially filled with the background color (white, 0), having the same dimensions as the input grid.
2.  Find all distinct connected components of non-background colors in the input grid.
3.  Identify the component with the maximum number of pixels; this is the "Wall". Copy the Wall pixels to their original positions in the output grid.
4.  Identify all other components; these are the "Movers". Collect their original pixel coordinates and colors.
5.  Calculate the bounding box (minimum/maximum row and column) of the Wall.
6.  Determine the target column (`C_target`) for the Movers:
    *   If the Wall's width is 1 (vertical line), set `C_target` to the Wall's column minus 1.
    *   If the Wall's height is 1 (horizontal line), set `C_target` to the floor of the average of the Wall's minimum and maximum column indices (its horizontal center).
7.  Check if all Mover components lie entirely on the same row in the input grid.
8.  **If all Movers are on the same row**:
    *   Find the maximum column index occupied by any pixel of any Mover on that row.
    *   Calculate the horizontal shift required: `shift = C_target - maximum_column_index`.
    *   For each pixel belonging to any Mover, add the `shift` to its column index to get its new position. Copy the Mover pixel's color to this new position in the output grid.
9.  **If Movers are on different rows (Scattered)**:
    *   Create a list of Movers, recording the original color and minimum row index for each.
    *   Sort this list based on the minimum row index (top to bottom).
    *   Set the starting row for placement (`Current_Row`) to the Wall's maximum row index plus 1.
    *   Iterate through the sorted list of Movers:
        *   For the current Mover, determine its new top-left position (or single pixel position if it's a single pixel) as (`Current_Row`, `C_target`).
        *   Copy the Mover's pixels (with their original color), translated to this new position, onto the output grid.
        *   Increment `Current_Row` by 2 for the next Mover (placing one empty row between Movers).
10. Return the completed output grid.
```python
import numpy as np
from collections import deque

"""
This program transforms an input grid based on identifying a large 'wall' object and smaller 'mover' objects.

1.  **Identify Objects**: Find all connected components of non-background (non-zero) pixels in the input grid.
2.  **Distinguish Wall and Movers**: The component with the most pixels is designated the 'Wall'. All other components are 'Movers'.
3.  **Determine Target Column**: Calculate a target column (`C_target`) based on the Wall's shape:
    *   If the Wall is a vertical line (width 1), `C_target` is the column to the left of the Wall (`Wall_column - 1`).
    *   If the Wall is a horizontal line (height 1), `C_target` is the horizontal center column of the Wall (`floor((Wall_min_col + Wall_max_col) / 2)`).
4.  **Analyze Mover Positions**: Check if all Mover components are initially located on the same row.
5.  **Apply Movement Strategy**:
    *   **Co-linear Movers (Same Row)**: Find the rightmost column occupied by any Mover pixel on their shared row. Calculate a horizontal shift to move this rightmost pixel to the `C_target` column. Apply this shift to all Mover pixels.
    *   **Scattered Movers (Different Rows)**: Sort the Movers based on their topmost row index (ascending). Place them vertically stacked in the `C_target` column, starting one row below the Wall's bottom edge. Maintain the original top-to-bottom order and leave one empty row between consecutive Movers.
6.  **Construct Output**: Create an output grid initialized with the background color. Place the Wall at its original position and the Movers at their calculated new positions.
"""

def find_connected_components(grid):
    """Finds all connected components of non-background pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                component = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r, min_c, max_c = r, r, c, c

                while q:
                    row, col = q.popleft()
                    component.append((row, col, color))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                components.append({
                    'pixels': component, 
                    'color': color, 
                    'size': len(component),
                    'bounds': (min_r, max_r, min_c, max_c)
                })
    return components

def transform(input_grid_list):
    """
    Transforms the input grid according to the rules derived from examples.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape
    
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)

    # 1. Find all connected components
    components = find_connected_components(input_grid)

    if not components:
        return output_grid.tolist() # Return empty grid if no objects

    # 2. Identify Wall and Movers
    components.sort(key=lambda x: x['size'], reverse=True)
    wall = components[0]
    movers = components[1:]

    # 3. Place Wall in the output grid
    for r, c, color in wall['pixels']:
        output_grid[r, c] = color

    if not movers:
        return output_grid.tolist() # Return grid with only wall if no movers

    # 4. Calculate Wall Properties and Target Column
    wall_min_r, wall_max_r, wall_min_c, wall_max_c = wall['bounds']
    wall_height = wall_max_r - wall_min_r + 1
    wall_width = wall_max_c - wall_min_c + 1
    
    c_target = -1 # Initialize target column
    if wall_width == 1: # Vertical wall
        c_target = wall_min_c - 1
    elif wall_height == 1: # Horizontal wall
        c_target = (wall_min_c + wall_max_c) // 2 # Floor division for center
    else:
        # Fallback or error case if wall is not a line?
        # Based on examples, assume it's always a line.
        # If not a line, maybe use centroid or another rule?
        # For now, let's stick to the observed patterns.
        # If neither vertical nor horizontal, maybe default to one rule?
        # Let's default to horizontal rule if ambiguous based on examples seen.
         c_target = (wall_min_c + wall_max_c) // 2


    # Ensure target column is valid
    if c_target < 0:
        # Handle cases where target might be off-grid left? 
        # Or is this expected? Example 1 target is valid.
        pass # Assume valid for now based on examples.

    # 5. Check if all Movers are on the same row
    first_mover_row = movers[0]['bounds'][0] # min_r of the first mover
    all_same_row = True
    shared_row = -1
    if movers:
       shared_row = movers[0]['bounds'][0] # Get min_r of first mover
       for mover in movers:
           # Check if all pixels of the mover are on the same row and if that row is 'shared_row'
           mover_min_r, mover_max_r, _, _ = mover['bounds']
           if mover_min_r != shared_row or mover_max_r != shared_row:
               all_same_row = False
               break
    else:
        all_same_row = False # No movers means not "all on the same row"

    # 6. Apply Movement Strategy
    if all_same_row:
        # Strategy 1: Co-linear Movers
        max_mover_col = -1
        all_mover_pixels = []
        for mover in movers:
            all_mover_pixels.extend(mover['pixels'])
            for _, c, _ in mover['pixels']:
                 max_mover_col = max(max_mover_col, c)
        
        if max_mover_col != -1 and c_target != -1 :
             shift = c_target - max_mover_col
             for r, c, color in all_mover_pixels:
                 new_c = c + shift
                 # Place pixel if within bounds
                 if 0 <= r < rows and 0 <= new_c < cols:
                     output_grid[r, new_c] = color

    else:
        # Strategy 2: Scattered Movers
        # Sort movers by their top row index (min_r)
        movers.sort(key=lambda x: x['bounds'][0]) 

        current_row = wall_max_r + 1 # Start placing one row below the wall

        for mover in movers:
            mover_min_r, _, mover_min_c, _ = mover['bounds']
            color = mover['color']
            
            # Calculate shift needed to move the mover's top-left corner 
            # (defined by min_r, min_c) to (current_row, c_target)
            dr = current_row - mover_min_r
            dc = c_target - mover_min_c

            # Apply shift to all pixels of the current mover
            for r, c, _ in mover['pixels']:
                 new_r, new_c = r + dr, c + dc
                 # Place pixel if within bounds
                 if 0 <= new_r < rows and 0 <= new_c < cols:
                     output_grid[new_r, new_c] = color
            
            # Update current_row for the next mover, adding 1 for the mover height 
            # (assuming 1px height based on example 2) + 1 for spacing = +2
            # If movers can have >1 height, need to use actual mover height.
            mover_height = mover['bounds'][1] - mover['bounds'][0] + 1
            current_row += mover_height + 1 # Add mover height + 1 row gap

    return output_grid.tolist()
```
