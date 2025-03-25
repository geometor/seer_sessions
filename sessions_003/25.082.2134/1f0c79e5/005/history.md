
Previous Code:
```python
"""
1.  **Identify the Input Object:** Locate the contiguous non-zero pixels in the input grid. Determine the bounding box (min/max row and column) of this object.
2.  **Identify the Core and Unique Colors:** Determine the core color (the most frequent non-zero color within the object). If there are multiple colors with same frequency, use first encountered.  Identify if there's a unique color (occurring only once).
3.  **Determine Unique Pixel Location:** Locate Unique Color Pixel within the input grid, else note there is no unique color.
4.  **Construct 9-Sliced Output:** Create an output grid filled with zeros. The dimensions of the input's object's bounding box determine how the grid is transformed to 9-sliced output grid.
5.  **Place the Core:** Create a 3x3 block of the core color.  Place this 3x3 block in the center of the 9-sliced section of the output grid.
6.  **Mirror based on Unique Pixel (or color balanced input):**
    *   Determine where unique color is positioned.
    *   If the unique pixel is on the right edge of the *bounding box*, the central 3x3 core is placed to prepare for horizontal mirroring.
    *   If the unique pixel is on the left edge of the *bounding box*, the core is mirrored horizontally.
    *   If the unique pixel is on the top edge of the *bounding box*, the core is mirrored vertically.
    *   If the unique pixel is on the bottom edge of the *bounding box*, the core is placed to prepare for vertical mirroring.
    *   If there is no unique pixel and the core is made of multiple colors:
        *   It is as if the unique pixel is in a corner.
        *   Example 3, is acting as the 2 is on the bottom left corner.
        *    In Example 3, the 2 is on the top-right.

    *   If the unique pixel is in a corner of the bounding box:
        *   It is prepared by placing the core for both horizontal and vertical mirroring, and also needs mirroring on major diagonal.
7.  **Fill 9-sliced region:**  The identified transformations are performed creating the 9 slices.
"""

import numpy as np

def find_object_and_bbox(grid):
    """Finds the object (non-zero pixels) and its bounding box."""
    non_zero_pixels = np.argwhere(grid != 0)
    if len(non_zero_pixels) == 0:
        return [], None  # No object found

    min_row, min_col = np.min(non_zero_pixels, axis=0)
    max_row, max_col = np.max(non_zero_pixels, axis=0)
    object_pixels = [(r, c) for r in range(min_row, max_row + 1)
                     for c in range(min_col, max_col + 1)
                     if grid[r, c] != 0]
    bbox = ((min_row, max_row), (min_col, max_col))
    return object_pixels, bbox

def get_core_and_unique_colors(grid, object_pixels):
    """Identifies the core and unique colors within the object."""
    if not object_pixels:
        return None, None

    color_counts = {}
    for r, c in object_pixels:
        color = grid[r, c]
        color_counts[color] = color_counts.get(color, 0) + 1

    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)
    core_color = sorted_colors[0][0]
    unique_color = None
    if len(sorted_colors) >1 and sorted_colors[-1][1] == 1:
      unique_color = sorted_colors[-1][0]

    return core_color, unique_color

def find_unique_pixel_location(grid, object_pixels, unique_color):
    """Locates the unique color pixel within the grid."""
    if unique_color is None:
        return None
    for r, c in object_pixels:
        if grid[r, c] == unique_color:
            return (r, c)
    return None

def create_9_sliced_grid(bbox, input_grid):
  """Expands grid into a 9 sliced grid"""
  output_grid = np.zeros_like(input_grid)

  return output_grid

def determine_mirroring(bbox, unique_pixel_loc):
    """Determines mirroring operations based on unique pixel location and bbox."""
    if unique_pixel_loc is None:
       return "no_unique"  # Handle cases with no unique pixel

    (min_row, max_row), (min_col, max_col) = bbox
    row, col = unique_pixel_loc

    horizontal_mirror = False
    vertical_mirror = False
    diagonal_mirror = False

    if col == max_col:
        horizontal_mirror = True #right
    elif col == min_col:
        horizontal_mirror = True # left
    if row == max_row:
        vertical_mirror = True #bottom
    elif row == min_row:
        vertical_mirror = True #top
    if row == min_row and col == min_col:
        diagonal_mirror = True # top-left
    if row == min_row and col == max_col:
        diagonal_mirror = True  # top-right
    if row == max_row and col == min_col:
        diagonal_mirror = True # bottom left
    if row == max_row and col == max_col:
        diagonal_mirror = True  # bottom-right
    
    return horizontal_mirror, vertical_mirror, diagonal_mirror
  
def fill_9_sliced_grid(output_grid, core_color, bbox, horizontal_mirror, vertical_mirror, diagonal_mirror):
    """Fills 3x3 grid based on mirroring"""
    (min_row, max_row), (min_col, max_col) = bbox
    
    # Create 3x3
    core = np.full((3, 3), core_color)

    # size of original grid
    grid_height = output_grid.shape[0]
    grid_width = output_grid.shape[1]

    #center
    center_row_start = (grid_height-1) // 2 - 1
    center_col_start = (grid_width-1) // 2

    output_grid[center_row_start:center_row_start+3, center_col_start:center_col_start+3 ] = core

    # Horizontal Mirror
    if horizontal_mirror:
        if unique_pixel_loc[1] == max_col: # right
           output_grid[center_row_start:center_row_start+3, 0:center_col_start] = np.fliplr(core)
        if unique_pixel_loc[1] == min_col: # left
            output_grid[center_row_start:center_row_start+3, center_col_start+3:] = np.fliplr(core)
    
    # Vertical Mirror
    if vertical_mirror:
        if unique_pixel_loc[0] == max_row:  # bottom
            output_grid[0:center_row_start, center_col_start:center_col_start+3] = np.flipud(core)
        if unique_pixel_loc[0] == min_row: # top
            output_grid[center_row_start+3:, center_col_start:center_col_start+3] = np.flipud(core)

    # Diagonal Mirror
    if diagonal_mirror:
       flipped = np.transpose(core)
       if unique_pixel_loc == (min_row, min_col): #top-left
            output_grid[center_row_start+3:, center_col_start+3:] = flipped
       if unique_pixel_loc == (min_row, max_col):  #top-right
            output_grid[center_row_start+3:, 0:center_col_start] = flipped
       if unique_pixel_loc == (max_row, min_col):  #bottom-left
            output_grid[0:center_row_start, center_col_start+3:] = flipped
       if unique_pixel_loc == (max_row, max_col):  #bottom-right
            output_grid[0:center_row_start, 0:center_col_start] = flipped

    return output_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the object and its bounding box
    object_pixels, bbox = find_object_and_bbox(input_grid)

    # Get the core and unique colors
    core_color, unique_color = get_core_and_unique_colors(input_grid, object_pixels)
    
    # Find unique pixel location
    unique_pixel_loc = find_unique_pixel_location(input_grid, object_pixels, unique_color)
    if unique_pixel_loc is None and len(np.unique(input_grid[input_grid !=0])) > 1:
        # find "pseudo-unique" pixels, that would act as unique if we only had one of them
        colors, counts = np.unique(input_grid[input_grid != 0], return_counts=True)

        color_counts = {}
        for (r,c) in object_pixels:
            color = input_grid[r,c]
            if color not in color_counts:
                color_counts[color] = []
            color_counts[color].append((r,c))

        
        min_count = np.min(counts)

        pseudo_unique_color = colors[counts == min_count][0]

        pseudo_unique_pixels = color_counts[pseudo_unique_color]
        
        (min_row, max_row), (min_col, max_col) = bbox

        if pseudo_unique_color == core_color:
           unique_pixel_loc = pseudo_unique_pixels[0]
           if unique_pixel_loc[0] == min_row:
                unique_pixel_loc = (max_row, max_col) # top-right
           else:
                unique_pixel_loc = (min_row, min_col) # bottom-left
        else:
            # assume it is in a diagonal
            unique_pixel_loc = pseudo_unique_pixels[0]

    # Expand to 9-sliced
    output_grid = create_9_sliced_grid(bbox, output_grid)

    # Determine mirroring operations
    horizontal_mirror, vertical_mirror, diagonal_mirror = determine_mirroring(bbox, unique_pixel_loc)
    
    # Fill output_grid
    output_grid = fill_9_sliced_grid(output_grid, core_color, bbox, horizontal_mirror, vertical_mirror, diagonal_mirror)

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 2 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 4 4 4
0 0 0 0 0 4 4 4 0
0 0 0 0 4 4 4 0 0
0 0 0 4 4 4 0 0 0
0 0 4 4 4 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
match: False
pixels_off: None
size_correct: False
color_palette_correct: False
correct_pixel_counts: None

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 3 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0
0 0 0 0 3 3 3 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 3
```
match: False
pixels_off: None
size_correct: False
color_palette_correct: False
correct_pixel_counts: None

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 2 0 0 0 0
0 0 0 2 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 6 6 6
0 0 0 0 0 6 6 6 0
0 0 0 0 6 6 6 0 0
0 0 0 6 6 6 0 0 0
0 0 6 6 6 0 0 0 0
0 6 6 6 0 0 0 0 0
6 6 6 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
```
match: False
pixels_off: None
size_correct: False
color_palette_correct: False
correct_pixel_counts: None

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0
0 0 0 2 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
7 7 0 0 0 0 7 7 7
7 7 7 0 0 7 7 7 0
0 7 7 7 7 7 7 0 0
0 0 7 7 7 7 0 0 0
0 0 7 7 7 0 0 0 0
0 7 7 7 0 0 0 0 0
7 7 7 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
```
match: False
pixels_off: None
size_correct: False
color_palette_correct: False
correct_pixel_counts: None
Okay, let's analyze the results and refine the natural language program.

**General Assessment:**

The initial strategy correctly identified the core concept of finding an object, identifying a core color, and using a unique color to determine mirroring. However, the 9-slicing logic, especially the placement of the mirrored core and the handling of cases with *no true* unique color (where multiple colors appear with equal, minimum frequency), needs significant improvement. The assumption of mirroring *always* from the center also needs modification. The current code transforms *input grid* to *output grid* of the same size, while the *output grid* should follow nine-sliced output where dimensions are derived from the object in the *input grid*.

**Strategy for Resolving Errors:**

1.  **Fix 9-slicing Logic:**. The output grid size should be based on extending a 3x3 around the borders based on the *input grid* object's bounding box, not same dimension as *input grid*.
2.  **Improve Unique/Pseudo-Unique Pixel Handling:** The current logic for pseudo-unique pixels is not robust. We need a better way to identify what constitutes a valid "pseudo-unique" pixel, and the default positions aren't always correct.
3.  **Correct Mirroring Placement:** The mirroring should create the 9-sliced regions, not simply be a horizontal or vertical flip relative to the center.
4. **Diagonal Mirroring**: Diagonally mirrored should be better understood.

**Gather Metrics and Evidence:**

I'll use `tool_code` to gather more specific information about the examples, particularly regarding object sizes, core colors, unique colors, and their positions.



*code_execution:*
```python
import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    def find_object_and_bbox(grid):
        """Finds the object (non-zero pixels) and its bounding box."""
        non_zero_pixels = np.argwhere(grid != 0)
        if len(non_zero_pixels) == 0:
            return [], None  # No object found

        min_row, min_col = np.min(non_zero_pixels, axis=0)
        max_row, max_col = np.max(non_zero_pixels, axis=0)
        object_pixels = [(r, c) for r in range(min_row, max_row + 1)
                         for c in range(min_col, max_col + 1)
                         if grid[r, c] != 0]
        bbox = ((min_row, max_row), (min_col, max_col))
        return object_pixels, bbox

    def get_core_and_unique_colors(grid, object_pixels):
        """Identifies the core and unique colors within the object."""
        if not object_pixels:
            return None, None

        color_counts = {}
        for r, c in object_pixels:
            color = grid[r, c]
            color_counts[color] = color_counts.get(color, 0) + 1

        sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)
        core_color = sorted_colors[0][0]
        unique_color = None
        if len(sorted_colors) > 1 and sorted_colors[-1][1] == 1:
            unique_color = sorted_colors[-1][0]

        return core_color, unique_color
    
    def find_unique_pixel_location(grid, object_pixels, unique_color):
        """Locates the unique color pixel within the grid."""
        if unique_color is None:
            return None
        for r, c in object_pixels:
            if grid[r, c] == unique_color:
                return (r, c)
        return None


    object_pixels, bbox = find_object_and_bbox(input_grid)
    core_color, unique_color = get_core_and_unique_colors(input_grid, object_pixels)
    unique_pixel_loc = find_unique_pixel_location(input_grid, object_pixels, unique_color)

    analysis = {
        'object_pixels': object_pixels,
        'bbox': bbox,
        'core_color': core_color,
        'unique_color': unique_color,
        'unique_pixel_loc': unique_pixel_loc,
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape
    }
    return analysis

examples = [
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 4, 2, 0, 0, 0, 0, 0],
         [0, 0, 4, 4, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 4, 4, 4],
         [0, 0, 0, 0, 0, 4, 4, 4, 0],
         [0, 0, 0, 0, 4, 4, 4, 0, 0],
         [0, 0, 0, 4, 4, 4, 0, 0, 0],
         [0, 0, 4, 4, 4, 0, 0, 0, 0],
         [0, 0, 4, 4, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 3, 3, 0, 0, 0, 0, 0],
         [0, 0, 3, 2, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 3, 3, 0, 0, 0, 0, 0],
         [0, 0, 3, 3, 3, 0, 0, 0, 0],
         [0, 0, 0, 3, 3, 3, 0, 0, 0],
         [0, 0, 0, 0, 3, 3, 3, 0, 0],
         [0, 0, 0, 0, 0, 3, 3, 3, 0],
         [0, 0, 0, 0, 0, 0, 3, 3, 3],
         [0, 0, 0, 0, 0, 0, 0, 3, 3],
         [0, 0, 0, 0, 0, 0, 0, 0, 3]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 6, 2, 0, 0, 0, 0],
         [0, 0, 0, 2, 6, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 6, 6, 6],
         [0, 0, 0, 0, 0, 6, 6, 6, 0],
         [0, 0, 0, 0, 6, 6, 6, 0, 0],
         [0, 0, 0, 6, 6, 6, 0, 0, 0],
         [0, 0, 6, 6, 6, 0, 0, 0, 0],
         [0, 6, 6, 6, 0, 0, 0, 0, 0],
         [6, 6, 6, 0, 0, 0, 0, 0, 0],
         [6, 6, 0, 0, 0, 0, 0, 0, 0],
         [6, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 2, 2, 0, 0, 0, 0],
         [0, 0, 0, 2, 7, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[7, 7, 0, 0, 0, 0, 7, 7, 7],
         [7, 7, 7, 0, 0, 7, 7, 7, 0],
         [0, 7, 7, 7, 7, 7, 7, 0, 0],
         [0, 0, 7, 7, 7, 7, 0, 0, 0],
         [0, 0, 7, 7, 7, 0, 0, 0, 0],
         [0, 7, 7, 7, 0, 0, 0, 0, 0],
         [7, 7, 7, 0, 0, 0, 0, 0, 0],
         [7, 7, 0, 0, 0, 0, 0, 0, 0],
         [7, 0, 0, 0, 0, 0, 0, 0, 0]]
    )
]

for i, (input_grid, output_grid) in enumerate(examples):
    analysis = analyze_example(input_grid, output_grid)
    print(f"Example {i+1}:")
    print(f"  Object Pixels: {analysis['object_pixels']}")
    print(f"  Bounding Box: {analysis['bbox']}")
    print(f"  Core Color: {analysis['core_color']}")
    print(f"  Unique Color: {analysis['unique_color']}")
    print(f"  Unique Pixel Location: {analysis['unique_pixel_loc']}")
    print(f"  Input Shape: {analysis['input_shape']}")
    print(f"  Output Shape: {analysis['output_shape']}")
    print("-" * 20)

```

*code_execution_result:*
outcome: 1
```
Example 1:
  Object Pixels: [(4, 2), (4, 3), (5, 2), (5, 3)]
  Bounding Box: ((np.int64(4), np.int64(5)), (np.int64(2), np.int64(3)))
  Core Color: 4
  Unique Color: 2
  Unique Pixel Location: (4, 3)
  Input Shape: (9, 9)
  Output Shape: (9, 9)
--------------------
Example 2:
  Object Pixels: [(1, 2), (1, 3), (2, 2), (2, 3)]
  Bounding Box: ((np.int64(1), np.int64(2)), (np.int64(2), np.int64(3)))
  Core Color: 3
  Unique Color: 2
  Unique Pixel Location: (2, 3)
  Input Shape: (9, 9)
  Output Shape: (9, 9)
--------------------
Example 3:
  Object Pixels: [(3, 3), (3, 4), (4, 3), (4, 4)]
  Bounding Box: ((np.int64(3), np.int64(4)), (np.int64(3), np.int64(4)))
  Core Color: 6
  Unique Color: None
  Unique Pixel Location: None
  Input Shape: (9, 9)
  Output Shape: (9, 9)
--------------------
Example 4:
  Object Pixels: [(3, 3), (3, 4), (4, 3), (4, 4)]
  Bounding Box: ((np.int64(3), np.int64(4)), (np.int64(3), np.int64(4)))
  Core Color: 2
  Unique Color: 7
  Unique Pixel Location: (4, 4)
  Input Shape: (9, 9)
  Output Shape: (9, 9)
--------------------

```
**YAML Facts:**


```yaml
examples:
  - id: 1
    object:
      shape: rectangle
      colors: [4, 2]
      core_color: 4
      unique_color: 2
      unique_pixel_position: top-right # Relative to the bounding box
      bounding_box: [[4, 5], [2, 3]] # [min_row, max_row], [min_col, max_col]
    transformation:
      type: nine_slice_and_mirror
      output_shape: [9,9] # Not the final shape, will need to change
      horizontal_mirror: true
      vertical_mirror: false
      diagonal_mirror: false
  - id: 2
    object:
      shape: rectangle
      colors: [3, 2]
      core_color: 3
      unique_color: 2
      unique_pixel_position: bottom-right
      bounding_box:  [[1, 2], [2, 3]]
    transformation:
      type: nine_slice_and_mirror
      output_shape: [9,9] # Not the final shape, will need to change
      horizontal_mirror: false
      vertical_mirror: true
      diagonal_mirror: false
  - id: 3
    object:
      shape: rectangle
      colors: [6, 2]
      core_color: 6 # most frequent
      unique_color: None # No single unique color
      pseudo_unique_color: 2 # appears only twice
      pseudo_unique_pixel_position: top-right # Relative to bounding box.
      bounding_box: [[3, 4], [3, 4]]
    transformation:
      type: nine_slice_and_mirror
      output_shape: [9,9] # Not the final shape, will need to change
      horizontal_mirror: true
      vertical_mirror: true
      diagonal_mirror: true
  - id: 4
    object:
      shape: rectangle
      colors: [2, 7]
      core_color: 2
      unique_color: 7
      unique_pixel_position: bottom-right
      bounding_box: [[3, 4], [3, 4]]
    transformation:
      type: nine_slice_and_mirror
      output_shape: [9,9] # Not the final shape, will need to change
      horizontal_mirror: true
      vertical_mirror: true
      diagonal_mirror: true
```


**Natural Language Program:**

1.  **Identify Input Object:** Find the contiguous non-zero pixels in the input grid. Determine the bounding box (min/max row and min/max column) of this object.

2.  **Determine Core and Unique Colors:** Calculate the frequency of each non-zero color within the object. The core color is the most frequent color.  If there's a color that appears only once, it's the unique color. If there are multiple colors with the same *minimum* frequency, the first encountered is used.

3.  **Locate Unique/Pseudo-Unique Pixel:** Find the coordinates of the unique color pixel. If no unique color exists, find the coordinates of pixels of colors that have minimum frequency.

4. **Determine Output Dimensions:** Calculate the final dimensions of the output: `output_rows = object_height + 2 + padding`, `output_cols = object_width + 2 + padding`, where `object_height = max_row - min_row +1` and `object_width = max_col - min_col + 1`. In this case `padding` is always `0` so `output_rows = object_height + 2` and `output_cols = object_width + 2`

5.  **Create a 3x3 Core:** Create a 3x3 block filled with the core color.

6.  **Position and Mirror based on Unique/Pseudo-Unique Pixel:**
    *   If a unique pixel exists and is located on an edge of the object's bounding box:
        *   Right edge: Create a horizontal mirror of the 3x3 core to the *left*.
        *   Left edge: Create a horizontal mirror of the 3x3 core to the *right*.
        *   Bottom edge: Create a vertical mirror of the 3x3 core *above*.
        *   Top edge: Create a vertical mirror of the 3x3 core *below*.
    *   If a unique pixel is in a corner:
        * Mirror horizontally *and* vertically *and* diagonally to the opposite corner quadrant.
    * If there are only two pixels with different colors, and thus no true unique pixel, consider the first encountered color from the minimum frequency color as the "pseudo-unique" color for positioning. The position of the first "pseudo-unique" pixel dictates mirroring.

7.  **Construct Output Grid:** Create an output grid of zeros with the calculated dimensions. Place the 3x3 core and its mirrored versions based on the unique/pseudo-unique pixel's location.

8. Place original `core` to the center position of the `output_grid`.


