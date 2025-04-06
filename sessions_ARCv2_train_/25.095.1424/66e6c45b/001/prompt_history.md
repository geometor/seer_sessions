
## train_1

**input:**
```
0 0 0 0
0 5 6 0
0 8 3 0
0 0 0 0
```


**output:**
```
5 0 0 6
0 0 0 0
0 0 0 0
8 0 0 3
```


## train_2

**input:**
```
0 0 0 0
0 3 4 0
0 7 6 0
0 0 0 0
```


**output:**
```
3 0 0 4
0 0 0 0
0 0 0 0
7 0 0 6
```

*   **Perception:**
    *   The input and output are both 4x4 grids containing single-digit integers.
    *   The input grid features a 2x2 block of non-zero digits surrounded by zeros.
    *   The output grid has zeros everywhere except for the four corner cells.
    *   The non-zero digits from the input's 2x2 block are relocated to the corners of the output grid.
    *   The relative positions within the 2x2 block correspond to the corner positions in the output:
        *   Top-left of the 2x2 block maps to the top-left corner of the output.
        *   Top-right of the 2x2 block maps to the top-right corner of the output.
        *   Bottom-left of the 2x2 block maps to the bottom-left corner of the output.
        *   Bottom-right of the 2x2 block maps to the bottom-right corner of the output.

*   **Facts:**
    
```yaml
    - object: Input Grid
      properties:
        - type: 2D array (4x4)
        - contains: integers (0-9)
        - structure: a central 2x2 block of non-zero digits surrounded by zeros
    - object: Output Grid
      properties:
        - type: 2D array (4x4)
        - contains: integers (0-9)
        - structure: non-zero digits only at the four corner cells, zeros elsewhere
    - object: Non-zero Block
      properties:
        - size: 2x2
        - location: central region of the Input Grid
        - elements: [top_left, top_right, bottom_left, bottom_right]
    - object: Corner Cells (Output)
      properties:
        - locations: [(0,0), (0,3), (3,0), (3,3)]
    - action: Identify
      actor: Transformation Rule
      target: Non-zero Block within Input Grid
    - action: Extract
      actor: Transformation Rule
      source: Non-zero Block elements
    - action: Create
      actor: Transformation Rule
      result: Output Grid (initialized with zeros)
    - action: Place
      actor: Transformation Rule
      source_elements: Elements from Non-zero Block
      target_locations: Corner Cells of Output Grid
    - relationship: Mapping
      from: Non-zero Block elements (relative position)
      to: Output Grid corner cells (absolute position)
      details:
        - Non-zero Block top-left -> Output Grid (0,0)
        - Non-zero Block top-right -> Output Grid (0,3)
        - Non-zero Block bottom-left -> Output Grid (3,0)
        - Non-zero Block bottom-right -> Output Grid (3,3)
    ```


*   **Natural Language Program:**
    1.  Initialize a new 4x4 grid with all cells set to 0. This will be the output grid.
    2.  Locate the 2x2 subgrid within the input grid that contains non-zero numbers.
    3.  Identify the four numbers within this 2x2 subgrid and their positions (top-left, top-right, bottom-left, bottom-right).
    4.  Place the number from the top-left position of the identified 2x2 subgrid into the top-left corner (row 0, column 0) of the output grid.
    5.  Place the number from the top-right position of the identified 2x2 subgrid into the top-right corner (row 0, column 3) of the output grid.
    6.  Place the number from the bottom-left position of the identified 2x2 subgrid into the bottom-left corner (row 3, column 0) of the output grid.
    7.  Place the number from the bottom-right position of the identified 2x2 subgrid into the bottom-right corner (row 3, column 3) of the output grid.
    8.  Return the modified output grid.
