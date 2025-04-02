## General Assessment

The initial code successfully identified the largest connected component of non-white pixels (using 8-way connectivity) and calculated its bounding box. The dimensions derived from this bounding box correctly matched the dimensions of the expected output grid across all training examples. However, the code failed because it performed a simple rectangular crop of the input grid based on these bounds. The comparison between the `transformed output` and the `expected output` reveals that the output grid should *only* contain the pixels belonging to the largest object itself, placed within the bounding box frame, while all other positions within that frame should be the background color (white, 0). The original crop included background pixels and potentially pixels from smaller objects that happened to fall within the largest object's bounding box.

The strategy needs refinement: instead of cropping, create a new grid of the correct dimensions (derived from the bounding box) initialized with the background color, and then "paint" only the pixels from the largest object onto this new canvas, adjusting their coordinates relative to the bounding box's top-left corner.

## Metrics

Based on the previous `code_execution` output and analysis:

*   **Connectivity:** 8-way connectivity is used for identifying objects.
*   **Background Color:** White (0) is the background color.
*   **Object Selection Criterion:** The object with the maximum number of non-white pixels is selected.
*   **Bounding Box Role:** Defines the exact dimensions (height and width) of the output grid.
*   **Output Content:** Consists *only* of the pixels from the selected largest object, translated to fit within the bounding box dimensions, padded with the background color.

| Example | Input Dims | Expected Output Dims | Largest Object Size (Pixels) | Largest Object BBox (min_r, max_r, min_c, max_c) | BBox Derived Dims (H, W) | BBox Dims Match Output Dims? | Simple Crop Matches Output? |
| :------ | :--------- | :------------------- | :--------------------------- | :---------------------------------------------- | :------------------------- | :--------------------------- | :-------------------------- |
| 1       | (20, 20)   | (13, 13)             | 100                          | (0, 12, 6, 18)                                  | (13, 13)                   | Yes                          | No                          |
| 2       | (20, 20)   | (10, 10)             | 46                           | (2, 11, 6, 15)                                  | (10, 10)                   | Yes                          | No                          |
| 3       | (20, 20)   | (10, 10)             | 48                           | (9, 18, 1, 10)                                  | (10, 10)                   | Yes                          | No                          |

## Facts


```yaml
task_type: object_extraction, filtering, relative_positioning

components:
  - role: input_grid
    type: 2D array of integers (colors 0-9)
    properties:
      - contains a background color (white, 0)
      - may contain multiple distinct objects (groups of connected non-white pixels)
  - role: output_grid
    type: 2D array of integers (colors 0-9)
    properties:
      - dimensions match the bounding box of the 'target object' from the input_grid.
      - contains only the pixels belonging to the 'target object', positioned relative to the top-left corner of the bounding box.
      - all pixels not belonging to the target object are set to the background color (white, 0).

objects:
  - type: pixel_group
    definition: A contiguous group of non-white pixels in the input grid.
    connectivity: 8-way (includes diagonals)
    properties:
      - pixels: list of (row, col) coordinates comprising the object.
      - size: number of pixels in the group (len(pixels)).
      - bounding_box: minimum rectangle enclosing all pixels (min_row, max_row, min_col, max_col).
  - type: target_object
    definition: The 'pixel_group' with the largest 'size' (maximum pixel count).
    assumption: There is expected to be a unique largest object.

relationships:
  - type: selection
    description: The target_object is selected from all identified pixel_groups based on having the maximum size.
  - type: spatial_mapping
    description: Each pixel (r, c) of the target_object in the input grid is mapped to a new position (r - min_row, c - min_col) in the output grid, where (min_row, min_col) are from the target_object's bounding_box.
  - type: framing
    description: The target_object's bounding_box determines the height (max_row - min_row + 1) and width (max_col - min_col + 1) of the output grid.

actions:
  - name: find_pixel_groups
    description: Identify all connected components of non-white pixels (value != 0) using 8-way connectivity, returning a list where each item contains the coordinates of pixels for one group.
    inputs: input_grid
    outputs: list_of_pixel_groups (each group is a list of (r, c) tuples)
  - name: select_target_object
    description: Find the pixel_group from the list that has the maximum number of pixels.
    inputs: list_of_pixel_groups
    outputs: target_object_pixels (list of (r, c) tuples)
  - name: get_bounding_box
    description: Calculate the min/max row/column indices for the pixels in the target object.
    inputs: target_object_pixels
    outputs: bounding_box (min_r, max_r, min_c, max_c)
  - name: create_output_canvas
    description: Create a new grid with height = max_r - min_r + 1 and width = max_c - min_c + 1, filled entirely with the background color (white, 0).
    inputs: bounding_box
    outputs: output_grid
  - name: draw_target_object
    description: For each pixel (r, c) in target_object_pixels, get its color from input_grid[r, c] and place it in the output_grid at position (r - min_r, c - min_c).
    inputs: output_grid, target_object_pixels, input_grid, bounding_box (min_r, min_c needed)
    outputs: populated_output_grid

goal: Extract the single largest connected object (by pixel count) of non-background colors from the input grid and display it, preserving pixel colors and relative positions, on a clean background grid sized exactly to fit the object's bounding box.
```


## Natural Language Program

1.  **Scan and Group:** Examine the input grid. Identify all distinct groups of connected non-white pixels (pixels with values 1-9). Use 8-way connectivity (horizontal, vertical, and diagonal neighbors are considered connected). Keep track of the coordinates `(row, col)` for every pixel within each group.
2.  **Find the Largest Group:** Calculate the size (number of pixels) for each group found in step 1. Identify the group that has the largest size. This is the "target object".
3.  **Determine Bounds:** Find the minimum row index (`min_r`), maximum row index (`max_r`), minimum column index (`min_c`), and maximum column index (`max_c`) among all pixels belonging to the target object. These define its bounding box.
4.  **Prepare Output Grid:** Create a new, empty grid. The height of this grid will be `(max_r - min_r + 1)` and the width will be `(max_c - min_c + 1)`. Fill this entire new grid with the background color (white, 0).
5.  **Transfer Object:** Iterate through each pixel coordinate `(r, c)` that belongs to the target object (identified in step 2).
    a.  Retrieve the original color of this pixel from the input grid at `input_grid[r, c]`.
    b.  Calculate the corresponding position in the output grid: `new_row = r - min_r`, `new_col = c - min_c`.
    c.  Place the retrieved color into the output grid at `output_grid[new_row, new_col]`.
6.  **Final Output:** The newly created and populated grid is the result.