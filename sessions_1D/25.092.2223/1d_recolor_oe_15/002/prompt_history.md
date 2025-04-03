
## train_1

**input:**
```
0 0 3 3 3 3 0 0 0 3 3 3 3 3 0 0 3 0 3 3 3 3 0 0 0
```


**output:**
```
0 0 1 1 1 1 0 0 0 5 5 5 5 5 0 0 5 0 1 1 1 1 0 0 0
```


## train_2

**input:**
```
0 0 0 3 3 0 0 0 3 3 3 3 3 0 0 3 0 0 3 3 3 0 0 0 0
```


**output:**
```
0 0 0 1 1 0 0 0 5 5 5 5 5 0 0 5 0 0 5 5 5 0 0 0 0
```


## train_3

**input:**
```
0 0 0 3 3 3 3 3 3 0 0 0 3 3 3 0 0 3 3 0 0 3 3 3 3
```


**output:**
```
0 0 0 1 1 1 1 1 1 0 0 0 5 5 5 0 0 1 1 0 0 1 1 1 1
```

Okay, I will analyze the provided examples to understand the transformation task.

## Perception

1.  **Input/Output Structure:** The input and output are grids of the same dimensions. The background color is consistently white (0).
2.  **Color Transformation:** The primary transformation involves changing green (3) pixels in the input to either blue (1) or gray (5) pixels in the output. All other pixels (white background) remain unchanged.
3.  **Object Identification:** The green pixels in the input form distinct connected components (objects). These objects appear to be processed independently.
4.  **Shape Dependency:** The final color (blue or gray) seems to depend on the shape properties of the green objects or their constituent parts.
5.  **Rule 1: Solid Rectangles:** Connected components of green pixels that form a solid rectangle (where the number of green pixels equals the area of their bounding box) are consistently transformed into blue (1) pixels.
6.  **Rule 2: Non-Rectangular Shapes:** For connected green components that are *not* solid rectangles, the transformation depends on the horizontal segments within them.
    *   Maximal horizontal segments of green pixels are identified within these non-rectangular shapes.
    *   Segments with a length of exactly 2 or exactly 4 are transformed into blue (1) pixels.
    *   Segments with any other length (e.g., 1, 3, 5) are transformed into gray (5) pixels.

## YAML Facts


```yaml
Task: Color transformation based on shape properties of green objects.

Input_Grid:
  - Contains_Pixels: [0, 3] # white, green
  - Background_Color: 0 # white

Output_Grid:
  - Contains_Pixels: [0, 1, 5] # white, blue, gray
  - Background_Color: 0 # white
  - Derived_From: Input_Grid

Objects:
  - Type: Connected Components
  - Color: 3 # green
  - Properties:
      - Bounding_Box: Calculated for each component.
      - Size: Number of pixels in the component.
      - Is_Solid_Rectangle: True if Size == (Bounding_Box.height * Bounding_Box.width), False otherwise.
      - Horizontal_Segments: List of contiguous horizontal runs of green pixels within the component.
        - Properties:
            - Length: Number of pixels in the segment.

Transformation_Rules:
  - Rule_1:
      - Applies_To: Green objects where Is_Solid_Rectangle is True.
      - Action: Recolor all pixels of the object to 1 (blue).
  - Rule_2:
      - Applies_To: Green objects where Is_Solid_Rectangle is False.
      - Action: Process each Horizontal_Segment within the object.
        - If Segment.Length is 2 or Segment.Length is 4:
            - Recolor pixels of the segment to 1 (blue).
        - Else (Segment.Length is 1, 3, 5, etc.):
            - Recolor pixels of the segment to 5 (gray).

Relationships:
  - Pixel_Mapping: Each output pixel corresponds to the input pixel at the same coordinate.
  - Color_Mapping:
      - Input 0 -> Output 0
      - Input 3 -> Output 1 (if part of Rule_1 object, or specific segments in Rule_2 object)
      - Input 3 -> Output 5 (if part of Rule_2 object and segment length is not 2 or 4)
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Find all distinct connected components (objects) consisting of green (3) pixels in the input grid.
3.  For each green object found:
    a.  Determine if the object forms a solid rectangle (i.e., its pixel count equals the area of its bounding box).
    b.  **If the object is a solid rectangle:** Change the color of all pixels belonging to this object in the output grid to blue (1).
    c.  **If the object is not a solid rectangle:**
        i.  Identify all maximal horizontal segments of green pixels within this object.
        ii. For each horizontal segment:
            *   Calculate the length of the segment.
            *   If the length is exactly 2 or exactly 4, change the color of the pixels belonging to this segment in the output grid to blue (1).
            *   Otherwise (if the length is 1, 3, 5, or any other value not equal to 2 or 4), change the color of the pixels belonging to this segment in the output grid to gray (5).
4.  Return the modified output grid.
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms a grid by analyzing connected components of green (3) pixels.

1. Find all distinct connected components (objects) of green (3) pixels.
2. For each green object:
   a. Check if it forms a solid rectangle (pixel count equals bounding box area).
   b. If it's a solid rectangle, change all its pixels to blue (1) in the output.
   c. If it's not a solid rectangle:
      i. Find all maximal horizontal segments of green pixels within the object.
      ii. For each segment:
         - If its length is 2 or 4, change its pixels to blue (1) in the output.
         - Otherwise, change its pixels to gray (5) in the output.
3. Keep all other pixels (background white 0) unchanged.
"""

def find_connected_components(grid, color):
    """
    Finds connected components of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the components to find.

    Returns:
        list: A list of lists, where each inner list contains the
              coordinates (row, col) of the pixels belonging to one component.
              Returns an empty list if no components are found.
    """
    binary_grid = (grid == color).astype(int)
    labeled_grid, num_features = label(binary_grid)

    if num_features == 0:
        return []

    components = []
    # find_objects returns slices, need to convert to coordinates
    slices = find_objects(labeled_grid)
    for i in range(num_features):
        coords = []
        component_slice = slices[i]
        # Extract the subgrid corresponding to the labeled component
        subgrid = labeled_grid[component_slice]
        # Find coordinates within the subgrid where the label matches
        relative_coords = np.argwhere(subgrid == (i + 1))
        # Convert relative coordinates to absolute coordinates in the original grid
        for r, c in relative_coords:
            coords.append((component_slice[0].start + r, component_slice[1].start + c))
        if coords: # Ensure component is not empty (shouldn't happen with find_objects but good practice)
             components.append(coords)
             
    return components

def get_bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return min_r, min_c, max_r, max_c

def is_solid_rectangle(coords, bounding_box):
    """Checks if a component fills its bounding box."""
    if not coords or bounding_box is None:
        return False
    min_r, min_c, max_r, max_c = bounding_box
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return len(coords) == height * width

def find_horizontal_segments(coords):
    """Finds maximal horizontal segments within a set of coordinates."""
    if not coords:
        return []

    segments = []
    # Group coordinates by row
    coords_by_row = {}
    for r, c in coords:
        if r not in coords_by_row:
            coords_by_row[r] = []
        coords_by_row[r].append(c)

    # Find segments in each row
    for r, cols in coords_by_row.items():
        if not cols:
            continue
        cols.sort()
        current_segment = [(r, cols[0])]
        for i in range(1, len(cols)):
            # Check if the current column is adjacent to the previous one
            if cols[i] == cols[i-1] + 1:
                current_segment.append((r, cols[i]))
            else:
                # End of the current segment, start a new one
                segments.append(current_segment)
                current_segment = [(r, cols[i])]
        # Add the last segment
        segments.append(current_segment)

    return segments


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    target_color = 3 # green
    rect_color = 1 # blue
    seg_2_4_color = 1 # blue
    other_seg_color = 5 # gray

    # Find all green connected components
    green_components = find_connected_components(input_grid, target_color)

    # Process each component
    for component_coords in green_components:
        if not component_coords:
            continue

        # Calculate bounding box
        bbox = get_bounding_box(component_coords)

        # Check if it's a solid rectangle (Rule 1)
        if is_solid_rectangle(component_coords, bbox):
            for r, c in component_coords:
                output_grid[r, c] = rect_color
        else:
            # Not a solid rectangle, process horizontal segments (Rule 2)
            horizontal_segments = find_horizontal_segments(component_coords)
            for segment in horizontal_segments:
                segment_len = len(segment)
                # Determine the color based on segment length
                color_to_set = seg_2_4_color if segment_len == 2 or segment_len == 4 else other_seg_color
                # Apply the color to the pixels in the segment
                for r, c in segment:
                    output_grid[r, c] = color_to_set

    return output_grid.tolist() # Return as list of lists per ARC standard
```
