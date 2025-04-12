**Perception**

1.  **Input Structure:** The input grids contain multiple distinct objects composed of colored pixels (1-9) set against a white (0) background.
2.  **Object Types:** There are primary shapes (like 'H', diamond, square) and a specific "separator" object (a vertical green line in `train_1`, a horizontal magenta bar in `train_2`).
3.  **Separation:** The separator object divides the grid into distinct regions (left/right for a vertical separator, top/bottom for a horizontal separator). The other non-white objects reside entirely within these separate regions.
4.  **Transformation:** The transformation involves identifying the non-separator objects, extracting them based on their minimal bounding boxes, and then concatenating these extracted shapes. The separator object and the original background are discarded.
5.  **Concatenation Logic:** If the separator is vertical, the objects are concatenated horizontally (left object then right object). If the separator is horizontal, the objects are concatenated vertically (top object then bottom object).
6.  **Output Structure:** The output grid contains only the extracted primary shapes placed adjacent to each other, with no separator or original background. The dimensions of the output grid depend on the dimensions of the extracted shapes and the concatenation direction.

**Facts**


```yaml
task_context: The task involves isolating specific shapes from an input grid by removing a separator element and the background, then combining the isolated shapes.
elements:
  - type: background
    properties:
      color: white (0)
  - type: shape
    properties:
      color: non-white (1-9)
      contiguity: pixels of the same color are connected
      role: primary_object or separator
  - type: primary_object
    description: The shapes intended to be extracted and combined in the output.
    properties:
      - bounding_box: The minimal rectangle containing all pixels of the object.
      - position: Location within the input grid (e.g., top-left coordinates).
  - type: separator
    description: A specific object that divides the grid and separates the primary objects.
    properties:
      - shape: Typically a line or bar (vertical or horizontal rectangle).
      - orientation: vertical or horizontal.
      - function: Partitions the grid, separating other objects.
relationships:
  - type: spatial_separation
    description: The separator object divides the grid, placing primary objects into distinct regions (e.g., left/right, top/bottom).
    properties:
      - axis: horizontal or vertical
      - separator: the object performing the separation
      - separated_objects: list of primary objects
  - type: adjacency
    description: In the output, the extracted primary objects are placed directly next to each other.
    properties:
      - direction: horizontal or vertical (determined by separator orientation)
      - order: Based on original relative positions (left-to-right or top-to-bottom)
actions:
  - action: identify_objects
    description: Find all distinct contiguous regions of non-white pixels.
  - action: identify_separator
    description: Distinguish the separator object from primary objects based on its shape (line/bar) and its function of partitioning the grid.
  - action: determine_separator_orientation
    description: Check if the separator is taller than wide (vertical) or wider than tall (horizontal).
  - action: filter_objects
    description: Select only the primary (non-separator) objects for further processing.
  - action: extract_bounding_box
    description: For each selected primary object, find its minimal bounding box and extract the corresponding subgrid from the input.
  - action: sort_objects
    description: Order the extracted subgrids based on the original spatial position of their corresponding objects relative to the separator axis.
  - action: concatenate_subgrids
    description: Combine the sorted, extracted subgrids along the axis orthogonal to the separator's orientation (horizontally for a vertical separator, vertically for a horizontal separator).
```


**Natural Language Program**

1.  Identify all connected components (objects) of non-white pixels in the input grid.
2.  Determine which object serves as the separator. The separator is typically a rectangular line or bar shape (either vertically or horizontally oriented) that divides the grid such that all other non-white objects lie entirely on one side of it or the other.
3.  Note the orientation of the separator (vertical or horizontal).
4.  Isolate the non-white objects that are *not* the separator (these are the primary objects).
5.  For each primary object:
    a. Calculate its minimal bounding box (the smallest rectangle enclosing all its pixels).
    b. Extract the subgrid corresponding to this bounding box.
6.  If the separator's orientation is vertical:
    a. Sort the extracted subgrids based on the horizontal position (left-to-right) of their corresponding objects in the original input grid.
    b. Concatenate these sorted subgrids horizontally.
7.  If the separator's orientation is horizontal:
    a. Sort the extracted subgrids based on the vertical position (top-to-bottom) of their corresponding objects in the original input grid.
    b. Concatenate these sorted subgrids vertically.
8.  The resulting concatenated grid is the final output.