
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 7 7 7
8 8 8 8 8 8 8 8 8 7 7 7 7 7 7 8 8 2 2 2
8 8 8 8 8 8 8 8 8 0 0 0 7 0 7 8 8 7 7 7
8 8 8 8 8 8 8 8 8 0 7 0 0 0 7 8 8 7 7 7
8 7 7 7 7 7 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 7 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 7 0 7 0 0 8 8 8 8 8 8 8 8 8 7 7 7 8 8
8 7 7 7 7 7 8 8 8 8 8 8 8 8 8 2 2 7 8 8
8 7 2 7 2 2 8 8 8 8 8 8 8 8 8 7 2 7 8 8
8 7 2 2 2 7 8 8 8 8 8 8 8 8 8 7 7 7 4 8
8 7 7 7 7 7 8 8 8 8 8 8 8 8 8 8 8 4 4 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 7 7 7 7 7 7 7 7 7 7 7 8 8
8 8 8 8 8 8 8 7 0 0 0 0 0 0 0 7 0 7 8 8
8 8 8 8 8 8 8 7 0 7 0 0 0 7 0 0 0 7 8 8
8 8 8 8 8 8 8 7 7 7 7 7 7 7 7 7 7 7 8 8
8 8 8 8 8 8 8 7 2 7 2 2 2 2 2 2 2 7 8 8
8 8 8 8 8 8 8 7 2 2 2 7 7 7 7 7 2 7 8 8
8 8 8 8 8 8 8 7 7 7 7 7 7 7 7 7 7 7 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 4 4 8 8 8 9 9 3 8
8 4 3 3 3 8 3 3 3 8
8 8 3 9 9 8 3 3 3 8
8 8 3 9 9 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 3 3 3 8 8 3 9 9 8
8 9 9 3 8 8 3 9 3 8
8 9 9 3 8 8 3 3 3 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 3 3 3 3 3 3 8 8
8 8 3 9 9 9 9 3 8 8
8 8 3 9 9 9 9 3 8 8
8 8 3 9 9 9 9 3 8 8
8 8 3 9 3 3 3 3 8 8
8 8 3 3 3 3 3 3 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```

```yaml
perception:
  task_type: grid_transformation
  observations:
    - Input and output are 2D grids of single digits.
    - A background color (digit '8') fills most of the grid.
    - The input contains multiple disconnected regions (objects) composed of non-background colors.
    - The output grid contains only one non-background object, while the rest is filled with the background color.
    - The transformation identifies relevant objects in the input, combines or selects information from them, determines a bounding box for the output object, and populates this box based on the input objects and potentially fixed rules (like border colors).
  grid_properties:
    - dimensions: Vary between examples (12x20 for train_1, 10x10 for train_2). Output dimensions match input.
    - background_color: '8'
    - object_colors: Digits other than '8' (e.g., '0', '2', '3', '4', '7', '9').
  transformation_hints:
    - Selection: Input objects are filtered based on some criteria. In train_2, objects containing both '3' and '9' seem relevant. In train_1, the largest object or the one enclosed by '7's might be relevant.
    - Bounding_Box: The output object occupies a rectangular bounding box. In train_2, this box seems derived from the bounding box of the *centers* of the selected input objects. The method for train_1 is less clear.
    - Population: The output bounding box is filled. The border often has a specific color ('7' in train_1, '3' in train_2). The interior is filled based on the selected input objects, possibly involving default fills ('9' in train_2 interior) and overlays/copies from input objects relative to their centers.

facts:
  - input_grid: A 2D array of integers.
  - output_grid: A 2D array of integers with the same dimensions as the input.
  - background_color: Integer '8'.
  - objects:
      - definition: Contiguous regions of cells in the input_grid with values not equal to background_color.
      - properties:
          - colors_present: Set of unique non-background colors within the object.
          - bounding_box: Smallest rectangle enclosing the object.
          - center: Geometric center coordinates of the object's cells.
          - size: Number of cells in the object.
  - selection_criteria:
      - train_1: Seems related to size or enclosure (e.g., by color '7'). The largest object enclosed by '7's appears selected.
      - train_2: Objects containing both color '3' and color '9'.
  - output_object_definition:
      - location_and_size: Defined by a bounding box.
      - bounding_box_determination (hypothesis for train_2): Calculate the bounding box of the geometric centers of the selected input objects.
      - content:
          - border_color: A specific color ('7' for train_1, '3' for train_2).
          - interior_fill: Combination of default fill color ('9' for train_2) and colors copied/overlaid from selected input objects based on relative positions.

natural_language_program:
  - Identify all contiguous regions of non-background ('8') cells in the input grid (input objects).
  - Filter these input objects based on specific criteria relevant to the task example (e.g., for train_2, keep objects containing both '3' and '9'; for train_1, potentially select the largest object enclosed by '7's).
  - Calculate the geometric center for each selected input object.
  - Determine the bounding box enclosing all calculated centers. This defines the output object's bounding box.
  - Create the output grid, initially filled with the background color ('8').
  - Populate the determined bounding box in the output grid:
      - Set the cells forming the border of the bounding box to a specific color ('3' for train_2, '7' for train_1).
      - Fill the interior cells of the bounding box according to a rule:
          - For train_2: Fill with a default color ('9'), then iterate through the selected input objects. For each '3' cell within an input object, find its corresponding relative position within the output bounding box (based on center mapping) and set that output cell to '3', overwriting the default '9'.
          - For train_1: The interior fill appears more complex, possibly involving copying or transforming the content of the primary selected input object into the output bounding box, potentially scaling or modifying it. (The exact rule is less certain).
```
```python
"""
This program transforms an input grid based on identifying and processing specific objects within it.

The core logic observed, particularly from the second training example, involves:
1. Identifying all contiguous regions (objects) of non-background ('8') cells.
2. Filtering these objects to select those containing specific colors (e.g., both '3' and '9').
3. Calculating the geometric center of each selected object.
4. Determining a bounding box that encloses all these centers.
5. Creating an output grid filled with the background color ('8').
6. Populating the calculated bounding box in the output grid:
    a. Setting the border cells of the box to a specific color (e.g., '3').
    b. Filling the interior cells with a default color (e.g., '9').
    c. Overlaying specific colors (e.g., '3') from the selected input objects onto the interior of the output box. The position of these overlaid colors is determined by mapping the cell's position relative to its input object's center to a corresponding position relative to the center of the output bounding box.

Note: The logic for the first training example appears different (selection based on size/enclosure, different border/fill colors, potential color transformations within the object) and is not fully captured by this implementation. This code prioritizes the clearer pattern from the second example.
"""

import numpy as np
from skimage.measure import label, regionprops
from collections import namedtuple
import math

# Define structure for object properties
# Bbox is (min_row, min_col, max_row_inclusive, max_col_inclusive)
Object = namedtuple("Object", ["label", "coords", "colors", "bbox", "center", "size"])

def find_objects(grid: np.ndarray, background_color: int) -> list[Object]:
    """
    Identifies connected regions (objects) of non-background colors in the grid.

    Args:
        grid: The input numpy array.
        background_color: The integer value representing the background.

    Returns:
        A list of Object namedtuples, each containing properties of an object.
            - label: Unique integer ID for the object.
            - coords: Nx2 numpy array of (row, col) coordinates.
            - colors: Set of unique non-background colors in the object.
            - bbox: Tuple (min_row, min_col, max_row_incl, max_col_incl).
            - center: Tuple (center_row, center_col) - float coordinates.
            - size: Integer number of pixels in the object.
    """
    mask = grid != background_color
    # Use connectivity=1 for 4-way neighbors (up, down, left, right)
    labeled_grid, num_labels = label(mask, connectivity=1, background=0, return_num=True)

    objects = []
    # Use regionprops for efficient calculation of properties
    # Pass grid itself to intensity_image to access original values if needed
    props = regionprops(labeled_grid, intensity_image=grid)

    for region in props:
        # region.label is the label number
        coords = region.coords # Nx2 array of (row, col)
        if not coords.size > 0: continue # Skip empty regions if any

        # Extract colors present in the object using the coordinates
        colors_present = set(grid[coords[:, 0], coords[:, 1]])
        # Remove background color if present (though mask should prevent this)
        colors_present.discard(background_color)

        if not colors_present: continue # Skip if somehow only background was included

        # Bbox: (min_row, min_col, max_row, max_col) - Note: max is *exclusive* in skimage
        min_r, min_c, max_r_excl, max_c_excl = region.bbox
        # Convert to inclusive bbox for easier use later
        bbox_inclusive = (min_r, min_c, max_r_excl - 1, max_c_excl - 1)

        # Center: (centroid-0, centroid-1) -> (row, col)
        center_r, center_c = region.centroid

        # Size: number of pixels
        size = region.area

        objects.append(Object(
            label=region.label,
            coords=coords,
            colors=colors_present,
            bbox=bbox_inclusive,
            center=(center_r, center_c),
            size=size
        ))

    return objects

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules primarily derived from train_2.
    Finds objects containing both 3 and 9, calculates bbox of their centers,
    and populates this box with border 3, fill 9, overlaying 3s from inputs.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    background_color = 8 # Deduced from examples
    output_grid = np.full_like(input_grid, background_color)

    # 1. Find all non-background objects
    objects = find_objects(input_grid, background_color)
    if not objects:
        return output_grid.tolist() # Return background if no objects found

    # 2. Filter objects: Select objects containing both 3 and 9 (train_2 logic)
    required_colors = {3, 9}
    border_color = 3
    fill_color = 9
    overlay_color = 3 # The color from input objects to overlay
    selected_objects = [obj for obj in objects if required_colors.issubset(obj.colors)]

    # If the primary filtering logic (train_2) doesn't yield results,
    # return the background grid, as the alternative (train_1) logic is unclear.
    if not selected_objects:
        # print("No objects found matching criteria {3, 9}. Returning background.")
        return output_grid.tolist()

    # 3. Determine the output bounding box based on centers of selected objects
    centers = [obj.center for obj in selected_objects]
    if not centers:
        # This case should not happen if selected_objects is not empty, but check anyway
        return output_grid.tolist()

    center_rows = [r for r, c in centers]
    center_cols = [c for r, c in centers]

    # Determine bounds by rounding the min/max of center coordinates
    # Using math.floor/math.ceil might be slightly more robust than round()
    # Let's use rounding as per initial thought process.
    min_r_bbox = int(round(min(center_rows)))
    max_r_bbox = int(round(max(center_rows)))
    min_c_bbox = int(round(min(center_cols)))
    max_c_bbox = int(round(max(center_cols)))

    # Ensure bbox coordinates are within grid dimensions
    min_r_bbox = max(0, min_r_bbox)
    min_c_bbox = max(0, min_c_bbox)
    max_r_bbox = min(height - 1, max_r_bbox)
    max_c_bbox = min(width - 1, max_c_bbox)

    # Handle degenerate cases where bbox might be invalid after rounding/clipping
    if min_r_bbox > max_r_bbox or min_c_bbox > max_c_bbox:
        # print("Degenerate bounding box calculated. Returning background.")
        return output_grid.tolist()

    # 4. Populate the output bounding box
    # Calculate the geometric center of the output bounding box
    out_center_r = (min_r_bbox + max_r_bbox) / 2.0
    out_center_c = (min_c_bbox + max_c_bbox) / 2.0

    # Fill border and interior first
    for r in range(min_r_bbox, max_r_bbox + 1):
        for c in range(min_c_bbox, max_c_bbox + 1):
            is_border = (r == min_r_bbox or r == max_r_bbox or
                         c == min_c_bbox or c == max_c_bbox)
            if is_border:
                output_grid[r, c] = border_color
            else:
                output_grid[r, c] = fill_color

    # Overlay the 'overlay_color' from selected input objects
    for obj in selected_objects:
        obj_center_r, obj_center_c = obj.center
        # Iterate through coordinates of the current object
        for r_in, c_in in obj.coords:
            # Check if this cell in the input object has the color to be overlaid
            if input_grid[r_in, c_in] == overlay_color:
                # Calculate position relative to the input object's center
                delta_r = r_in - obj_center_r
                delta_c = c_in - obj_center_c

                # Calculate target position in the output grid relative to the output box center
                r_out = int(round(out_center_r + delta_r))
                c_out = int(round(out_center_c + delta_c))

                # Check if the target position is strictly *inside* the output bbox (not on the border)
                # and also within the overall grid bounds (safety check)
                if (min_r_bbox < r_out < max_r_bbox and
                    min_c_bbox < c_out < max_c_bbox and
                    0 <= r_out < height and 0 <= c_out < width):
                     output_grid[r_out, c_out] = overlay_color

    return output_grid.tolist()
```
