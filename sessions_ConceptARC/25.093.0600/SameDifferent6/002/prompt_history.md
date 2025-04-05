
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

Okay, let's analyze the task based on the provided examples.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are grids of digits. The digit '0' consistently represents the background.
2.  **Objects:** The non-zero digits form distinct connected components or "objects" separated by the background '0'. These objects can be composed of one or more different non-zero digits (e.g., train_1 has an object made of 4s and 8s).
3.  **Transformation:** The transformation involves selectively removing entire objects from the input grid. Objects identified for removal are completely replaced with the background color '0'. Some objects remain unchanged.
4.  **Selection Criteria:** The key determinant for whether an object is removed seems to be the presence of a specific "target removal color" within that object. If an object contains *any* instance of this specific color, the entire object is removed. This target removal color varies across the training examples (2 in train_1, 3 in train_2, 4 in train_3).

**YAML Fact Documentation:**


```yaml
task_elements:
  - element: Grid
    properties:
      - type: 2D array of integers
      - background_color: 0
  - element: Object
    properties:
      - definition: A connected component of non-zero cells in the grid (using 4-way or 8-way connectivity, typically 8-way in ARC).
      - composition: Can be composed of one or more distinct non-zero colors (digits).
      - location: Occupies a specific set of coordinates within the grid.
  - element: Target Removal Color
    properties:
      - definition: A specific non-zero color C.
      - role: Determines which objects are removed.
      - identification: Found by observing which color C, when present in an input object, leads to that object's complete removal in the output, while objects lacking color C remain.
relationships:
  - relationship: Object Membership
    involved_elements: [Grid, Object]
    description: Objects are subsets of cells within the Grid.
  - relationship: Color Presence
    involved_elements: [Object, Target Removal Color]
    description: An object either contains the Target Removal Color or it does not.
actions:
  - action: Identify Objects
    input: Input Grid
    output: Set of Objects (each defined by its constituent cells and colors)
    description: Use connectivity analysis (e.g., flood fill or similar) on non-zero cells to find distinct components.
  - action: Determine Target Removal Color
    input: Input Grid, Output Grid
    output: Target Removal Color C
    description: Find a non-zero color C present in some input objects such that all objects containing C are absent (replaced by 0) in the output, while at least one object not containing C persists.
  - action: Filter Objects
    input: Set of Objects, Target Removal Color C
    output: Set of Objects to Keep
    description: Select objects that do *not* contain the Target Removal Color C.
  - action: Generate Output Grid
    input: Input Grid Dimensions, Set of Objects to Keep, Background Color (0)
    output: Output Grid
    description: Create a new grid filled with the background color, then draw the cells of the "Objects to Keep" onto it using their original colors and positions.
```


**Natural Language Program:**

1.  **Analyze** the input and output grids to determine the single "target removal color" (let's call it `C`). `C` is a non-zero color found in the input such that every distinct connected non-zero object containing *any* cell with color `C` is entirely replaced by the background color (0) in the output, while at least one object *not* containing `C` remains in the output.
2.  **Identify** all distinct connected components (objects) of non-zero cells in the input grid. Record the set of cells belonging to each object.
3.  **Filter** these objects: For each identified object, check if any of its constituent cells have the color `C`. Keep only those objects that do *not* contain any cell with color `C`.
4.  **Construct** the output grid: Start with a grid of the same dimensions as the input, filled entirely with the background color (0). For each object that was kept in the filtering step, copy the colors of its constituent cells from the input grid to the corresponding positions in the output grid.
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transformation Rule:

1.  Identify all unique non-zero colors present in the input grid.
2.  Determine the "target removal color" (C). This color is the smallest non-zero color present in the grid, excluding the color 1. If only color 1 and 0 are present, or only 0 is present, no removal occurs.
3.  Identify all distinct connected components (objects) of non-zero cells in the input grid using 8-way connectivity.
4.  For each object, check if any of its constituent cells have the color C.
5.  Construct the output grid, initially filled with the background color (0).
6.  Copy only those objects from the input grid to the output grid that do *not* contain the target removal color C. Objects containing C are effectively removed (left as background).
"""

def find_connected_objects(grid):
    """
    Finds connected components of non-zero cells in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list where each element represents an object.
              Each object is itself a list of tuples (row, col, color).
    """
    # Define connectivity: 8-way connectivity
    structure = np.array([[1,1,1],
                          [1,1,1],
                          [1,1,1]], dtype=bool)

    # Label connected components of non-zero cells
    labeled_grid, num_labels = label(grid > 0, structure=structure)

    objects = []
    # Extract coordinates and colors for each labeled component
    object_slices = find_objects(labeled_grid)
    for i in range(num_labels):
        obj_slice = object_slices[i]
        obj_coords = np.argwhere(labeled_grid[obj_slice] == (i + 1))
        obj_cells = []
        for coord in obj_coords:
            # Adjust coordinates back to original grid space
            r, c = coord[0] + obj_slice[0].start, coord[1] + obj_slice[1].start
            color = grid[r, c]
            obj_cells.append((r, c, color))
        if obj_cells:
            objects.append(obj_cells)
            
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.zeros_like(input_array)
    
    # 1. Identify unique non-zero colors
    unique_colors = np.unique(input_array)
    non_zero_colors = unique_colors[unique_colors != 0]

    # 2. Determine the target removal color (C)
    # Smallest non-zero color, excluding 1
    candidate_colors = non_zero_colors[non_zero_colors != 1]
    target_removal_color = None
    if candidate_colors.size > 0:
        target_removal_color = np.min(candidate_colors)

    # If no target color found (e.g., only 0s or 1s present), no removal needed
    if target_removal_color is None:
        return input_grid # Return original grid if no removal target

    # 3. Identify all connected non-zero objects
    objects = find_connected_objects(input_array)

    # 4 & 6. Filter objects and construct output grid
    for obj in objects:
        # Check if the object contains the target removal color
        contains_target = False
        for r, c, color in obj:
            if color == target_removal_color:
                contains_target = True
                break
        
        # If the object does NOT contain the target color, copy it to the output
        if not contains_target:
            for r, c, color in obj:
                output_array[r, c] = color

    # Convert back to list of lists for the required output format
    output_grid = output_array.tolist()
    return output_grid
```
