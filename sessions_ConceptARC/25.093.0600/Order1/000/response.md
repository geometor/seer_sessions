## Perception

The input and output are 2D grids containing integer values. The non-zero values appear to form distinct "objects" or "blobs", where each object consists of connected cells of the same number (color). The background is represented by zeros.

The core transformation involves rearranging these objects within the grid. The rearrangement happens along a primary axis, either horizontal or vertical.

1.  **Object Identification:** The first step is to identify all distinct connected components of non-zero cells having the same value. Each such component is an "object".
2.  **Axis Determination:** The overall spatial layout of these objects determines the axis of rearrangement. If the bounding box containing all non-zero cells is wider than it is tall, the rearrangement occurs horizontally. Otherwise (if taller or square), it occurs vertically.
3.  **Gap Identification:** The empty space (rows or columns of zeros) between adjacent objects along the primary axis in the input grid is identified. These gaps are preserved in the output.
4.  **Sorting:** The objects are reordered based on a rule that depends on the determined axis:
    *   **Vertical Axis:** Objects are sorted based on their topmost row index (minimum row index) in descending order. The object starting in the lowest row comes first in the output.
    *   **Horizontal Axis:** Objects are sorted based on their color value in descending order, *except* for the object that is rightmost in the input (the one with the largest minimum column index). This rightmost object retains its position as the last object in the sequence after the others are sorted.
5.  **Reconstruction:** The output grid is constructed by placing the objects in their new sorted order, maintaining the original gaps (in terms of width or height) between them along the primary axis. The placement starts from the top (for vertical) or left (for horizontal) edge of the grid, potentially including an initial gap if one existed before the first object in the input.

## Facts


```yaml
task_elements:
  - type: grid
    properties:
      - content: integers (0 for background, non-zero for objects)
      - dimensionality: 2D
  - type: object
    properties:
      - definition: maximal connected component of identical non-zero cells
      - attributes:
          - color: integer value of the cells
          - coordinates: list of (row, col) tuples for cells belonging to the object
          - bounding_box: (min_row, max_row, min_col, max_col)
          - min_row: topmost row index
          - min_col: leftmost column index
  - type: layout
    properties:
      - overall_bounding_box: (min_r, max_r, min_c, max_c) encompassing all non-zero cells
      - overall_height: max_r - min_r + 1
      - overall_width: max_c - min_c + 1
      - primary_axis: derived from overall dimensions ('horizontal' if overall_width > overall_height, else 'vertical')
  - type: gap
    properties:
      - definition: contiguous rows/columns of zeros separating objects along the primary_axis
      - size: number of rows (for vertical axis) or columns (for horizontal axis)
      - location: relative position between objects in the input order

actions:
  - action: identify_objects
    inputs: input_grid
    outputs: list of object descriptions (color, coordinates, bbox, etc.)
  - action: determine_axis
    inputs: list of objects (or overall_bounding_box)
    outputs: primary_axis ('horizontal' or 'vertical')
  - action: identify_gaps
    inputs: input_grid, list of objects, primary_axis
    outputs: list of gap sizes between adjacent objects along the axis in input order
  - action: sort_objects
    inputs: list of objects, primary_axis
    outputs: list of objects in the new order
    logic:
      - if primary_axis is 'vertical': sort by object.min_row descending
      - if primary_axis is 'horizontal': identify rightmost object (max of min_col); sort remaining objects by object.color descending; append rightmost object
  - action: reconstruct_grid
    inputs: output grid dimensions, sorted list of objects, list of gaps
    outputs: output_grid
    logic: place objects and gaps sequentially along the primary axis starting from the top/left

relationships:
  - relationship: object rearrangement
    notes: The core transformation is the reordering of objects.
  - relationship: gap preservation
    notes: The spacing between objects along the primary axis is maintained.
  - relationship: axis-dependent sorting
    notes: The rule for ordering objects depends on whether they are arranged primarily horizontally or vertically.
```


## Natural Language Program

1.  Parse the input grid to identify all distinct connected components (objects) of non-zero cells with the same value. For each object, record its color, its cell coordinates, and its bounding box (minimum/maximum row and column).
2.  Determine the overall bounding box encompassing all identified objects. Calculate the height and width of this overall bounding box.
3.  Determine the primary axis of rearrangement: if the overall width is greater than the overall height, the axis is 'horizontal'; otherwise, the axis is 'vertical'.
4.  Identify the sequence of objects based on their position along the primary axis in the input grid (top-to-bottom for vertical, left-to-right for horizontal).
5.  Calculate the size of the gaps (number of zero rows for vertical axis, number of zero columns for horizontal axis) between consecutive objects in the input sequence along the primary axis. Also, note any gap before the first object.
6.  Determine the target order of the objects based on the primary axis:
    a.  If the axis is 'vertical', sort the list of identified objects based on their minimum row index in descending order.
    b.  If the axis is 'horizontal', identify the object with the maximum minimum column index (the "rightmost" object). Remove this object temporarily. Sort the remaining objects based on their color value in descending order. Append the "rightmost" object to the end of this sorted list.
7.  Create a new empty grid with the same dimensions as the input grid.
8.  Iterate through the newly sorted list of objects and the identified gap sizes. Place the objects and gaps sequentially onto the new grid along the primary axis, starting from the top-left (row 0, col 0). Maintain the original content and relative positions of cells within each object. Ensure the gaps placed between objects have the correct sizes as identified in step 5. Fill any remaining space with zeros.
9.  Return the reconstructed grid as the output.