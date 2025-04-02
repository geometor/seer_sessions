
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
