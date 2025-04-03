
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 0 2 2 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 0 2 2 2 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0
0 3 4 4 4 4 3 0
0 3 4 4 4 4 3 0
0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0
0 3 3 3 3 3 3 0
0 3 3 3 3 3 3 0
0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 6 0 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
```


**output:**
```
0 0 0 6 0 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
```

## Perception of Task Elements

The task involves transforming a 2D grid of numbers (representing colors). The core operation appears to be a "fill" or "paint bucket" like function, constrained by specific boundaries within the grid.

1.  **Grid Structure:** Both input and output are 2D grids of the same dimensions, containing single digits (0-9). '0' consistently represents the background color.
2.  **Colored Regions:** Non-zero numbers form distinct regions or shapes within the grid.
3.  **Boundary/Frame:** In each example, there's a specific non-zero color that acts as a frame or boundary (`C_frame`). This frame partially or fully encloses regions of other non-zero colors.
4.  **Enclosed Area:** The area inside the `C_frame` boundary contains other non-zero colors (`C_inner`).
5.  **External Area:** Areas outside the `C_frame` boundary, including the background (0) and potentially other non-zero colored regions not enclosed by `C_frame`, are considered external.
6.  **Transformation:** The transformation identifies the `C_frame` color and the region it encloses. All cells within this enclosed region that originally had a `C_inner` color are changed to the `C_frame` color in the output. The `C_frame` cells themselves, the background (0), and any non-zero cells in the external area remain unchanged.

## Facts


```yaml
---
task_elements:
  - name: Grid
    type: Container
    properties:
      - dimensions: [rows, columns] (constant between input/output)
      - elements: Cells

  - name: Cell
    type: Element
    properties:
      - position: [row, column]
      - color: integer (0-9)
      - state: (derived) external or internal relative to the frame

  - name: Background
    type: Region
    properties:
      - color: 0
      - state: external

  - name: Frame Region
    type: Region
    properties:
      - color: C_frame (specific non-zero integer, e.g., 1, 3, 7 in examples)
      - connectivity: Forms a boundary separating internal and external areas
      - state: external (in the sense that its color is preserved)

  - name: Enclosed Region
    type: Region
    properties:
      - color: C_inner (one or more non-zero integers different from C_frame)
      - location: Geometrically inside the Frame Region
      - state: internal

  - name: External Non-Frame Region
    type: Region
    properties:
      - color: Non-zero integer (potentially same as C_inner, but located outside)
      - location: Geometrically outside the Frame Region
      - state: external

relationships:
  - type: Adjacency
    between: [Cell, Cell]
    properties: [4-connectivity (up, down, left, right)]
  - type: Enclosure
    subject: Frame Region
    object: Enclosed Region
  - type: Reachability
    description: Cells reachable from the Background without crossing the Frame Region color are external.

actions:
  - name: Identify Frame Color (C_frame)
    input: Input Grid
    output: C_frame color value
    method: Find the unique non-zero color C such that treating C as a wall isolates other non-zero colors from the background during a flood fill starting from the background.
  - name: Determine Reachability (Flood Fill)
    input: [Input Grid, C_frame]
    output: Set of coordinates for "external" cells
    method: Perform a flood fill starting from all background (0) cells. The fill can propagate to adjacent cells unless the target cell has the C_frame color. Mark all reached cells as external.
  - name: Generate Output Grid
    input: [Input Grid, C_frame, External Cells Set]
    output: Output Grid
    method: Iterate through input grid cells. If a cell's color is C_frame, copy C_frame to output. If a cell is marked external, copy its input color to output. If a cell is not external and not C_frame, set its output color to C_frame.
---
```


## Natural Language Program

1.  **Identify** the unique non-zero color (`C_frame`) in the input grid that acts as a boundary, such that if cells of this color were treated as impassable walls, a flood fill starting from the background (color 0) would fail to reach at least one other non-zero colored cell.
2.  **Perform** a flood fill starting from all background cells (color 0) in the input grid. This fill can move to adjacent cells (up, down, left, right) but *cannot* enter cells whose color is `C_frame`.
3.  **Mark** all cells reached by this flood fill as "external". All other cells (including the `C_frame` cells themselves and any unreached non-zero cells) are considered "internal" in terms of reachability, though `C_frame` cells are treated specially.
4.  **Create** a new output grid with the same dimensions as the input grid.
5.  **Iterate** through each cell `(r, c)` of the input grid:
    a.  If the input cell `(r, c)` has the color `C_frame`, set the output cell `(r, c)` to `C_frame`.
    b.  Else if the input cell `(r, c)` is marked "external" (from step 3), copy the input cell's color to the output cell `(r, c)`.
    c.  Else (the cell is not `C_frame` and was not marked "external"), set the output cell `(r, c)` to the `C_frame` color.
6.  **Return** the completed output grid.
```python
import numpy as np
from collections import deque

"""
Identify the unique non-zero color (C_frame) that acts as a boundary separating the background (0) from at least one other non-zero color region.
Perform a flood fill starting from all background cells (0), treating C_frame cells as impassable walls. Mark all reachable cells as 'external'.
Create the output grid:
- Cells with color C_frame remain C_frame.
- Cells marked 'external' retain their original color.
- All other cells (internal, non-C_frame cells) are changed to C_frame.
"""

def _flood_fill(grid, start_coords, walls_color):
    """
    Performs a flood fill (BFS) starting from start_coords.
    Returns a set of reachable coordinates, avoiding cells with walls_color.
    """
    rows, cols = grid.shape
    q = deque(start_coords)
    reachable = set(start_coords)
    
    while q:
        r, c = q.popleft()
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                # Check if neighbor is reachable: not already visited and not a wall
                if neighbor_coord not in reachable and grid[nr, nc] != walls_color:
                    reachable.add(neighbor_coord)
                    q.append(neighbor_coord)
                    
    return reachable

def _find_frame_color(grid):
    """
    Identifies the frame color C_frame.
    C_frame is the non-zero color that partitions the grid such that
    some non-zero cells are not reachable from the background (0)
    when C_frame cells are treated as walls.
    """
    rows, cols = grid.shape
    non_zero_colors = np.unique(grid[grid != 0])
    
    if len(non_zero_colors) < 2:
        # Not enough distinct colors to form a frame and an inside
        return None 

    background_coords = list(zip(*np.where(grid == 0)))
    all_non_zero_coords = list(zip(*np.where(grid != 0)))

    for potential_frame_color in non_zero_colors:
        # Perform flood fill from background, treating potential_frame_color as walls
        reachable_from_bg = _flood_fill(grid, background_coords, potential_frame_color)
        
        # Check if *any* non-zero cell (that isn't the potential frame color) is *not* reachable
        unreachable_found = False
        for r_nz, c_nz in all_non_zero_coords:
            if grid[r_nz, c_nz] != potential_frame_color:
                if (r_nz, c_nz) not in reachable_from_bg:
                    unreachable_found = True
                    break # Found an unreachable internal cell for this potential frame color
        
        if unreachable_found:
            return potential_frame_color # This is the frame color

    # Should ideally find a frame color based on problem constraints
    # If not, maybe return the most frequent non-zero, or handle error
    # Based on examples, a frame color always exists if there are >= 2 non-zero colors.
    print("Warning: Could not definitively identify a frame color.")
    return None # Or raise an error


def transform(input_grid):
    """
    Transforms the input grid by filling the area enclosed by a specific frame color
    with that frame color.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = np.copy(input_grid_np)

    # 1. Identify the frame color (C_frame)
    frame_color = _find_frame_color(input_grid_np)
    
    # Handle cases where no clear frame is identified (e.g., single color, only background)
    if frame_color is None:
         # If only one non-zero color exists or just background, no transformation needed
         unique_colors = np.unique(input_grid_np)
         if len(unique_colors) <= 2: # Background + at most one other color
              return output_grid
         else:
              # Fallback or error if frame identification failed unexpectedly
              print("Error: Frame color identification failed unexpectedly.")
              return output_grid # Return original grid as fallback


    # 2. Perform flood fill from background to find external cells
    background_coords = list(zip(*np.where(input_grid_np == 0)))
    # The fill should treat frame_color cells as walls
    external_cells = _flood_fill(input_grid_np, background_coords, frame_color)

    # 3. Generate the output grid
    for r in range(rows):
        for c in range(cols):
            # Rule a: If the cell has the frame color, keep it.
            if input_grid_np[r, c] == frame_color:
                output_grid[r, c] = frame_color
            # Rule b: If the cell is external (reachable from background without crossing frame), keep its original color.
            elif (r, c) in external_cells:
                output_grid[r, c] = input_grid_np[r, c]
            # Rule c: Otherwise (it's internal and not the frame color), change it to the frame color.
            else:
                output_grid[r, c] = frame_color
                
    return output_grid.tolist() # Convert back to list of lists if needed by the environment

```
```python
import numpy as np
from collections import deque

"""
Identifies "valid frame colors" by checking if treating a color as a wall during a background flood fill isolates other non-zero colors. 
Performs a final background flood fill treating all valid frame colors as walls to determine "external" cells.
Creates the output grid:
- Cells with a valid frame color retain their color.
- External cells retain their original color.
- Internal cells (not frame color, not external) take the color of an adjacent valid frame color cell from the input grid.
"""

def _get_neighbors(r, c, rows, cols):
    """ Helper to get valid 4-connectivity neighbors. """
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def _flood_fill(grid, start_coords, wall_colors):
    """
    Performs a flood fill (BFS) starting from start_coords.
    Returns a set of reachable coordinates, avoiding cells with colors in wall_colors set.
    """
    rows, cols = grid.shape
    q = deque(start_coords)
    reachable = set(start_coords)
    
    # Ensure start coordinates themselves aren't walls, although background (0) shouldn't be.
    initial_q = deque()
    for r, c in start_coords:
         if grid[r,c] not in wall_colors:
              initial_q.append((r,c))
         # Add wall start coords to reachable if they started there, though usually they are 0
         # else:
         #     reachable.add((r,c)) # Not needed if start_coords are guaranteed non-wall

    q = initial_q # Use filtered queue

    visited = set(start_coords) # Keep track of visited to avoid cycles and redundant checks

    while q:
        r, c = q.popleft()
        reachable.add((r, c)) # Mark current cell as reachable

        for nr, nc in _get_neighbors(r, c, rows, cols):
            neighbor_coord = (nr, nc)
            # Check if neighbor is reachable: not already visited and not a wall color
            if neighbor_coord not in visited and grid[nr, nc] not in wall_colors:
                visited.add(neighbor_coord)
                q.append(neighbor_coord)

    return reachable


def _find_valid_frame_colors(grid):
    """
    Identifies the set of valid frame colors.
    A color Cf is a valid frame color if treating it as a wall during a background
    flood fill leaves at least one other non-zero, non-Cf cell unreachable.
    """
    rows, cols = grid.shape
    non_zero_colors = np.unique(grid[grid != 0])
    valid_frame_colors = set()

    if len(non_zero_colors) < 2:
        return valid_frame_colors # Need at least two non-zero colors

    background_coords = list(zip(*np.where(grid == 0)))
    if not background_coords: # Handle grids with no background
        # In this specific problem context, background always seems to exist.
        # If not, the definition of "external" breaks down. Assume background exists.
         pass

    all_non_zero_coords = list(zip(*np.where(grid != 0)))

    for potential_frame_color in non_zero_colors:
        # Perform test flood fill from background, treating potential_frame_color as the *only* wall
        # We need a single color wall set for this test fill
        wall_set_test = {potential_frame_color}
        reachable_test = _flood_fill(grid, background_coords, wall_set_test)

        # Check if any non-zero cell (that isn't the potential frame color) is *not* reachable
        unreachable_internal_found = False
        for r_nz, c_nz in all_non_zero_coords:
            if grid[r_nz, c_nz] != potential_frame_color:
                if (r_nz, c_nz) not in reachable_test:
                    unreachable_internal_found = True
                    break # Found an unreachable internal cell for this potential frame color

        if unreachable_internal_found:
            valid_frame_colors.add(potential_frame_color) # This is a valid frame color

    return valid_frame_colors


def transform(input_grid):
    """
    Transforms the input grid based on frame color identification and flood fill.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = np.copy(input_grid_np) # Initialize output as a copy

    # 1. Identify the set of valid frame colors
    valid_frame_colors = _find_valid_frame_colors(input_grid_np)

    # If no valid frame colors are found, likely implies no enclosed regions exist as per the task definition. Return original.
    if not valid_frame_colors:
        return input_grid # Return the original grid as list of lists

    # 2. Determine the final set of external cells using all valid frame colors as walls
    background_coords = list(zip(*np.where(input_grid_np == 0)))
    if not background_coords and np.all(input_grid_np != 0):
         # Edge case: grid completely filled, no background.
         # Based on examples, this shouldn't happen. Assume background exists.
         # If it did happen, all non-frame cells would arguably be internal.
         external_cells_final = set()
    elif not background_coords: # No background but some zeros might exist isolatedly? Seems unlikely.
        external_cells_final = set() # Default to no external cells if background finding fails unexpectedly
    else:
        external_cells_final = _flood_fill(input_grid_np, background_coords, valid_frame_colors)

    # 3. Generate the output grid by iterating and applying rules
    for r in range(rows):
        for c in range(cols):
            input_color = input_grid_np[r, c]
            coord = (r, c)

            # Rule: If the cell has a valid frame color, keep it.
            if input_color in valid_frame_colors:
                output_grid[r, c] = input_color
                continue # Skip other checks for this cell

            # Rule: If the cell is external, keep its original color.
            # Note: This also correctly keeps background (0) cells that are external.
            if coord in external_cells_final:
                output_grid[r, c] = input_color
                continue # Skip other checks for this cell

            # Rule: Otherwise (cell is internal and not a frame color), change it
            #       to the color of an adjacent valid frame color cell.
            else:
                adjacent_frame_color = -1 # Default/error value
                found_neighbor = False
                for nr, nc in _get_neighbors(r, c, rows, cols):
                    neighbor_color = input_grid_np[nr, nc]
                    if neighbor_color in valid_frame_colors:
                        adjacent_frame_color = neighbor_color
                        found_neighbor = True
                        break # Found one, use it

                if found_neighbor:
                    output_grid[r, c] = adjacent_frame_color
                else:
                    # This case *shouldn't* happen if the logic is correct for the given examples.
                    # An internal, non-frame cell must be adjacent to a frame cell that separates it.
                    # If it happens, keep original color as a fallback? Or raise error? Keep original for now.
                    output_grid[r, c] = input_color # Fallback
                    # print(f"Warning: Internal cell ({r},{c}) with color {input_color} had no valid frame neighbor.")


    return output_grid.tolist() # Convert back to list of lists
```
