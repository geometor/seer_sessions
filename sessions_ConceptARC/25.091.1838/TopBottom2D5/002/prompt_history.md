
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 1 1 1 0 2 0 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 7 7 7 0
0 3 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0
4 4 4 0 0 0 8 8 8 0
3 3 3 0 0 0 8 0 8 0
3 0 3 0 0 0 8 8 8 0
3 3 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of Elements:**

1.  **Grid Structure:** Both input and output are 2D grids of pixels with different colors. The background is consistently white (0).
2.  **Objects:** The input grids contain multiple distinct "objects," which are contiguous areas of non-white pixels. These objects have different shapes (like 'L', 'T', 'H', 'C') and colors.
3.  **Transformation:** The transformation involves selecting certain objects from the input grid and discarding others. The selected objects retain their original shape, color, and position in the output grid. The discarded objects are replaced by the white background color.
4.  **Selection Criterion:** By comparing the input and output across the examples, the key factor determining which object(s) are kept seems to be their vertical position. Specifically, the object(s) that start at the lowest row index (i.e., are closest to the bottom of the grid) are preserved. If multiple objects share the same lowest starting row index, all of them are kept.

**Facts:**


```yaml
elements:
  - type: grid
    properties:
      - background_color: white (0)
  - type: object
    properties:
      - composed_of: contiguous non-white pixels
      - has: color (non-white)
      - has: shape
      - has: position (defined by pixel coordinates)
      - has: bounding_box
      - derived_property: top_row_index (minimum row index of any pixel in the object)
relationships:
  - description: Multiple objects can exist within a single input grid.
  - description: Objects are distinguished by color and spatial separation.
actions:
  - action: identify_objects
    input: input grid
    output: set of distinct non-white objects
  - action: calculate_top_row
    input: object
    output: minimum row index for that object
  - action: find_lowest_starting_row
    input: set of top_row_indices for all objects
    output: maximum value among the top_row_indices
  - action: filter_objects
    input: set of objects, lowest_starting_row value
    output: subset of objects whose top_row_index equals the lowest_starting_row value
  - action: construct_output
    input: input grid dimensions, filtered objects
    output: output grid (white background with filtered objects placed in their original positions)
transformation:
  - description: Selects and keeps only the object(s) whose top-most pixel(s) are located at the lowest row index compared to all other objects in the input grid. All other objects are removed.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, but filled entirely with the background color (white).
2.  Identify all distinct connected components (objects) of non-white pixels in the input grid.
3.  If no non-white objects are found, return the empty output grid.
4.  For each identified object, determine its minimum row index (the row index of its highest pixel).
5.  Find the maximum value among these minimum row indices calculated in the previous step. This value represents the lowest starting row achieved by any object(s). Let's call this `lowest_start_row`.
6.  Iterate through all the identified objects again.
7.  If an object's minimum row index is equal to `lowest_start_row`, copy all pixels belonging to this object from the input grid to their corresponding positions in the output grid.
8.  Return the final output grid.
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Identifies all distinct non-background objects in the input grid. 
Determines the top-most row index for each object. 
Finds the maximum of these top-most row indices (representing the lowest starting position on the grid).
Constructs an output grid containing only the object(s) whose top-most row index matches this maximum value, preserving their original colors and positions.
"""

def find_all_objects(grid):
    """
    Finds all connected components of non-background colors.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A labeled array where each object has a unique integer ID, 
               and the number of features (objects) found. Returns (None, 0) if no objects.
    """
    background_color = 0
    data = grid != background_color # Mask of non-background pixels
    labeled_array, num_features = label(data)
    if num_features == 0:
        return None, 0
    return labeled_array, num_features

def get_object_properties(labeled_array, num_features):
    """
    Calculates properties like bounding box slices and top row index for each object.

    Args:
        labeled_array (np.array): The array with labeled objects.
        num_features (int): The number of objects found.

    Returns:
        list: A list of dictionaries, each containing 'id', 'slices', and 'top_row' for an object.
              Returns an empty list if num_features is 0.
    """
    if num_features == 0 or labeled_array is None:
        return []
        
    object_slices = find_objects(labeled_array)
    properties = []
    for i in range(num_features):
        obj_id = i + 1
        slices = object_slices[i]
        # Calculate the actual minimum row index within the bounding box for this specific object
        obj_mask = labeled_array == obj_id
        rows, _ = np.where(obj_mask)
        min_row = np.min(rows) # This is the true top row of the object pixels
        
        properties.append({
            'id': obj_id,
            'slices': slices,
            'top_row': min_row # Use the actual minimum row of the object's pixels
        })
    return properties

def transform(input_grid):
    """
    Filters the input grid to keep only the object(s) starting at the lowest row index.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    # Initialize output_grid with the background color
    output_grid = np.zeros_like(input_grid)
    background_color = 0 # Assuming 0 is the standard background

    # Find all distinct objects (connected components of non-background colors)
    labeled_array, num_features = find_all_objects(input_grid)

    # If no objects are found, return the empty grid
    if num_features == 0:
        return output_grid

    # Get properties (including top row) for each object
    object_props = get_object_properties(labeled_array, num_features)

    # Find the lowest starting row index among all objects
    # The top row index is the minimum row index for an object's pixels.
    # We want the object(s) whose top row index is the largest (closest to the bottom).
    lowest_start_row = -1
    for prop in object_props:
        if prop['top_row'] > lowest_start_row:
            lowest_start_row = prop['top_row']

    # Identify objects that start at the lowest row
    objects_to_keep_ids = [prop['id'] for prop in object_props if prop['top_row'] == lowest_start_row]

    # Construct the output grid by copying only the selected objects
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            label_id = labeled_array[r, c]
            if label_id in objects_to_keep_ids:
                output_grid[r, c] = input_grid[r, c]

    return output_grid
```
