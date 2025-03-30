**Perception**

The input grids contain a white background (0) and multiple distinct objects composed of azure (8) pixels. These azure objects often resemble numerical digits formed on a grid, similar to a seven-segment display, but can also be other connected shapes. The output grids retain the exact shapes and positions of the azure objects from the input, but the azure color (8) is replaced with other colors: blue (1), red (2), green (3), or yellow (4). The white background remains unchanged.

The core transformation involves identifying each separate azure object, determining a specific color for each object based on a rule, and then recoloring all pixels of that object with its assigned color. The rule for assigning colors appears to depend on the total number of azure objects found in the input grid and the order in which these objects are encountered (e.g., determined by scanning top-to-bottom, left-to-right based on the object's top-leftmost pixel). A specific sequence of colors is assigned to the ordered objects, and this sequence itself is determined by the total object count.

**Facts**


```yaml
elements:
  - element: grid
    properties:
      - contains pixels of different colors (0-9)
      - background color is white (0)
  - element: object
    properties:
      - contiguous group of non-background pixels
      - in input grids, objects are composed solely of azure (8) pixels
      - objects often resemble digit shapes but are defined by connectivity
      - objects maintain their shape and position in the output
      - objects are assigned a new color in the output based on a rule
objects:
  - object: azure_shape
    description: A contiguous block of azure (8) pixels in the input grid.
    properties:
      - color: azure (8)
      - shape: preserved in output
      - position: preserved in output
    count: Variable (N per grid, observed N=3, N=4, N=5 in examples)
relationships:
  - type: identity
    description: Each azure object in the input corresponds to exactly one colored object in the output at the same location and with the same shape.
  - type: ordering
    description: Azure objects are implicitly ordered, likely based on their top-most, then left-most coordinate. Let this order be O_1, O_2, ..., O_N.
  - type: color_assignment
    description: The output color assigned to object O_i depends on its index 'i' and the total number of objects 'N'.
    details: Specific color sequences are used based on N.
      - If N=3, the color sequence assigned to (O_1, O_2, O_3) is [blue(1), blue(1), green(3)].
      - If N=4, the color sequence assigned to (O_1, O_2, O_3, O_4) is [red(2), blue(1), green(3), blue(1)].
      - If N=5, the color sequence assigned to (O_1, O_2, O_3, O_4, O_5) is [yellow(4), yellow(4), green(3), red(2), blue(1)].
actions:
  - action: find_objects
    input: input grid
    output: list of distinct azure (8) objects, identified by their pixel coordinates
  - action: count_objects
    input: list of objects
    output: total number of objects (N)
  - action: order_objects
    input: list of objects
    output: ordered list of objects (O_1, ..., O_N), based on top-left coordinate
  - action: select_color_sequence
    input: object count (N)
    output: specific sequence of colors based on N (using predefined mapping for N=3, 4, 5)
  - action: recolor_objects
    input:
      - output grid (initially a copy of input)
      - ordered list of objects (O_1, ..., O_N)
      - color sequence (C_1, ..., C_N)
    output: modified output grid where pixels of object O_i are changed to color C_i
```


**Natural Language Program**

1.  Identify all distinct contiguous objects composed of azure (8) pixels in the input grid.
2.  Count the total number of these azure objects found (let the count be N).
3.  Determine the order of these objects based on their spatial position: sort them primarily by the row index of their top-most pixel, and secondarily by the column index of their left-most pixel. Let the ordered objects be O_1, O_2, ..., O_N.
4.  Select a specific sequence of output colors based on the total object count N:
    *   If N is 3, the color sequence is [blue, blue, green].
    *   If N is 4, the color sequence is [red, blue, green, blue].
    *   If N is 5, the color sequence is [yellow, yellow, green, red, blue].
    *   (Assume a rule exists or can be inferred for other values of N if encountered).
5.  Create the output grid, initially identical to the input grid.
6.  For each object O_i (from i=1 to N) in the ordered list, find the i-th color (C_i) in the selected color sequence.
7.  Change the color of all pixels belonging to object O_i in the output grid to the assigned color C_i.
8.  Leave all background (white, 0) pixels unchanged.
9.  The final modified grid is the result.