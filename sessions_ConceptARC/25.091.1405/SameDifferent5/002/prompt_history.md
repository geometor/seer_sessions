
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 0 0
0 2 4 2 0 3 1 3 0 0 0
0 2 2 2 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 7 7 7
0 0 0 6 4 6 0 0 7 8 7
0 0 0 6 6 6 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 0
0 3 3 3 3 0 0 0 0 4 5 5 4 0
0 3 2 2 3 0 0 0 0 4 5 5 4 0
0 3 2 2 3 0 0 0 0 4 4 4 4 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 8 7 7 8 0 0 0
0 0 0 0 0 0 0 8 7 7 8 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 9 9 9 9 0 0 0 0 0 0 0 0
0 0 9 4 4 9 0 0 1 1 1 1 0 0
0 0 9 4 4 9 0 0 1 2 2 1 0 0
0 0 9 9 9 9 0 0 1 2 2 1 0 0
0 0 0 0 0 0 0 0 1 1 1 1 0 0
```


**output:**
```
2
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 7 3 0 0 5 5 5 0
0 3 7 3 0 0 5 7 5 0
0 3 3 3 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 4 4 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
```


**output:**
```
7
```

*   **Perception:** The input is a grid containing multiple distinct shapes or objects, often composed of a primary "boundary" color and a secondary "inner" or "center" color. The background is typically white (0). The output is always a single digit, which corresponds to one of the colors present in the input grid. The task seems to involve analyzing the properties of the objects, specifically their inner colors, and determining which inner color is the most common across all objects in the grid.

*   **Facts:**
    
```yaml
    task_type: analysis
    elements:
      - type: grid
        description: Input grid containing pixels of various colors (0-9).
      - type: object
        description: A contiguous block of non-white pixels.
        properties:
          - boundary_color: The primary color forming the outer part of the object.
          - inner_color: A color different from the boundary_color, located inside the object. Not all objects have an inner_color.
      - type: color_count
        description: Frequency of occurrence for each inner_color across all objects in the grid.
      - type: output_value
        description: A single digit (0-9) representing a color.
    relationships:
      - The output_value corresponds to the inner_color that appears most frequently among all objects in the input grid.
    actions:
      - Identify all distinct objects in the input grid.
      - For each object, determine its boundary_color and, if present, its inner_color.
      - Count the occurrences of each unique inner_color found.
      - Identify the inner_color with the highest count.
      - Output the digit corresponding to the most frequent inner_color.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify all separate objects (contiguous groups of non-white pixels).
    2.  For each identified object:
        a.  Determine its main boundary color.
        b.  Check if there are any pixels inside the object (surrounded by the boundary color) that have a different color. This is the object's "inner color". Note that an object might not have an inner color, or it might have multiple pixels of the same inner color.
        c.  If an inner color exists, record it.
    3.  Create a list of all inner colors found across all objects in the grid.
    4.  Count the frequency of each unique color in this list.
    5.  Find the color that has the highest frequency (the mode).
    6.  The output is the single digit representing this most frequent inner color.
```python
import numpy as np
from collections import deque, Counter

"""
Identify all distinct objects (contiguous blocks of the same non-background color).
For each pixel in the grid that is not part of any object's boundary and is not background (color 0):
  Check if all its 4 cardinal neighbors belong to the boundary of *one single* object.
  If so, this pixel's color is considered an "inner color".
Collect all such inner colors found across the grid.
Count the frequency of each inner color.
The output is the color that appears most frequently (the mode).
"""

def find_objects(grid):
    """
    Finds connected components of the same non-background color in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'coords' (a set of (row, col) tuples) and 'color' (int).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Start BFS from unvisited non-background pixels
            if color != 0 and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))
                
                # Breadth-First Search to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-connectivity
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the same color and unvisited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                
                # Store the found object
                objects.append({'coords': obj_coords, 'color': color})
    return objects

def transform(input_grid_list):
    """
    Transforms the input grid based on the identified rule.
    Finds the most frequent "inner color" surrounded by object boundaries.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        int: The most frequent inner color found in the grid. Returns 0 if none found.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape
    
    # 1. Identify all objects (boundaries)
    objects = find_objects(input_grid)
    
    # Create a set of all boundary coordinates for faster lookup
    all_boundary_coords = set()
    for obj in objects:
        all_boundary_coords.update(obj['coords'])
        
    inner_colors = []
    
    # 2. Iterate through grid to find inner pixels
    for r in range(rows):
        for c in range(cols):
            pixel_color = input_grid[r, c]
            
            # 2a. Skip background color and pixels that are part of a boundary
            if pixel_color == 0 or (r, c) in all_boundary_coords:
                continue

            # 2b. Check neighbors to see if it's an inner pixel
            neighbor_boundary_color = -1 # Track the color of the surrounding boundary
            is_surrounded_by_one_boundary = True
            
            neighbors = []
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 neighbors.append((r + dr, c + dc))

            for nr, nc in neighbors:
                # Check bounds: all neighbors must be within grid
                if not (0 <= nr < rows and 0 <= nc < cols):
                    is_surrounded_by_one_boundary = False
                    break
                    
                # Check if neighbor is part of *any* boundary
                current_neighbor_boundary_color = -1
                neighbor_is_boundary = False
                for obj in objects:
                     if (nr, nc) in obj['coords']:
                         neighbor_is_boundary = True
                         current_neighbor_boundary_color = obj['color']
                         break # Found the boundary object this neighbor belongs to

                # Neighbor must be part of a boundary
                if not neighbor_is_boundary:
                    is_surrounded_by_one_boundary = False
                    break

                # Track the color of the surrounding boundary
                if neighbor_boundary_color == -1:
                    # Store the color of the first boundary neighbor found
                    neighbor_boundary_color = current_neighbor_boundary_color
                # Ensure all subsequent boundary neighbors have the *same* color
                elif neighbor_boundary_color != current_neighbor_boundary_color:
                    is_surrounded_by_one_boundary = False
                    break

            # 2c. If the pixel is surrounded by exactly one boundary color, add its color to list
            if is_surrounded_by_one_boundary and neighbor_boundary_color != -1:
                 inner_colors.append(pixel_color)

    # 3. Count frequencies and find the mode
    if not inner_colors:
        # Handle cases where no inner colors are found as per the definition
        # This might indicate an issue or an edge case not covered by examples.
        # Returning 0 seems like a safe default, although ambiguity exists.
        return 0 

    counts = Counter(inner_colors)
    
    # Find the mode (most frequent color). 
    # Counter.most_common(1) returns a list like [(element, count)]
    # If there are ties for the most common, most_common() provides one arbitrarily.
    most_common_color = counts.most_common(1)[0][0] 
    
    # 4. Return the single integer representing the most frequent inner color
    return most_common_color
```
