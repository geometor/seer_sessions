
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 5 0 0 0 0 2 0 0 2 0 0
0 2 2 2 2 0 0 0 0 2 0 0 0 0 0 0 0
0 2 0 0 2 0 4 0 0 0 0 0 5 0 0 0 0
0 2 0 0 2 0 0 0 0 0 0 0 0 0 0 2 0
0 2 2 2 2 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0 4 0 0 5 0
0 2 0 0 5 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 4 0 0 4 0 5 5 5 5
0 0 0 0 0 4 0 0 4 0 0 0 0 5 0 0 5
0 4 0 5 0 4 4 4 4 0 0 0 2 5 0 0 5
0 0 0 0 0 0 0 0 0 0 5 0 0 5 5 5 5
0 0 5 0 0 0 0 0 0 0 0 0 5 0 0 0 0
```


**output:**
```
2 2 2 2 4 4 4 4 5 5 5 5
2 0 0 2 4 0 0 4 5 0 0 5
2 0 0 2 4 0 0 4 5 0 0 5
2 2 2 2 4 4 4 4 5 5 5 5
```


## train_2

**input:**
```
0 3 0 0 3 0 0 0 0 8 0 0 0 1 0 0 0 7 0 3 0
0 8 8 8 0 0 8 0 7 0 0 3 0 0 0 7 3 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0 8
0 8 8 8 0 3 3 3 3 0 0 0 0 1 1 1 0 0 0 0 0
1 0 0 0 0 3 3 3 0 0 3 0 0 1 1 1 0 0 1 0 0
0 0 0 8 0 3 3 3 0 0 0 0 1 1 1 1 0 0 0 8 0
1 0 0 0 0 0 0 0 0 8 0 0 0 0 7 0 0 0 0 0 0
0 0 0 1 0 0 0 7 0 0 0 0 0 0 0 0 0 8 7 7 7
0 8 0 0 0 0 8 0 0 3 3 3 0 3 0 0 0 0 7 7 7
0 0 0 3 0 0 0 0 0 3 3 3 0 0 0 0 0 0 7 7 7
0 3 0 0 0 0 3 0 0 3 3 3 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 1 0 0 3 0 0 0 1
```


**output:**
```
8 8 8 3 3 3 3 3 3 1 1 1 7 7 7
8 8 8 3 3 3 3 3 3 1 1 1 7 7 7
8 8 8 3 3 3 3 3 3 1 1 1 7 7 7
```

*   **Perception:** The input grid contains scattered objects of various colors and shapes on a white background. The output grid is smaller and consists of solid squares of color, arranged horizontally. The colors in the output correspond to the colors of specific objects in the input. The key transformation involves identifying objects in the input whose bounding boxes are perfect squares, determining the size 'N' of these squares from the first one found, creating solid NxN squares for each such object, and arranging these squares horizontally in the output based on their original position.

*   **Facts:**
    
```yaml
    task_type: object_extraction_and_arrangement
    element_type: objects (contiguous non-background pixels)
    background_color: 0 (white)
    object_properties:
      - color: integer 1-9
      - shape: various, some have square bounding boxes
      - bounding_box: minimum rectangle enclosing the object
    parameters:
      - square_size_N: determined by the height/width of the bounding box of the first object encountered (scanning top-to-bottom, left-to-right) whose bounding box is square.
    actions:
      - identify_objects: find all contiguous groups of non-background pixels.
      - calculate_bounding_box: determine the minimum enclosing rectangle for each object.
      - filter_objects: select only objects whose bounding box dimensions are exactly N x N.
      - sort_objects: arrange the selected objects based on the row, then column index of the top-left corner of their bounding box.
      - create_solid_squares: generate an N x N grid filled with the color of each selected object.
      - concatenate_squares: combine the generated N x N squares horizontally in the sorted order.
    relationships:
      - input_output_colors: Colors of the output squares match the colors of the selected input objects.
      - output_dimensions: Output height is N, output width is N * (number of selected objects).
      - object_selection_criteria: Bounding box must be N x N.
      - arrangement_order: Determined by the top-left coordinate of the bounding box in the input grid (row-major).
    ```


*   **Natural Language Program:**
    1.  Determine the characteristic square size `N` for the task: Scan the input grid row by row, then column by column. Find the first non-background pixel that belongs to an object whose bounding box is a perfect square (height equals width). Set `N` to be the side length of this first square bounding box.
    2.  Identify all distinct contiguous objects (groups of connected pixels of the same color, excluding the background color 0).
    3.  For each identified object, calculate its bounding box (the smallest rectangle enclosing all its pixels).
    4.  Filter these objects, keeping only those whose bounding box dimensions are exactly `N` rows by `N` columns.
    5.  Sort the filtered objects based on the coordinate of the top-left corner of their bounding box, primarily by row index (top to bottom) and secondarily by column index (left to right).
    6.  Create a new output grid with height `N` and width equal to `N` multiplied by the number of filtered objects.
    7.  For each filtered object, in the sorted order, create an `N`x`N` square filled entirely with that object's color.
    8.  Place these `N`x`N` colored squares sequentially into the output grid from left to right.
