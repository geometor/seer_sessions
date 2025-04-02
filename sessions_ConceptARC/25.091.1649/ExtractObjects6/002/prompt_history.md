
## train_1

**input:**
```
0 0 0 6 0 0 0 4 5 3 3 3 3 5 5
0 0 6 0 6 0 0 4 5 3 5 5 3 5 5
0 6 0 0 0 6 0 4 5 3 5 5 3 5 5
6 0 0 0 0 0 6 4 5 3 5 5 3 5 5
0 6 0 0 0 6 0 4 5 3 5 5 3 5 5
0 0 6 0 6 0 0 4 5 3 5 5 3 5 5
0 0 0 6 0 0 0 4 5 3 3 3 3 5 5
```


**output:**
```
0 0 0 6 0 0 0 3 3 3 3
0 0 6 0 6 0 0 3 0 0 3
0 6 0 0 0 6 0 3 0 0 3
6 0 0 0 0 0 6 3 0 0 3
0 6 0 0 0 6 0 3 0 0 3
0 0 6 0 6 0 0 3 0 0 3
0 0 0 6 0 0 0 3 3 3 3
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7
7 7 7 2 7 7 7 7
7 7 7 2 7 7 7 7
7 7 7 2 7 7 7 7
7 2 2 2 2 2 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
4 4 4 4 4 4 4 4
8 8 8 3 8 8 8 8
8 8 3 3 3 8 8 8
8 8 8 3 8 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
```


**output:**
```
0 0 2 0 0
0 0 2 0 0
0 0 2 0 0
2 2 2 2 2
0 0 3 0 0
0 3 3 3 0
0 0 3 0 0
```

Okay, let's analyze the provided examples to understand the transformation logic.

## Perception

1.  **Input Structure:** The input grids appear to be divided into two main regions by a single, solid line (row or column) of yellow (4) pixels.
2.  **Regions:** Each region contains a background color and one or more "object" colors forming distinct shapes.
    *   In `train_1`, the input is split vertically by a yellow column. The left region has a magenta (6) diamond on a white (0) background. The right region has green (3) pixels within a gray (5) frame, also on a white background outside the frame.
    *   In `train_2`, the input is split horizontally by a yellow row. The top region has a red (2) 'T' shape on an orange (7) background. The bottom region has a green (3) cross shape on an azure (8) background.
3.  **Transformation:**
    *   The yellow separator line is removed in the output.
    *   The objects from each region seem to be extracted.
    *   The original background colors within each region are replaced with a uniform white (0) background in the output.
    *   In `train_1`, the magenta diamond is copied directly. However, for the green/gray region, only the *outer perimeter* of the green shape is kept. The gray frame is discarded.
    *   In `train_2`, the red 'T' and green cross shapes are extracted.
    *   The extracted shapes/objects are placed onto the new white background.
    *   The relative orientation of the regions (side-by-side in `train_1`, top-bottom in `train_2`) is preserved.
4.  **Output Resizing/Alignment:**
    *   In `train_1` (horizontal split), the output height matches the input height (7). The widths of the processed regions (7 for the left, 4 for the right) are concatenated.
    *   In `train_2` (vertical split), the output width seems standardized. The red 'T' has a bounding box width of 5. The green cross has a bounding box width of 3. In the output, both shapes occupy a width of 5, with the narrower cross shape being centered horizontally. The heights of the processed regions (4 for the top, 3 for the bottom) are concatenated.
    *   This suggests that if the split is vertical (by a row), the *widths* of the resulting parts are standardized to the maximum width before concatenation. If the split is horizontal (by a column), the *heights* are standardized (though in `train_1`, they were already equal).

## Facts


```yaml
task_type: object_extraction_and_composition

components:
  - role: separator
    attributes:
      color: yellow (4)
      shape: solid line (row or column)
      function: divides the input grid into distinct regions
      persistence: removed in output

  - role: region
    attributes:
      count: typically two per input grid, defined by the separator
      content: contains a background color and one or more object colors
      processing: processed independently

  - role: background
    attributes:
      location: within a region
      color: variable (white, gray, orange, azure observed)
      relation_to_object: surrounds or fills space around the object(s)
      persistence: replaced by white (0) in the output

  - role: object
    attributes:
      location: within a region
      color: variable (magenta, green, red observed)
      shape: variable (diamond, square-like, T, cross observed)
      relation_to_background: distinct from the region's background color
      persistence: extracted and placed onto the output grid's white background
    subtypes:
      - type: primary_object
        attributes:
          color: the main non-background color(s) in a region
          extraction_rule: typically extracted based on minimal bounding box
      - type: frame_object (optional)
        attributes:
          color: e.g., gray (5) in train_1
          relation_to_primary: often surrounds or is adjacent to the primary object
          persistence: usually discarded during extraction

actions:
  - name: identify_separator
    inputs: input_grid
    outputs: separator_line (position, orientation), split_orientation (horizontal/vertical)
    description: Find the solid yellow line dividing the grid.

  - name: split_grid
    inputs: input_grid, separator_line
    outputs: list_of_subgrids
    description: Divide the input grid into subgrids based on the separator.

  - name: extract_object_representation
    inputs: subgrid
    outputs: processed_subgrid (object on white background, cropped), dimensions (height, width)
    description: >
      Identify background and object colors.
      Apply extraction logic:
      If green(3) object with gray(5) frame detected, extract green perimeter.
      Otherwise, extract primary object shape(s).
      Replace original background with white(0).
      Crop to minimal bounding box of the extracted object/perimeter.

  - name: standardize_dimensions
    inputs: list_of_processed_subgrids, split_orientation
    outputs: list_of_standardized_subgrids
    description: >
      If split_orientation is vertical (row separator), find max width. Pad narrower subgrids horizontally with white(0) to match max width, centering the object.
      If split_orientation is horizontal (column separator), find max height. Pad shorter subgrids vertically with white(0) to match max height, centering the object.

  - name: combine_subgrids
    inputs: list_of_standardized_subgrids, split_orientation
    outputs: output_grid
    description: Concatenate the standardized subgrids according to the original split orientation (horizontally for horizontal split, vertically for vertical split).

relationships:
  - type: spatial
    description: Relative positions of regions in the input are preserved in the output after processing and standardization.
  - type: conditional_processing
    description: The extraction logic for an object depends on the colors present (e.g., green and gray trigger perimeter extraction).
  - type: dimensional_alignment
    description: The dimension orthogonal to the split axis (width for vertical split, height for horizontal split) is standardized across processed subgrids before combination.
```


## Natural Language Program

1.  **Find Separator:** Scan the input grid to locate a complete horizontal or vertical line composed solely of yellow (4) pixels. Note the orientation (horizontal/vertical) and position of this separator line.
2.  **Divide Input:** Split the input grid into two subgrids along the separator line. The separator line itself is discarded.
3.  **Process Each Subgrid:** For each subgrid obtained in step 2, perform the following:
    a.  **Identify Colors:** Determine the background color (typically the most frequent color) and the object color(s) (the other non-yellow colors).
    b.  **Extract Feature:**
        i.  **Special Case:** If the subgrid contains green (3) pixels as the primary object and also contains gray (5) pixels (likely forming a frame or adjacent structure), identify only the pixels forming the outer perimeter of the green shape.
        ii. **General Case:** Otherwise, identify all pixels belonging to the primary object color(s).
    c.  **Create Output Subgrid:** Create a new grid containing only the extracted feature pixels (from step 3b) placed at their original relative positions within the feature's minimal bounding box. Fill the rest of the bounding box with white (0) pixels. Note the height and width of this new grid.
4.  **Standardize Dimensions:**
    a.  **Vertical Split (Row Separator):** If the separator found in step 1 was horizontal (a row), compare the *widths* of all output subgrids created in step 3c. Find the maximum width. For any subgrid narrower than this maximum, expand its width by adding columns of white (0) pixels equally to the left and right sides (centering the original content) until it matches the maximum width.
    b.  **Horizontal Split (Column Separator):** If the separator found in step 1 was vertical (a column), compare the *heights* of all output subgrids created in step 3c. Find the maximum height. For any subgrid shorter than this maximum, expand its height by adding rows of white (0) pixels equally to the top and bottom (centering the original content) until it matches the maximum height.
5.  **Combine Results:** Concatenate the standardized subgrids (from step 4) back together in their original relative order (top-to-bottom for a vertical split, left-to-right for a horizontal split) to form the final output grid.
```python
import numpy as np
from collections import Counter
import math

"""
Processes an input grid by performing the following steps:

1.  **Find Separator:** Locates a solid horizontal or vertical line of yellow (4) pixels that divides the grid.
2.  **Divide Input:** Splits the input grid into two subgrids based on the separator, discarding the separator itself.
3.  **Process Each Subgrid:**
    a.  Identifies object pixels (non-background, non-yellow).
    b.  Applies extraction logic:
        i.  **Special Case:** If green (3) and gray (5) pixels are present, extracts only the outer perimeter of the green shape(s). The perimeter is defined as green pixels adjacent (up, down, left, right) to the most frequent non-green, non-gray color (assumed background).
        ii. **General Case:** Extracts all object pixels (non-background, non-yellow).
    c.  Creates a new grid containing the extracted pixels on a white (0) background, cropped to the minimal bounding box of the extracted pixels.
4.  **Standardize Dimensions:**
    a.  If the split was vertical (row separator), pads the width of the processed subgrids to match the maximum width found among them, centering the content horizontally.
    b.  If the split was horizontal (column separator), pads the height of the processed subgrids to match the maximum height found among them, centering the content vertically.
5.  **Combine Results:** Concatenates the standardized subgrids back together according to the original split orientation (vertically for vertical splits, horizontally for horizontal splits).
"""

def find_separator(grid):
    """Finds a horizontal or vertical solid line of yellow (4)."""
    h, w = grid.shape
    # Check for horizontal separator
    for r in range(h):
        if np.all(grid[r, :] == 4):
            return 'h', r
    # Check for vertical separator
    for c in range(w):
        if np.all(grid[:, c] == 4):
            return 'v', c
    return None, -1 # Should not happen based on examples

def get_bounding_box(coords):
    """Calculates the bounding box for a list of coordinates."""
    if not coords:
        return 0, 0, 0, 0 # Return zero size if no coords
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return min_r, max_r, min_c, max_c

def find_green_perimeter(subgrid):
    """Finds green pixels adjacent to the background color."""
    h, w = subgrid.shape
    colors = np.unique(subgrid)
    
    # Identify potential background color (most frequent non-green, non-gray)
    counts = Counter(subgrid.flatten())
    bg_color = 0 # Default to white if no clear background
    max_count = -1
    for color, count in counts.items():
        if color != 3 and color != 5 and color != 4: # Exclude green, gray, yellow
             if count > max_count:
                 max_count = count
                 bg_color = color
        # If only green and gray exist besides maybe yellow, background might be ambiguous
        # Based on train_1, the background is white(0). Let's assume 0 if no other dominant color.
        elif 3 in colors and 5 in colors and 0 in colors:
             bg_color = 0 # Explicitly handle case from train_1 right side

    perimeter_coords = []
    green_coords = np.argwhere(subgrid == 3)

    for r, c in green_coords:
        is_perimeter = False
        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w:
                if subgrid[nr, nc] == bg_color:
                    is_perimeter = True
                    break
            else: # Edge of the subgrid, could be considered perimeter if bg is outside
                 # This might need refinement depending on task specifics, but adjacency to explicit bg seems safer
                 pass
        if is_perimeter:
            perimeter_coords.append((r, c))

    return perimeter_coords, 3 # Return coordinates and the color (green)

def extract_feature(subgrid):
    """Extracts the main feature/object from a subgrid."""
    h, w = subgrid.shape
    unique_colors = np.unique(subgrid)
    
    # Handle the special green (3) and gray (5) case
    if 3 in unique_colors and 5 in unique_colors:
        feature_coords, feature_color = find_green_perimeter(subgrid)
        if not feature_coords: # Fallback if no perimeter found? Extract all green?
             # For now, stick to perimeter. If it fails, return empty coords.
             pass
    else:
        # General case: extract non-background, non-yellow pixels
        counts = Counter(subgrid.flatten())
        # Find likely background (most frequent, non-yellow)
        bg_color = -1
        max_count = -1
        for color, count in counts.items():
             if color != 4: # ignore yellow separator remnants if any
                 if count > max_count:
                     max_count = count
                     bg_color = color
        
        # Object pixels are those not matching background or yellow
        feature_coords = []
        feature_color = -1 # Usually one object color, but could be multiple
        object_colors = set()

        for r in range(h):
            for c in range(w):
                color = subgrid[r, c]
                if color != bg_color and color != 4:
                    feature_coords.append((r, c))
                    object_colors.add(color)

        # Determine the single feature color if possible (e.g., the most frequent object color)
        # For simplicity, if multiple object colors exist, just pick one.
        # This might need adjustment if objects can have multiple colors.
        # In the examples, objects seem monochromatic (excluding the green/gray case handled above)
        if len(object_colors) == 1:
             feature_color = object_colors.pop()
        elif len(object_colors) > 1:
             # Heuristic: pick the most frequent non-background color
             obj_counts = {c: counts[c] for c in object_colors}
             feature_color = max(obj_counts, key=obj_counts.get)
             # Filter coords to only include the chosen feature color
             feature_coords = [(r,c) for r,c in feature_coords if subgrid[r,c] == feature_color]
        else: # No object pixels found
            feature_color = 0 # default color for empty?

    if not feature_coords:
        return np.zeros((1, 1), dtype=int), (1, 1) # Return minimal grid if no feature

    # Create the output subgrid based on bounding box
    min_r, max_r, min_c, max_c = get_bounding_box(feature_coords)
    out_h = max_r - min_r + 1
    out_w = max_c - min_c + 1
    output_subgrid = np.zeros((out_h, out_w), dtype=int) # Fill with white (0)

    # Place feature pixels
    for r, c in feature_coords:
        # Check if the pixel's color matches the primary feature color (relevant for multi-color objects)
        # Or if it's the green perimeter case where color is always 3
        pixel_color = subgrid[r,c]
        if pixel_color == feature_color:
             output_subgrid[r - min_r, c - min_c] = feature_color

    return output_subgrid, (out_h, out_w)


def pad_grid(grid, target_h, target_w, bg_color=0):
    """Pads a grid to target dimensions, centering the content."""
    h, w = grid.shape
    pad_h = target_h - h
    pad_w = target_w - w

    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top
    pad_left = pad_w // 2
    pad_right = pad_w - pad_left

    if pad_top < 0 or pad_bottom < 0 or pad_left < 0 or pad_right < 0:
        # This case should ideally not happen if target dimensions are max dimensions
        # If it does, maybe crop instead? For now, assume padding is non-negative.
        # Or perhaps return the original grid if target is smaller.
        print(f"Warning: Negative padding calculated. Grid shape: ({h},{w}), Target: ({target_h},{target_w})")
        # Let's handle by clipping target dims to be at least current dims
        target_h = max(h, target_h)
        target_w = max(w, target_w)
        pad_h = target_h - h
        pad_w = target_w - w
        pad_top = pad_h // 2
        pad_bottom = pad_h - pad_top
        pad_left = pad_w // 2
        pad_right = pad_w - pad_left


    padded_grid = np.pad(
        grid,
        ((pad_top, pad_bottom), (pad_left, pad_right)),
        mode='constant',
        constant_values=bg_color
    )
    return padded_grid


def transform(input_grid):
    """
    Transforms the input grid according to the described logic.
    """
    input_array = np.array(input_grid, dtype=int)

    # 1. Find Separator
    orientation, index = find_separator(input_array)
    if orientation is None:
        # Handle error: No separator found (shouldn't happen for valid tasks)
        return input_grid # Or raise an error

    # 2. Divide Input
    subgrids = []
    if orientation == 'h': # Horizontal separator (row)
        if index > 0:
            subgrids.append(input_array[:index, :])
        if index < input_array.shape[0] - 1:
            subgrids.append(input_array[index+1:, :])
        split_orientation = 'vertical' # Regions are top/bottom -> vertical stack
    elif orientation == 'v': # Vertical separator (column)
        if index > 0:
            subgrids.append(input_array[:, :index])
        if index < input_array.shape[1] - 1:
             subgrids.append(input_array[:, index+1:])
        split_orientation = 'horizontal' # Regions are left/right -> horizontal stack

    # 3. Process Each Subgrid
    processed_subgrids = []
    dimensions = []
    for subgrid in subgrids:
        processed, (h, w) = extract_feature(subgrid)
        processed_subgrids.append(processed)
        dimensions.append((h, w))

    if not processed_subgrids:
         return [[]] # Return empty if no subgrids resulted

    # 4. Standardize Dimensions
    standardized_subgrids = []
    if split_orientation == 'vertical': # Row separator -> standardize width
        max_w = 0
        if dimensions:
             max_w = max(w for h, w in dimensions)
        
        for i, grid in enumerate(processed_subgrids):
            h, w = dimensions[i]
            if w < max_w:
                 standardized = pad_grid(grid, h, max_w)
                 standardized_subgrids.append(standardized)
            else:
                 standardized_subgrids.append(grid)

    elif split_orientation == 'horizontal': # Column separator -> standardize height
        max_h = 0
        if dimensions:
            max_h = max(h for h, w in dimensions)

        for i, grid in enumerate(processed_subgrids):
            h, w = dimensions[i]
            if h < max_h:
                standardized = pad_grid(grid, max_h, w)
                standardized_subgrids.append(standardized)
            else:
                 standardized_subgrids.append(grid)

    # 5. Combine Results
    if not standardized_subgrids:
        return [[]] # Return empty grid if processing failed

    if split_orientation == 'vertical':
        output_array = np.vstack(standardized_subgrids)
    elif split_orientation == 'horizontal':
        output_array = np.hstack(standardized_subgrids)
    else: # Should not happen
        output_array = standardized_subgrids[0]


    # Convert final numpy array back to list of lists
    output_grid = output_array.tolist()
    return output_grid

```
