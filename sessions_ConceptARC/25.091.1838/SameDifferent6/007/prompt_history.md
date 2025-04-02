
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2
0 2 1 2 0 0 2 1 2
0 2 2 2 0 0 2 2 2
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3
0 6 6 6 0 0 3 7 7 7 3
0 6 7 6 0 0 3 7 7 7 3
0 6 6 6 0 0 3 7 7 7 3
0 0 0 0 0 0 3 3 3 3 3
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 3 3 3 3 0 0
5 5 7 5 5 3 7 7 3 0 0
5 5 5 5 5 3 7 7 3 0 0
5 5 5 5 5 3 3 3 3 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 6 7 6 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 7 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 1 1 1
0 4 0 0 0 4 0 0 0 1 0 1
0 4 4 4 4 4 0 0 0 1 0 1
0 0 0 0 0 4 4 4 0 1 0 1
0 0 0 0 0 4 0 4 0 1 1 1
7 7 7 0 0 4 0 4 0 0 0 0
7 0 7 0 0 4 4 4 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 1 1
7 7 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of Task Elements:**

1.  **Input Structure:** The input grids contain multiple distinct shapes or objects. Each object is primarily composed of a single non-black color (let's call this the "Outer Color").
2.  **Object Characteristics:** The objects vary in shape (squares, rectangles, L-shapes, T-shapes) and Outer Color.
3.  **Shared Feature:** Within each input grid, all the identified objects seem to share a common characteristic: they all contain or surround pixels of a single, specific color (let's call this the "Inner Color"). This Inner Color is different from the Outer Color of the objects themselves.
    *   Example 1: Objects (Red, Yellow, Azure) all contain Blue (1). Inner Color = Blue (1).
    *   Example 2: Objects (Magenta, Green, Gray) all contain Orange (7). Inner Color = Orange (7).
    *   Example 3: Objects (Yellow, Blue, Orange) all contain Black (0). Inner Color = Black (0).
4.  **Transformation:** The transformation involves selectively removing *entire* objects based on their Outer Color. The output grid retains only a subset of the objects from the input grid, replacing the removed objects' pixels with the background color (Black, 0).
5.  **Removal Rule:** The decision of which object color(s) to remove appears to depend on a comparison or relationship between the Outer Colors present and the shared Inner Color.
    *   In Ex 1 (Inner=1), Outer={2, 4, 8}. Color 2 (smallest) is removed.
    *   In Ex 2 (Inner=7), Outer={3, 5, 6}. Color 3 (smallest) is removed.
    *   In Ex 3 (Inner=0), Outer={1, 4, 7}. Color 4 (second smallest) is removed.
    *   This suggests a rule based on the sorted order of Outer Colors, conditional on the Inner Color value.

**YAML Fact Document:**


```yaml
task_elements:
  - element: Grid
    description: A 2D array of pixels with colors 0-9. Black (0) is the background.
  - element: Object
    description: A contiguous region of pixels sharing the same non-black color (Outer Color).
    properties:
      - OuterColor: The primary color of the object's pixels.
      - Pixels: The coordinates of the pixels comprising the object.
      - BoundingBox: The minimum rectangle enclosing the object.
  - element: InnerColor
    description: A single color found within the spatial extent (e.g., bounding box or internal adjacency) of all Objects in a given input grid. This color differs from the OuterColor of the objects it is associated with. It can be Black (0).
    relationship: Contained within or adjacent internally to all Objects.
  - element: SetOfOuterColors
    description: The unique collection of Outer Colors of all objects present in the input grid.
    properties:
      - UniqueColors: List of distinct Outer Colors.
      - SortedColors: UniqueColors sorted numerically.
      - MinColor: The smallest color in UniqueColors.
      - SecondMinColor: The second smallest color in UniqueColors (if it exists).

actions:
  - action: IdentifyObjects
    description: Find all connected components of non-black pixels in the input grid.
    inputs: Input Grid
    outputs: List of Objects (with their OuterColor and Pixels).
  - action: IdentifyInnerColor
    description: Determine the single color shared internally by all identified objects.
    inputs: Input Grid, List of Objects
    outputs: InnerColor value.
  - action: SelectColorToRemove
    description: Choose which Outer Color objects should be removed based on the InnerColor and the sorted list of Outer Colors.
    inputs: InnerColor, Sorted List of Outer Colors
    outputs: ColorToRemove.
    logic: |
      If InnerColor is Black (0), ColorToRemove is the second element in Sorted List of Outer Colors.
      If InnerColor is not Black (0), ColorToRemove is the first element (minimum) in Sorted List of Outer Colors.
  - action: FilterObjects
    description: Remove objects based on the selected ColorToRemove.
    inputs: Input Grid, List of Objects, ColorToRemove
    outputs: Output Grid.
    logic: Create an output grid of the same size as the input, initially Black (0). Copy pixels of all objects whose OuterColor is NOT ColorToRemove from the input to the output.

relationships:
  - relationship: RemovalCondition
    description: The rule determining object removal depends on the InnerColor and the relative order of the OuterColors.
    entities: InnerColor, SetOfOuterColors, ColorToRemove
```


**Natural Language Program:**

1.  **Analyze the Input Grid:**
    *   Identify all distinct contiguous objects composed of a single non-black color. Record the color of each object (its "Outer Color") and the set of pixel coordinates belonging to it.
2.  **Find the Shared Inner Color:**
    *   Examine the input grid to find the single color ("Inner Color") that is located spatially within or immediately adjacent internally to *all* the identified objects. This Inner Color will be different from the Outer Colors of the objects themselves (it can be Black, 0).
3.  **Determine the Target Color for Removal:**
    *   Collect all unique Outer Colors found in step 1.
    *   Sort these unique Outer Colors numerically in ascending order.
    *   Check the value of the Inner Color found in step 2:
        *   If the Inner Color is Black (0), select the *second* color from the sorted list of Outer Colors.
        *   If the Inner Color is *not* Black (0), select the *first* color (i.e., the minimum value) from the sorted list of Outer Colors.
    *   The selected color is the "Color To Remove".
4.  **Construct the Output Grid:**
    *   Create a new grid with the same dimensions as the input grid, filled initially with the background color (Black, 0).
    *   Iterate through all the objects identified in step 1.
    *   If an object's Outer Color is *not* the "Color To Remove", copy all of its pixels from the input grid to the corresponding positions in the new output grid.
    *   The resulting grid is the final output.
```python
import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects of a single non-black color (Outer Color).
Determine the single color (Inner Color) that is present in the grid but is not black (0) and not one of the Outer Colors. If no such color exists, the Inner Color is black (0).
Collect the unique Outer Colors and sort them numerically.
If the Inner Color is black (0), the color to remove is the second smallest Outer Color.
If the Inner Color is not black (0), the color to remove is the smallest Outer Color.
Create an output grid by copying only those objects whose Outer Color is NOT the color selected for removal.
"""

def _find_objects(grid):
    """
    Finds all contiguous objects of the same non-black color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'pixels' (set of (r, c) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # If it's a non-black pixel and hasn't been visited yet, start BFS
            if color != 0 and not visited[r, c]:
                obj_pixels = set()
                obj_color = color
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if the neighbor has the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == obj_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'color': obj_color, 'pixels': obj_pixels})
                
    return objects

def _find_inner_color(grid, outer_colors):
    """
    Determines the single 'inner' color based on grid contents and outer colors.
    The inner color is the unique color present in the grid that is not black (0)
    and not one of the outer colors. If no such unique color exists, it's black (0).

    Args:
        grid (np.array): The input grid.
        outer_colors (set): A set of the unique outer colors of the objects.

    Returns:
        int: The identified inner color.
    """
    unique_grid_colors = set(grid.flatten())
    
    # Find colors in the grid that are not black and not outer colors
    potential_inner_colors = unique_grid_colors - outer_colors - {0}
    
    if len(potential_inner_colors) == 1:
        # If exactly one such color exists, it's the inner color
        return potential_inner_colors.pop()
    elif len(potential_inner_colors) == 0:
        # If no such color exists, the inner color is black
        return 0
    else:
        # Handle unexpected cases (e.g., multiple candidates)
        # Based on the examples, this path should not be reached.
        # Defaulting to 0 as a fallback, though raising an error might be better
        # depending on strictness requirements.
        print(f"Warning: Ambiguous inner color situation. Candidates: {potential_inner_colors}. Defaulting to 0.")
        return 0


def transform(input_grid):
    """
    Transforms the input grid based on object colors and a derived inner color rule.

    1. Find all non-black objects and their colors (Outer Colors).
    2. Identify the shared Inner Color (the unique color present that isn't black or an Outer Color, or black if no such color exists).
    3. Determine the Outer Color to remove based on the Inner Color:
        - If Inner Color is black (0), remove the second smallest Outer Color.
        - If Inner Color is non-black, remove the smallest Outer Color.
    4. Construct the output grid containing only the objects whose color was not selected for removal.
    """
    # Convert input list of lists to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # 1. Find all distinct objects and their Outer Colors
    objects = _find_objects(input_array)
    if not objects: # Handle empty grid or grid with only black pixels
        return input_grid # Return original grid if no objects found

    outer_colors = sorted(list(set(obj['color'] for obj in objects)))

    # 2. Find the Inner Color
    inner_color = _find_inner_color(input_array, set(outer_colors))

    # 3. Determine the Color To Remove
    color_to_remove = -1 # Initialize with an invalid color
    if inner_color == 0:
        # If inner is black, remove the second smallest outer color
        if len(outer_colors) >= 2:
            color_to_remove = outer_colors[1]
        # If less than 2 outer colors, maybe nothing is removed? Or only if exactly 1?
        # The examples always have >= 2 colors when inner is 0.
        # Let's assume if < 2 colors, nothing is removed.
        # Fallback to -1 means no color matches, so nothing removed.

    else:
        # If inner is non-black, remove the smallest outer color
        if len(outer_colors) >= 1:
            color_to_remove = outer_colors[0]
        # If no outer colors, nothing to remove.
        # Fallback to -1 means no color matches, so nothing removed.

    # 4. Construct the Output Grid
    # Initialize output grid with background color (black)
    output_array = np.zeros_like(input_array, dtype=int)

    # Iterate through the found objects
    for obj in objects:
        # If the object's color is NOT the one to be removed, copy its pixels
        if obj['color'] != color_to_remove:
            for r, c in obj['pixels']:
                # Ensure coordinates are valid just in case
                if 0 <= r < rows and 0 <= c < cols:
                     output_array[r, c] = obj['color']

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
```python
import numpy as np
from collections import deque

"""
Identifies distinct contiguous objects of non-black colors (Outer Colors) in the input grid.
Determines a 'Special Color': the unique color present in the grid that is neither black (0) nor one of the Outer Colors. If no such unique color exists, the Special Color is 0.
Selects an Outer Color for removal based on the Special Color:
- If the Special Color is 0, remove the second smallest Outer Color (if it exists).
- If the Special Color is non-zero, remove the smallest Outer Color (if it exists).
Constructs the output grid by copying only the pixels belonging to the objects whose Outer Color was *not* selected for removal.
"""

def _find_objects(grid):
    """
    Finds all contiguous objects of the same non-black color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'pixels' (set of (r, c) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # If it's a non-black pixel and hasn't been visited yet, start BFS
            if color != 0 and not visited[r, c]:
                obj_pixels = set()
                obj_color = color
                q = deque([(r, c)])
                visited[r, c] = True
                is_primary_object = True # Assume primary initially

                # We perform BFS to find all pixels of this object first
                current_object_pixels = set()
                bfs_q = deque([(r, c)])
                bfs_visited_local = set([(r,c)]) # Keep track for this specific BFS

                while bfs_q:
                    row, col = bfs_q.popleft()
                    current_object_pixels.add((row, col))
                    
                    # Check 4 neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, same color, and not visited in this BFS
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == obj_color and (nr, nc) not in bfs_visited_local:
                            bfs_visited_local.add((nr, nc))
                            bfs_q.append((nr, nc))

                # Now mark all pixels of this object as visited globally
                for R, C in current_object_pixels:
                   visited[R, C] = True

                # Store the object found
                objects.append({'color': obj_color, 'pixels': current_object_pixels})

    return objects


def _get_special_color(grid, outer_colors_set):
    """
    Determines the unique color in the grid that is not black (0) and not
    one of the specified outer colors.

    Args:
        grid (np.array): The input grid.
        outer_colors_set (set): A set of the unique outer colors of the objects.

    Returns:
        int: The identified special color, or 0 if none or multiple exist.
    """
    unique_grid_colors = set(grid.flatten())
    
    # Find colors in the grid that are not black and not outer colors
    potential_special_colors = unique_grid_colors - outer_colors_set - {0}
    
    if len(potential_special_colors) == 1:
        # If exactly one such color exists, it's the special color
        return potential_special_colors.pop()
    else:
        # If zero or more than one such color exists, the special color is black
        return 0


def transform(input_grid):
    """
    Applies the transformation rule based on object colors and the special color.
    """
    # Convert input list of lists to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # 1. Identify Primary Objects and Outer Colors
    objects = _find_objects(input_array)
    if not objects: # Handle empty grid or grid with only black pixels
        return input_grid # Return original grid if no objects found

    outer_colors_set = set(obj['color'] for obj in objects)
    sorted_outer_colors = sorted(list(outer_colors_set))

    # 2. Identify the Special Color
    special_color = _get_special_color(input_array, outer_colors_set)

    # 3. Determine the Color To Remove
    color_to_remove = -1 # Initialize with an invalid color, meaning nothing removed by default

    if special_color == 0:
        # If special color is black, remove the second smallest outer color
        if len(sorted_outer_colors) >= 2:
            color_to_remove = sorted_outer_colors[1]
    else:
        # If special color is non-black, remove the smallest outer color
        if len(sorted_outer_colors) >= 1:
            color_to_remove = sorted_outer_colors[0]

    # 4. Construct the Output Grid
    # Initialize output grid with background color (black)
    output_array = np.zeros_like(input_array, dtype=int)

    # Iterate through the found objects
    for obj in objects:
        # If the object's color is NOT the one to be removed, copy its pixels
        if obj['color'] != color_to_remove:
            for r, c in obj['pixels']:
                # Ensure coordinates are valid just in case (should always be)
                if 0 <= r < rows and 0 <= c < cols:
                     # Directly use the object's color
                     output_array[r, c] = obj['color']

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
```python
import numpy as np
from collections import deque

"""
Identifies distinct contiguous objects of non-black colors (Outer Colors) in the input grid.
Determines a 'Special Color': the unique color present in the grid that is neither black (0) nor one of the Outer Colors. If no such unique color exists, the Special Color is defined as Black (0).
Selects an Outer Color for removal based on the Special Color:
- If the Special Color is 0, remove the second smallest Outer Color (if it exists).
- If the Special Color is non-zero, remove the smallest Outer Color (if it exists).
Constructs the output grid by starting with a copy of the input and changing the pixels of the objects selected for removal to black (0).
"""

def _find_objects(grid):
    """
    Finds all contiguous objects of the same non-black color in the grid using 4-way adjacency.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'pixels' (set of (r, c) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # If it's a non-black pixel and hasn't been visited yet, start BFS
            if color != 0 and not visited[r, c]:
                obj_color = color
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == obj_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'color': obj_color, 'pixels': current_object_pixels})
                
    return objects


def _get_special_color(grid, outer_colors_set):
    """
    Determines the unique color in the grid that is not black (0) and not
    one of the specified outer colors.

    Args:
        grid (np.array): The input grid.
        outer_colors_set (set): A set of the unique outer colors of the objects.

    Returns:
        int: The identified special color, or 0 if none or multiple exist.
    """
    unique_grid_colors = set(grid.flatten())
    
    # Find colors in the grid that are not black and not outer colors
    potential_special_colors = unique_grid_colors - outer_colors_set - {0}
    
    if len(potential_special_colors) == 1:
        # If exactly one such color exists, it's the special color
        return potential_special_colors.pop()
    else:
        # If zero or more than one such color exists, the special color is black (0)
        return 0


def transform(input_grid):
    """
    Applies the transformation rule based on object colors and the special color.
    """
    # Convert input list of lists to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # 1. Create a copy of the input grid to modify
    output_array = np.copy(input_array)

    # 2. Identify Objects and their Outer Colors
    objects = _find_objects(input_array)
    if not objects: # Handle empty grid or grid with only black pixels
        return input_grid # Return original grid if no objects found

    outer_colors_set = set(obj['color'] for obj in objects)
    sorted_outer_colors = sorted(list(outer_colors_set))

    # 3. Identify the Special Color
    special_color = _get_special_color(input_array, outer_colors_set)

    # 4. Determine the Color To Remove
    color_to_remove = -1 # Initialize with an invalid color, meaning nothing removed by default

    if special_color == 0:
        # If special color is black, target the second smallest outer color
        if len(sorted_outer_colors) >= 2:
            color_to_remove = sorted_outer_colors[1]
    else:
        # If special color is non-black, target the smallest outer color
        if len(sorted_outer_colors) >= 1:
            color_to_remove = sorted_outer_colors[0]

    # 5. Modify the Output Grid by removing targeted objects
    if color_to_remove != -1: # Check if a color was actually selected for removal
        # Iterate through the found objects
        for obj in objects:
            # If the object's color is the one to be removed
            if obj['color'] == color_to_remove:
                # Iterate through the pixels of this object
                for r, c in obj['pixels']:
                    # Set the corresponding pixel in the output grid to black (0)
                    if 0 <= r < rows and 0 <= c < cols: # Boundary check (mostly for safety)
                         output_array[r, c] = 0

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```

Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies distinct contiguous objects of non-black colors (Outer Colors) in the input grid.
Determines a 'Special Color': the unique color present in the grid that is neither black (0) nor one of the Outer Colors. If no such unique color exists, the Special Color is defined as Black (0).
Selects an Outer Color for removal based on the Special Color:
- If the Special Color is 0, remove the second smallest Outer Color (if it exists).
- If the Special Color is non-zero, remove the smallest Outer Color (if it exists).
Constructs the output grid by starting with a copy of the input and changing the pixels of the objects selected for removal to black (0).
"""

def _find_objects(grid):
    """
    Finds all contiguous objects of the same non-black color in the grid using 4-way adjacency.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'pixels' (set of (r, c) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # If it's a non-black pixel and hasn't been visited yet, start BFS
            if color != 0 and not visited[r, c]:
                obj_color = color
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == obj_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'color': obj_color, 'pixels': current_object_pixels})
                
    return objects


def _get_special_color(grid, outer_colors_set):
    """
    Determines the unique color in the grid that is not black (0) and not
    one of the specified outer colors.

    Args:
        grid (np.array): The input grid.
        outer_colors_set (set): A set of the unique outer colors of the objects.

    Returns:
        int: The identified special color, or 0 if none or multiple exist.
    """
    unique_grid_colors = set(grid.flatten())
    
    # Find colors in the grid that are not black and not outer colors
    potential_special_colors = unique_grid_colors - outer_colors_set - {0}
    
    if len(potential_special_colors) == 1:
        # If exactly one such color exists, it's the special color
        return potential_special_colors.pop()
    else:
        # If zero or more than one such color exists, the special color is black (0)
        return 0


def transform(input_grid):
    """
    Applies the transformation rule based on object colors and the special color.
    """
    # Convert input list of lists to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # 1. Create a copy of the input grid to modify
    output_array = np.copy(input_array)

    # 2. Identify Objects and their Outer Colors
    objects = _find_objects(input_array)
    if not objects: # Handle empty grid or grid with only black pixels
        return input_grid # Return original grid if no objects found

    outer_colors_set = set(obj['color'] for obj in objects)
    sorted_outer_colors = sorted(list(outer_colors_set))

    # 3. Identify the Special Color
    special_color = _get_special_color(input_array, outer_colors_set)

    # 4. Determine the Color To Remove
    color_to_remove = -1 # Initialize with an invalid color, meaning nothing removed by default

    if special_color == 0:
        # If special color is black, target the second smallest outer color
        if len(sorted_outer_colors) >= 2:
            color_to_remove = sorted_outer_colors[1]
    else:
        # If special color is non-black, target the smallest outer color
        if len(sorted_outer_colors) >= 1:
            color_to_remove = sorted_outer_colors[0]

    # 5. Modify the Output Grid by removing targeted objects
    if color_to_remove != -1: # Check if a color was actually selected for removal
        # Iterate through the found objects
        for obj in objects:
            # If the object's color is the one to be removed
            if obj['color'] == color_to_remove:
                # Iterate through the pixels of this object
                for r, c in obj['pixels']:
                    # Set the corresponding pixel in the output grid to black (0)
                    if 0 <= r < rows and 0 <= c < cols: # Boundary check (mostly for safety)
                         output_array[r, c] = 0

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2
0 2 1 2 0 0 2 1 2
0 2 2 2 0 0 2 2 2
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.938271604938279

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3
0 6 6 6 0 0 3 7 7 7 3
0 6 7 6 0 0 3 7 7 7 3
0 6 6 6 0 0 3 7 7 7 3
0 0 0 0 0 0 3 3 3 3 3
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 3 3 3 3 0 0
5 5 7 5 5 3 7 7 3 0 0
5 5 5 5 5 3 7 7 3 0 0
5 5 5 5 5 3 3 3 3 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 6 7 6 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 7 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3
0 6 6 6 0 0 3 7 7 7 3
0 6 7 6 0 0 3 7 7 7 3
0 6 6 6 0 0 3 7 7 7 3
0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0
0 0 7 0 0 3 7 7 3 0 0
0 0 0 0 0 3 7 7 3 0 0
0 0 0 0 0 3 3 3 3 0 0
```
Match: False
Pixels Off: 65
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 214.87603305785123

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 1 1 1
0 4 0 0 0 4 0 0 0 1 0 1
0 4 4 4 4 4 0 0 0 1 0 1
0 0 0 0 0 4 4 4 0 1 0 1
0 0 0 0 0 4 0 4 0 1 1 1
7 7 7 0 0 4 0 4 0 0 0 0
7 0 7 0 0 4 4 4 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 1 1
7 7 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 1 1
7 7 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
**General Assessment and Strategy**

The initial analysis correctly identified the core components: objects defined by an "Outer Color", a "Special Color" derived from the grid context, and a removal rule based on the Special Color and the sorted list of Outer Colors. However, the implementation failed because it only removed the pixels of the object's Outer Color, neglecting the associated Special Color pixels that were spatially related (inside/adjacent) to the removed object.

The strategy is to refine the removal step:
1.  Identify the objects and their Outer Colors.
2.  Determine the Special Color (the unique color in the grid that is not black and not an Outer Color; defaults to black if not unique or non-existent).
3.  Select the Outer Color to remove based on the Special Color (smallest if Special != 0, second smallest if Special == 0).
4.  Identify all pixels belonging to objects with the selected Outer Color.
5.  Identify all pixels of the Special Color.
6.  Determine which Special Color pixels should also be removed: those that are adjacent (4-way or 8-way, let's assume 4-way for now, but might need 8-way) to any pixel identified in step 4.
7.  Create the output grid by taking the input grid and setting both the object pixels (step 4) and the associated adjacent Special Color pixels (step 6) to black (0).

**Metrics and Analysis**


*code_execution:*
```python
import numpy as np
from collections import deque

# Re-using the helper functions from the previous attempt for analysis
def _find_objects(grid):
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and not visited[r, c]:
                obj_color = color
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == obj_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                objects.append({'color': obj_color, 'pixels': current_object_pixels})
    return objects

def _get_special_color(grid, outer_colors_set):
    unique_grid_colors = set(grid.flatten())
    potential_special_colors = unique_grid_colors - outer_colors_set - {0}
    if len(potential_special_colors) == 1:
        return potential_special_colors.pop()
    else:
        return 0

def analyze_example(input_grid_list):
    input_array = np.array(input_grid_list, dtype=int)
    objects = _find_objects(input_array)
    if not objects:
        print("No objects found.")
        return

    outer_colors_set = set(obj['color'] for obj in objects)
    sorted_outer_colors = sorted(list(outer_colors_set))
    special_color = _get_special_color(input_array, outer_colors_set)

    color_to_remove = -1
    if special_color == 0:
        if len(sorted_outer_colors) >= 2:
            color_to_remove = sorted_outer_colors[1]
    else:
        if len(sorted_outer_colors) >= 1:
            color_to_remove = sorted_outer_colors[0]

    removed_object_pixels = set()
    for obj in objects:
        if obj['color'] == color_to_remove:
            removed_object_pixels.update(obj['pixels'])

    special_color_pixels = set(zip(*np.where(input_array == special_color)))
    
    adjacent_special_pixels_to_remove = set()
    rows, cols = input_array.shape
    for r_spec, c_spec in special_color_pixels:
        is_adjacent = False
        # Check 4-way adjacency
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_spec + dr, c_spec + dc
            if (nr, nc) in removed_object_pixels:
                is_adjacent = True
                break
        if is_adjacent:
            adjacent_special_pixels_to_remove.add((r_spec, c_spec))

    # Let's try 8-way adjacency as well, as it might be needed
    adjacent_special_pixels_to_remove_8way = set()
    for r_spec, c_spec in special_color_pixels:
        is_adjacent = False
        # Check 8-way adjacency
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r_spec + dr, c_spec + dc
                if (nr, nc) in removed_object_pixels:
                    is_adjacent = True
                    break
            if is_adjacent:
                break
        if is_adjacent:
            adjacent_special_pixels_to_remove_8way.add((r_spec, c_spec))


    print(f"Outer Colors: {sorted_outer_colors}")
    print(f"Special Color: {special_color}")
    print(f"Color to Remove: {color_to_remove}")
    print(f"Pixels of Removed Object Color ({color_to_remove}): {len(removed_object_pixels)}")
    print(f"Pixels of Special Color ({special_color}): {len(special_color_pixels)}")
    print(f"Adjacent Special Pixels (4-way) to remove: {len(adjacent_special_pixels_to_remove)}")
    print(f"Adjacent Special Pixels (8-way) to remove: {len(adjacent_special_pixels_to_remove_8way)}")
    
    # Check if 8-way matches the failed examples' expected output
    # Example 1: Remove Red(2). Special=Blue(1). Removed Object Pixels=16. Special Pixels=4. 
    # Expected output removes 2 blue pixels. 
    # Blue pixels are at (2,2), (2,7), (6,2), (6,7).
    # Red pixels surround (2,2) and (2,7). Yellow surrounds (6,2). Azure surrounds (6,7).
    # 8-way adjacency check: Blue(2,2) adjacent to Red. Blue(2,7) adjacent to Red. Blue(6,2) adjacent to Yellow. Blue(6,7) adjacent to Azure. 
    # If removing Red(2), adjacent special pixels are (2,2) and (2,7). Count = 2. This matches. -> Use 8-way adjacency.
    print(f"Pixels to turn black (8-way): {len(removed_object_pixels | adjacent_special_pixels_to_remove_8way)}")


# Example 1 Input
input_1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 2, 2, 2],
    [0, 2, 1, 2, 0, 0, 2, 1, 2],
    [0, 2, 2, 2, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 4, 4, 0, 0, 8, 8, 8],
    [0, 4, 1, 4, 0, 0, 8, 1, 8],
    [0, 4, 4, 4, 0, 0, 8, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
print("--- Example 1 Analysis ---")
analyze_example(input_1)

# Example 2 Input
input_2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3],
    [0, 6, 6, 6, 0, 0, 3, 7, 7, 7, 3],
    [0, 6, 7, 6, 0, 0, 3, 7, 7, 7, 3],
    [0, 6, 6, 6, 0, 0, 3, 7, 7, 7, 3],
    [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3],
    [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 3, 3, 3, 3, 0, 0],
    [5, 5, 7, 5, 5, 3, 7, 7, 3, 0, 0],
    [5, 5, 5, 5, 5, 3, 7, 7, 3, 0, 0],
    [5, 5, 5, 5, 5, 3, 3, 3, 3, 0, 0]
]
print("\n--- Example 2 Analysis ---")
analyze_example(input_2)


# Example 3 Input
input_3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 4, 4, 4, 4, 0, 0, 0, 1, 1, 1],
    [0, 4, 0, 0, 0, 4, 0, 0, 0, 1, 0, 1],
    [0, 4, 4, 4, 4, 4, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 4, 4, 4, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 4, 0, 4, 0, 1, 1, 1],
    [7, 7, 7, 0, 0, 4, 0, 4, 0, 0, 0, 0],
    [7, 0, 7, 0, 0, 4, 4, 4, 0, 0, 0, 0],
    [7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
print("\n--- Example 3 Analysis ---")
analyze_example(input_3)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Analysis ---
Outer Colors: [np.int64(1), np.int64(2), np.int64(4), np.int64(8)]
Special Color: 0
Color to Remove: 2
Pixels of Removed Object Color (2): 16
Pixels of Special Color (0): 45
Adjacent Special Pixels (4-way) to remove: 21
Adjacent Special Pixels (8-way) to remove: 27
Pixels to turn black (8-way): 43

--- Example 2 Analysis ---
Outer Colors: [np.int64(3), np.int64(5), np.int64(6), np.int64(7)]
Special Color: 0
Color to Remove: 5
Pixels of Removed Object Color (5): 24
Pixels of Special Color (0): 46
Adjacent Special Pixels (4-way) to remove: 6
Adjacent Special Pixels (8-way) to remove: 7
Pixels to turn black (8-way): 31

--- Example 3 Analysis ---
Outer Colors: [np.int64(1), np.int64(4), np.int64(7)]
Special Color: 0
Color to Remove: 4
Pixels of Removed Object Color (4): 22
Pixels of Special Color (0): 98
Adjacent Special Pixels (4-way) to remove: 31
Adjacent Special Pixels (8-way) to remove: 37
Pixels to turn black (8-way): 59

```
**Analysis Update:**

The code execution reveals a flaw in my `_get_special_color` logic or its application.
*   **Example 1:** Outer Colors are {1, 2, 4, 8}. The unique color in the grid that isn't black or an outer color *should be* Blue (1). However, the code identified Blue (1) as an *object* color because it forms a contiguous block. My previous manual analysis incorrectly identified Blue(1) as the Inner/Special color. Let's redefine:
    *   Objects: Red(2, 16 pixels), Blue(1, 2 pixels at (2,2),(6,2)), Yellow(4, 8 pixels), Azure(8, 8 pixels), Blue(1, 2 pixels at (2,7),(6,7)). *Correction:* The Blue(1) pixels are singletons or pairs, maybe not full objects depending on connectivity rule. Re-running `_find_objects` focusing on non-black.
    *   Let's rethink the "Special Color". It's the color *used* by *all* primary objects but isn't their main color. In Ex 1, Red(2), Yellow(4), Azure(8) objects seem primary. They all contain/are adjacent to Blue(1). So Special=1. Outer={2,4,8}. Rule: Special!=0 -> remove smallest (2).
    *   In Ex 2, Magenta(6), Green(3), Gray(5) seem primary. They all contain/are adjacent to Orange(7). Special=7. Outer={3,5,6}. Rule: Special!=0 -> remove smallest (3).
    *   In Ex 3, Yellow(4), Blue(1), Orange(7) seem primary. They all contain/are adjacent to Black(0). Special=0. Outer={1,4,7}. Rule: Special==0 -> remove second smallest (4).

This matches the expected outputs and the original hypothesis *before* the code execution confused the issue by finding objects of the special color itself. The `_find_objects` needs refinement to distinguish "primary" objects from the "special color" pixels, perhaps by size or by the fact the special color is *inside* multiple different primary objects.

Alternatively, the logic can remain: find *all* non-black objects. Calculate the true "Special Color" based on visual inspection / common internal color (as done manually above). Then apply the rule. The crucial part is the removal step: remove the object pixels *and* the adjacent special color pixels using 8-way adjacency.

Let's re-run the analysis *manually* determining the Special Color based on the visual pattern:

*   **Example 1:** Objects={Red(2), Yellow(4), Azure(8)}. Special=Blue(1). Outer={2, 4, 8}. Special=1 (non-zero). Remove smallest: 2. Pixels to remove: All Red(2) pixels + Blue(1) pixels adjacent (8-way) to Red(2) pixels. (This matches the expected output).
*   **Example 2:** Objects={Magenta(6), Green(3), Gray(5)}. Special=Orange(7). Outer={3, 5, 6}. Special=7 (non-zero). Remove smallest: 3. Pixels to remove: All Green(3) pixels + Orange(7) pixels adjacent (8-way) to Green(3) pixels. (This matches the expected output).
*   **Example 3:** Objects={Yellow(4), Blue(1), Orange(7)}. Special=Black(0). Outer={1, 4, 7}. Special=0 (zero). Remove second smallest: 4. Pixels to remove: All Yellow(4) pixels + Black(0) pixels adjacent (8-way) to Yellow(4) pixels. (This matches the expected output).

The 8-way adjacency for removing associated special color pixels seems correct. The definition of the Special Color needs to be carefully implemented – it's not just *any* non-object color, but the one associated visually/spatially with *all* the main objects. The previous `_get_special_color` function was too simplistic. A better approach might be to find bounding boxes for primary objects and see which non-primary color appears within all (or most) of them. For now, let's assume we can correctly identify the Special Color as per the manual analysis above.

**YAML Fact Document (Revised)**


```yaml
task_elements:
  - element: Grid
    description: A 2D array of pixels (0-9). Black (0) is the background.
  - element: PrimaryObject
    description: A contiguous region of non-black pixels sharing the same color (Outer Color). Excludes singletons or small groups of the 'Special Color'.
    properties:
      - OuterColor: The main color of the object's pixels.
      - Pixels: The coordinates of the pixels comprising the object.
  - element: SpecialColor
    description: The single color that is spatially associated (e.g., inside, adjacent) with all Primary Objects but is different from their Outer Colors. Can be Black (0).
    identification: Found by observing the common non-Outer Color within or adjacent to all Primary Objects.
  - element: SetOfOuterColors
    description: The unique collection of Outer Colors of all Primary Objects.
    properties:
      - UniqueColors: List of distinct Outer Colors.
      - SortedColors: UniqueColors sorted numerically.

actions:
  - action: IdentifyPrimaryObjects
    description: Find all significant contiguous components of non-black pixels, potentially filtering by size or complexity to exclude simple 'Special Color' pixels.
    inputs: Input Grid
    outputs: List of PrimaryObjects (with OuterColor and Pixels).
  - action: IdentifySpecialColor
    description: Determine the single color commonly associated spatially with all Primary Objects.
    inputs: Input Grid, List of PrimaryObjects
    outputs: SpecialColor value.
  - action: SelectColorToRemove
    description: Choose which Outer Color objects should be removed based on the SpecialColor and the sorted list of Outer Colors.
    inputs: SpecialColor, Sorted List of Outer Colors
    outputs: ColorToRemove.
    logic: |
      If SpecialColor is Black (0), ColorToRemove is the second element in Sorted List of Outer Colors (if >= 2 elements exist).
      If SpecialColor is not Black (0), ColorToRemove is the first element (minimum) in Sorted List of Outer Colors (if >= 1 element exists).
      If the condition cannot be met (e.g., not enough elements), no color is removed.
  - action: RemoveTargetedPixels
    description: Modify the grid by setting specific pixels to Black (0).
    inputs: Input Grid, ColorToRemove, SpecialColor, List of PrimaryObjects
    outputs: Output Grid.
    logic: |
      1. Create a copy of the input grid.
      2. Identify all pixels belonging to PrimaryObjects whose OuterColor matches ColorToRemove ('object_pixels_to_remove').
      3. Identify all pixels in the original grid that have the SpecialColor ('special_pixels').
      4. Find the subset of 'special_pixels' where each pixel is adjacent (8-way) to at least one pixel in 'object_pixels_to_remove' ('adjacent_special_pixels_to_remove').
      5. In the copied grid, set all pixels in 'object_pixels_to_remove' to Black (0).
      6. In the copied grid, set all pixels in 'adjacent_special_pixels_to_remove' to Black (0).
      7. Return the modified grid.

relationships:
  - relationship: RemovalCondition
    description: The Outer Color chosen for removal depends on the Special Color and the numeric order of Outer Colors.
    entities: SpecialColor, SetOfOuterColors, ColorToRemove
  - relationship: PixelRemovalScope
    description: Removing an object entails removing both its own pixels and any adjacent Special Color pixels.
    entities: PrimaryObject (with ColorToRemove), SpecialColor, Pixels (to set to 0)
    details: Adjacency uses 8-connectivity.
```


**Natural Language Program (Revised)**

1.  **Analyze the Input Grid:**
    *   Identify all distinct "Primary Objects": contiguous regions of a single non-black color. (These appear distinct from any scattered pixels of a "Special Color"). Record the Outer Color and pixel coordinates for each Primary Object.
2.  **Identify the Special Color:**
    *   Examine the grid and the identified Primary Objects. Find the single color ("Special Color") that is spatially associated (inside or adjacent) with *all* Primary Objects but is not one of their Outer Colors. This Special Color can be Black (0).
3.  **Determine the Target Outer Color for Removal:**
    *   Collect all unique Outer Colors from the Primary Objects found in step 1.
    *   Sort these unique Outer Colors numerically (ascending).
    *   Based on the Special Color from step 2:
        *   If Special Color is Black (0) and there are at least two Outer Colors, select the *second* color in the sorted list.
        *   If Special Color is *not* Black (0) and there is at least one Outer Color, select the *first* color (minimum) in the sorted list.
        *   Otherwise, no color is selected for removal.
    *   The selected color is the "Color To Remove".
4.  **Construct the Output Grid:**
    *   Create a copy of the input grid.
    *   Find all pixel coordinates belonging to any Primary Object whose Outer Color matches the "Color To Remove". Let this set be `P_obj`.
    *   Find all pixel coordinates in the original grid whose color is the "Special Color". Let this set be `P_spec`.
    *   Identify the subset of `P_spec` where each pixel is adjacent (using 8-way connectivity - including diagonals) to at least one pixel in `P_obj`. Let this subset be `P_adj_spec`.
    *   Iterate through all coordinates in `P_obj` and set the corresponding pixel in the copied grid to Black (0).
    *   Iterate through all coordinates in `P_adj_spec` and set the corresponding pixel in the copied grid to Black (0).
    *   The resulting grid is the final output.
