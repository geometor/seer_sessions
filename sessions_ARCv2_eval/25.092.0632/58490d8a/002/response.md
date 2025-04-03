**General Assessment:**

The previous attempt incorrectly assumed the target area to be extracted was a rectangle composed *entirely* of white pixels. The results clearly show this is wrong, as the generated outputs were much smaller than expected and consisted only of white pixels, whereas the expected outputs match the dimensions of a specific white-bordered area in the input and include non-white pixels found within that area.

The core error lies in the identification criteria for the rectangle. The new hypothesis is that the task requires identifying the largest rectangular region whose *border* is composed entirely of white pixels (0). The content *inside* this border (including non-white pixels) is then extracted.

**Strategy for Resolution:**

1.  Modify the search algorithm to identify candidate rectangles based on their *border* pixels being white (0).
2.  For each candidate rectangle identified by a white border, calculate its area.
3.  Select the rectangle with the largest area.
4.  Extract the subgrid corresponding to the *full extent* of this largest white-bordered rectangle from the input grid.

**Metrics Gathering:**

Let's verify the coordinates and dimensions of the assumed target rectangles (those with all-white borders) in the training inputs and compare them with the expected output dimensions.


``` python
import numpy as np

def find_largest_white_bordered_rect(grid):
    np_grid = np.array(grid, dtype=int)
    height, width = np_grid.shape
    max_area = -1
    best_rect_coords = None # (r1, c1, r2, c2)

    for r1 in range(height):
        for c1 in range(width):
            # Check if top-left is white (potential start of a border)
            if np_grid[r1, c1] == 0:
                # Expand to find potential bottom-right corner (r2, c2)
                for r2 in range(r1 + 1, height): # Need at least height 2 for a border
                    for c2 in range(c1 + 1, width): # Need at least width 2 for a border
                        # Check if all corners are white
                        if np_grid[r1, c2] == 0 and np_grid[r2, c1] == 0 and np_grid[r2, c2] == 0:
                            # Check top border (row r1, from c1 to c2)
                            if not np.all(np_grid[r1, c1:c2+1] == 0):
                                continue
                            # Check bottom border (row r2, from c1 to c2)
                            if not np.all(np_grid[r2, c1:c2+1] == 0):
                                continue
                            # Check left border (col c1, from r1 to r2)
                            if not np.all(np_grid[r1:r2+1, c1] == 0):
                                continue
                            # Check right border (col c2, from r1 to r2)
                            if not np.all(np_grid[r1:r2+1, c2] == 0):
                                continue

                            # If all borders are white, calculate area
                            current_height = r2 - r1 + 1
                            current_width = c2 - c1 + 1
                            current_area = current_height * current_width

                            if current_area > max_area:
                                max_area = current_area
                                best_rect_coords = (r1, c1, r2, c2)
                                # Keep rect_height and rect_width for clarity
                                best_rect_dims = (current_height, current_width)

    if best_rect_coords:
        return best_rect_coords, best_rect_dims
    else:
        return None, None

# --- Example 1 Data ---
input_1 = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 3, 3, 3],
    [3, 3, 3, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 8, 3, 3],
    [3, 3, 3, 8, 3, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3],
    [3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 8, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 4, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [0, 8, 0, 0, 0, 0, 0, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [0, 4, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3],
    [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3],
    [0, 2, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]
expected_output_1_shape = (7, 7)
coords_1, dims_1 = find_largest_white_bordered_rect(input_1)
print(f"Example 1: Found Coords={coords_1}, Dims={dims_1}, Expected Shape={expected_output_1_shape}")

# --- Example 2 Data ---
input_2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 2, 2, 2, 1, 1, 1, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 8, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 8, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 8, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 8, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 1, 1],
    [1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1],
    [1, 1, 1, 1, 4, 4, 4, 1, 1, 1, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1]
]
expected_output_2_shape = (7, 12)
coords_2, dims_2 = find_largest_white_bordered_rect(input_2)
print(f"Example 2: Found Coords={coords_2}, Dims={dims_2}, Expected Shape={expected_output_2_shape}")


# --- Example 3 Data ---
input_3 = [
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 1, 0, 0, 0, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 4, 0, 0, 0, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 8, 4, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
]
expected_output_3_shape = (5, 5)
coords_3, dims_3 = find_largest_white_bordered_rect(input_3)
print(f"Example 3: Found Coords={coords_3}, Dims={dims_3}, Expected Shape={expected_output_3_shape}")
```
```
Example 1: Found Coords=(13, 0, 19, 6), Dims=(7, 7), Expected Shape=(7, 7)
Example 2: Found Coords=(0, 11, 6, 22), Dims=(7, 12), Expected Shape=(7, 12)
Example 3: Found Coords=(2, 9, 6, 13), Dims=(5, 5), Expected Shape=(5, 5)

```
**Facts:**


```yaml
task_description: Identify and extract the content of the largest rectangular area defined by a border of white pixels in the input grid.
grid_properties:
  - input_grid_size: Variable.
  - output_grid_size: Variable, determined by the size of the identified white-bordered rectangle.
  - dominant_input_background_color: Varies (green, blue, azure), appears irrelevant to the output.
  - output_background_color: The extracted rectangle retains its original background color, which is white (0) along the border and potentially inside, but can contain other colors.
objects:
  - type: Rectangular Area with White Border
    properties:
      - border_color: All pixels forming the top, bottom, left, and right edges of the rectangle must be white (0).
      - content: Can contain any color pixel, including white (0) and non-white colors.
      - role: Defines the boundaries and content of the output grid.
      - location: Varies within the input grid.
      - key_feature: The largest such rectangle by area (width * height) in the input grid. (Assumed unique maximal based on examples).
  - type: Pixels
    properties:
      - color: Various colors (white, non-white).
      - location: Some are scattered outside the target rectangle (ignored), others are located *inside* or *on the border* of the target rectangle (preserved).
      - role: Pixels inside or on the border of the identified rectangle are copied to the output grid in their relative positions.
transformation:
  - action: Scan the input grid to find all possible rectangular regions.
  - action: For each rectangle, check if all pixels on its four borders (top row, bottom row, left column, right column) are white (0).
  - action: Calculate the area (width * height) for each rectangle confirmed to have an all-white border.
  - action: Select the white-bordered rectangle with the largest area.
  - action: Extract the subgrid defined by the boundaries (inclusive) of the selected rectangle.
  - result: The extracted subgrid, including its internal content and white border, becomes the output grid.
relationships:
  - The output grid is a subgrid of the input grid.
  - The dimensions of the output grid are identical to the dimensions of the largest white-bordered rectangular area found in the input.
  - The content of the output grid is identical to the content within and including the border of the largest white-bordered rectangular area in the input.
```


**Natural Language Program:**

1.  Initialize variables to track the maximum area found so far (initially -1) and the coordinates of the corresponding rectangle (initially null).
2.  Iterate through all possible top-left corner coordinates (r1, c1) in the input grid.
3.  Iterate through all possible bottom-right corner coordinates (r2, c2) such that r2 > r1 and c2 > c1 (ensuring a minimum rectangle size of 2x2, which is necessary for a border).
4.  For each potential rectangle defined by (r1, c1) and (r2, c2), check if its border is composed entirely of white (0) pixels:
    a.  Verify that the top row segment (row r1, from column c1 to c2) consists only of white pixels.
    b.  Verify that the bottom row segment (row r2, from column c1 to c2) consists only of white pixels.
    c.  Verify that the left column segment (column c1, from row r1 to r2) consists only of white pixels.
    d.  Verify that the right column segment (column c2, from row r1 to r2) consists only of white pixels.
5.  If all four border segments consist only of white pixels:
    a.  Calculate the height (r2 - r1 + 1) and width (c2 - c1 + 1) of the current rectangle.
    b.  Calculate the area (height * width).
    c.  If this area is greater than the maximum area found so far, update the maximum area and store the coordinates (r1, c1, r2, c2) and dimensions (height, width) of this rectangle.
6.  After checking all possible rectangles, if a maximum-area white-bordered rectangle was found:
    a.  Extract the subgrid from the input grid starting at the stored top-left corner (r1, c1) and spanning the stored height and width.
7.  Return the extracted subgrid as the output. If no white-bordered rectangle was found, return an empty grid or handle as appropriate (though based on examples, one is always expected).