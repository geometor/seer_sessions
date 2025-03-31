
## train_1

**input:**
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 0 0 0 3 9
9 3 3 3 3 0 0 9 3 0
3 3 3 3 3 9 0 0 3 7
3 3 3 3 3 0 9 9 3 0
0 9 0 3 3 3 9 9 9 9
7 9 7 9 0 0 7 7 0 0
```


**output:**
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 3 3 0 3 9
9 3 3 3 3 3 3 3 3 0
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
0 9 0 3 3 3 3 9 9 9
7 9 7 9 0 0 7 7 0 0
```


## train_2

**input:**
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 0 0
6 1 1 1 1 1 1 1 6 0
6 1 1 1 1 1 1 1 6 8
0 8 1 1 1 8 6 8 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```


**output:**
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 8
0 8 1 1 1 1 1 1 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```


## train_3

**input:**
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 0 0 1 1 0
0 0 1 2 2 2 1 0 1 0
0 4 0 2 2 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 1 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```


**output:**
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 2 2 2 1 0
0 0 1 2 2 2 2 0 1 0
0 4 0 2 2 2 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 2 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```

Okay, let's analyze the task based on the provided examples.

**1. Perception of the Elements**

*   **Grid Structure:** The input and output are both 10x10 grids of colored pixels.
*   **Color Palette:** Several distinct colors are used in each example (maroon, white, orange, green in #1; magenta, azure, white, blue in #2; blue, white, yellow, red in #3). The background color (white/0) is present but doesn't seem to play a unique role compared to other colors involved in the transformation.
*   **Objects:** Each grid contains various contiguous blocks (objects) of single colors. In each example, one color forms a significantly larger connected component than others (green in #1, blue in #2, red in #3).
*   **Transformation:** The transformation modifies only a subset of the pixels. The output grid largely resembles the input grid, with specific regions changed. The change involves replacing pixels of certain colors with the color of the largest connected object.
*   **Nature of Change:** The change appears to be a "filling" process. Pixels that are *not* part of the largest object but are located in areas "enclosed" or forming "cavities" within that largest object are repainted with the object's color. These cavities can contain pixels of multiple different colors initially. Pixels belonging to the largest object itself are never changed. Pixels outside the largest object and reachable from the grid's border without crossing the largest object are also unchanged.

**2. Facts**


```yaml
task_elements:
  - grid:
      type: 2D array of integers (colors)
      properties:
        - height: 10
        - width: 10
  - objects:
      type: connected components of same-colored pixels
      properties:
        - color
        - size (pixel count)
        - location (set of coordinates)
        - connectivity (adjacency to other objects)
      identification:
        - LCC: Largest Connected Component (by pixel count). Let its color be 'dominant_color'.
  - relationships:
      - adjacency: pixels can be adjacent orthogonally or diagonally.
      - reachability: pixels can be reached from others via paths of adjacent pixels.
      - enclosure: some regions/components of non-dominant colors are not reachable from the grid border without crossing through a pixel with the 'dominant_color'. These are 'cavities'.
  - actions:
      - identify_LCC: Find the connected component with the maximum number of pixels. Determine its color ('dominant_color').
      - identify_cavities: Find all pixels that are NOT 'dominant_color' AND are NOT reachable from any border cell via a path consisting solely of non-'dominant_color' pixels.
      - fill_cavities: Change the color of all pixels identified as belonging to a cavity to 'dominant_color'.

example_specific_facts:
  - train_1:
      dominant_color: 3 (green)
      cavity_pixels_original_colors: [0 (white), 9 (maroon)]
      cavity_fill_color: 3 (green)
  - train_2:
      dominant_color: 1 (blue)
      cavity_pixels_original_colors: [0 (white), 6 (magenta), 8 (azure)]
      cavity_fill_color: 1 (blue)
  - train_3:
      dominant_color: 2 (red)
      cavity_pixels_original_colors: [0 (white), 1 (blue)]
      cavity_fill_color: 2 (red)
```


**3. Natural Language Program**

1.  **Identify the Dominant Object:** Examine the input grid to find all connected components (objects) of same-colored pixels, considering orthogonal and diagonal adjacency. Determine the component with the largest number of pixels. Record the color of this largest connected component (LCC); call it the `dominant_color`.
2.  **Identify External Regions:** Perform a search (like flood fill or Breadth-First Search) starting from *all* cells located on the borders (top, bottom, left, right edges) of the grid. This search can propagate to adjacent (orthogonal or diagonal) cells, but it *cannot* enter any cell whose color is the `dominant_color`. Mark all cells visited by this search as "externally reachable".
3.  **Identify and Fill Cavities:** Create a copy of the input grid to serve as the output grid. Iterate through every cell `(row, col)` of the grid. If the cell `(row, col)` in the input grid:
    *   a) does *not* have the `dominant_color`, AND
    *   b) was *not* marked as "externally reachable" in step 2,
    then change the color of the cell `(row, col)` in the output grid to the `dominant_color`.
4.  **Finalize Output:** All cells not meeting the criteria in step 3 retain their original color from the input grid. The resulting grid is the final output.
```python
import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1.  **Identify the Dominant Object:** Find the largest connected component (LCC) of pixels of the same color in the input grid, considering both orthogonal and diagonal adjacency. Determine the color of this LCC ('dominant_color').
2.  **Identify External Regions:** Perform a search (e.g., Breadth-First Search) starting from all border cells of the grid. This search propagates to adjacent cells (orthogonally and diagonally) but cannot pass through any cell with the 'dominant_color'. Mark all reachable cells from the border without crossing the 'dominant_color' as "externally reachable".
3.  **Identify and Fill Cavities:** Create a copy of the input grid. Iterate through each cell of the grid. If a cell in the input grid does *not* have the 'dominant_color' and was *not* marked as "externally reachable", change its color in the copied grid to the 'dominant_color'.
4.  **Output:** The modified copied grid is the final output. Cells that are part of the LCC or are externally reachable retain their original colors.
"""

def find_largest_connected_component(grid):
    """
    Finds the largest connected component (LCC) in the grid.
    Connectivity includes diagonals.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (dominant_color, set_of_coordinates) of the LCC.
               Returns (None, set()) if the grid is empty.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0
    lcc_color = None
    lcc_coords = set()

    # Define 8 directions for connectivity (orthogonal + diagonal)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                component_color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_coords.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()

                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == component_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_coords.add((nr, nc))

                if len(component_coords) > max_size:
                    max_size = len(component_coords)
                    lcc_color = component_color
                    lcc_coords = component_coords

    return lcc_color, lcc_coords


def find_externally_reachable(grid, dominant_color):
    """
    Finds all cells reachable from the border without crossing the dominant color.
    Connectivity includes diagonals.

    Args:
        grid (np.ndarray): The input grid.
        dominant_color (int): The color of the LCC.

    Returns:
        set: A set of coordinates (r, c) of externally reachable cells.
    """
    height, width = grid.shape
    reachable = set()
    q = deque()

    # Define 8 directions for connectivity
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Add border cells to queue if they are not the dominant color
    for r in range(height):
        for c in range(width):
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                if grid[r, c] != dominant_color and (r, c) not in reachable:
                    q.append((r, c))
                    reachable.add((r, c))

    # Perform BFS
    while q:
        curr_r, curr_c = q.popleft()

        for dr, dc in directions:
            nr, nc = curr_r + dr, curr_c + dc

            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] != dominant_color and (nr, nc) not in reachable:
                reachable.add((nr, nc))
                q.append((nr, nc))

    return reachable


def transform(input_grid_list):
    """
    Transforms the input grid based on the described rule:
    Finds the largest connected component (LCC), identifies cells not
    belonging to the LCC that are enclosed by it (not reachable from the border
    without crossing the LCC), and fills these enclosed cells with the LCC's color.

    Args:
        input_grid_list (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    
    # --- Step 1: Identify the Dominant Object (LCC) ---
    dominant_color, lcc_coords = find_largest_connected_component(input_grid)

    # Handle edge case where grid might be empty or uniform background
    if dominant_color is None:
        return input_grid_list # Return original if no component found

    # --- Step 2: Identify External Regions ---
    # Find all cells reachable from the border without passing through the dominant color
    externally_reachable_coords = find_externally_reachable(input_grid, dominant_color)

    # --- Step 3: Identify and Fill Cavities ---
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Iterate through all cells
    for r in range(height):
        for c in range(width):
            # Check if the cell is NOT the dominant color AND is NOT externally reachable
            # Note: We don't need to check if it's part of lcc_coords explicitly,
            # because if it were, its color would be dominant_color.
            if input_grid[r, c] != dominant_color and (r, c) not in externally_reachable_coords:
                # This cell is inside a cavity, fill it with the dominant color
                output_grid[r, c] = dominant_color

    # --- Step 4: Finalize Output ---
    # Convert the numpy array back to a list of lists
    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1.  **Identify the Dominant Object:** Find the largest connected component (LCC) of pixels of the same color in the input grid, considering both orthogonal and diagonal adjacency. Determine the color of this LCC ('dominant_color').
2.  **Identify External Regions:** Perform a search (e.g., Breadth-First Search) starting from all border cells of the grid. This search propagates to adjacent cells (orthogonally and diagonally) but cannot pass through any cell with the 'dominant_color'. Mark all reachable cells from the border without crossing the 'dominant_color' as "externally reachable".
3.  **Identify and Fill Cavities:** Create a copy of the input grid. Iterate through each cell of the grid. If a cell in the input grid does *not* have the 'dominant_color' and was *not* marked as "externally reachable", change its color in the copied grid to the 'dominant_color'.
4.  **Output:** The modified copied grid is the final output. Cells that are part of the LCC or are externally reachable retain their original colors.
"""

def find_largest_connected_component(grid):
    """
    Finds the largest connected component (LCC) in the grid.
    Connectivity includes diagonals.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (dominant_color, set_of_coordinates) of the LCC.
               Returns (None, set()) if the grid is empty.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0
    lcc_color = None
    lcc_coords = set()

    # Define 8 directions for connectivity (orthogonal + diagonal)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                component_color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_coords.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()

                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == component_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_coords.add((nr, nc))

                if len(component_coords) > max_size:
                    max_size = len(component_coords)
                    lcc_color = component_color
                    lcc_coords = component_coords

    return lcc_color, lcc_coords


def find_externally_reachable(grid, dominant_color):
    """
    Finds all cells reachable from the border without crossing the dominant color.
    Connectivity includes diagonals.

    Args:
        grid (np.ndarray): The input grid.
        dominant_color (int): The color of the LCC.

    Returns:
        set: A set of coordinates (r, c) of externally reachable cells.
    """
    height, width = grid.shape
    reachable = set()
    q = deque()

    # Define 8 directions for connectivity
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Add border cells to queue if they are not the dominant color
    for r in range(height):
        for c in range(width):
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                if grid[r, c] != dominant_color and (r, c) not in reachable:
                    q.append((r, c))
                    reachable.add((r, c))

    # Perform BFS
    while q:
        curr_r, curr_c = q.popleft()

        for dr, dc in directions:
            nr, nc = curr_r + dr, curr_c + dc

            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] != dominant_color and (nr, nc) not in reachable:
                reachable.add((nr, nc))
                q.append((nr, nc))

    return reachable


def transform(input_grid_list):
    """
    Transforms the input grid based on the described rule:
    Finds the largest connected component (LCC), identifies cells not
    belonging to the LCC that are enclosed by it (not reachable from the border
    without crossing the LCC), and fills these enclosed cells with the LCC's color.

    Args:
        input_grid_list (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    
    # --- Step 1: Identify the Dominant Object (LCC) ---
    dominant_color, lcc_coords = find_largest_connected_component(input_grid)

    # Handle edge case where grid might be empty or uniform background
    if dominant_color is None:
        return input_grid_list # Return original if no component found

    # --- Step 2: Identify External Regions ---
    # Find all cells reachable from the border without passing through the dominant color
    externally_reachable_coords = find_externally_reachable(input_grid, dominant_color)

    # --- Step 3: Identify and Fill Cavities ---
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Iterate through all cells
    for r in range(height):
        for c in range(width):
            # Check if the cell is NOT the dominant color AND is NOT externally reachable
            # Note: We don't need to check if it's part of lcc_coords explicitly,
            # because if it were, its color would be dominant_color.
            if input_grid[r, c] != dominant_color and (r, c) not in externally_reachable_coords:
                # This cell is inside a cavity, fill it with the dominant color
                output_grid[r, c] = dominant_color

    # --- Step 4: Finalize Output ---
    # Convert the numpy array back to a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 0 0 0 3 9
9 3 3 3 3 0 0 9 3 0
3 3 3 3 3 9 0 0 3 7
3 3 3 3 3 0 9 9 3 0
0 9 0 3 3 3 9 9 9 9
7 9 7 9 0 0 7 7 0 0
```
Expected Output:
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 3 3 0 3 9
9 3 3 3 3 3 3 3 3 0
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
0 9 0 3 3 3 3 9 9 9
7 9 7 9 0 0 7 7 0 0
```
Transformed Output:
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 0 0 0 3 9
9 3 3 3 3 0 0 9 3 0
3 3 3 3 3 9 0 0 3 7
3 3 3 3 3 0 9 9 3 0
0 9 0 3 3 3 9 9 9 9
7 9 7 9 0 0 7 7 0 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 28.0

## Example 2:
Input:
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 0 0
6 1 1 1 1 1 1 1 6 0
6 1 1 1 1 1 1 1 6 8
0 8 1 1 1 8 6 8 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```
Expected Output:
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 8
0 8 1 1 1 1 1 1 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```
Transformed Output:
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 0 0
6 1 1 1 1 1 1 1 6 0
6 1 1 1 1 1 1 1 6 8
0 8 1 1 1 8 6 8 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.0

## Example 3:
Input:
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 0 0 1 1 0
0 0 1 2 2 2 1 0 1 0
0 4 0 2 2 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 1 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```
Expected Output:
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 2 2 2 1 0
0 0 1 2 2 2 2 0 1 0
0 4 0 2 2 2 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 2 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```
Transformed Output:
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 0 0 1 1 0
0 0 1 2 2 2 1 0 1 0
0 4 0 2 2 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 1 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.0
