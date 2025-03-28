
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 8 2 2 8 8 8 8 8 0 0 0 0 0
0 0 8 2 2 8 8 8 8 8 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 8 8 8 8 8 3 3 8 0 0 0 0 0
0 0 8 8 8 8 8 3 3 8 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0
0 3
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 8 8 8 8 0
0 8 8 8 8 8 8 8 8 8 8 8 8 8 0
0 8 8 1 1 8 8 8 3 3 8 8 8 8 0
0 8 8 1 1 8 8 8 3 3 8 8 8 8 0
0 8 8 8 8 8 8 8 8 8 8 8 8 8 0
0 8 8 8 8 8 8 8 2 2 8 8 8 8 0
0 8 8 8 8 8 8 8 2 2 8 8 8 8 0
0 8 8 8 8 8 8 8 8 8 8 8 8 8 0
0 8 8 8 8 8 8 8 8 8 8 8 8 8 0
0 8 8 8 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 3
0 2
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 8 5 5 8 8 4 4 8 8 0 0 0 0 0 0
0 8 5 5 8 8 4 4 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 8 3 3 8 8 8 8 8 8 0 0 0 0 0 0
0 8 3 3 8 8 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 4
3 0
```

*   **perception**
    *   The input grids feature a large, irregular shape made of azure (8) pixels, surrounded by a white (0) background.
    *   Within this azure shape, there are smaller, solid rectangular blocks of other colors (e.g., red, green, blue, gray, yellow). These colored blocks do not touch the outer white background directly; they are fully enclosed by the azure pixels.
    *   The output grids are always 2x2.
    *   The colors present in the output grid (excluding white) are the same colors as the rectangular blocks found inside the azure shape in the input grid.
    *   The position of a color in the 2x2 output grid corresponds to the approximate quadrant (top-left, top-right, bottom-left, bottom-right) where the corresponding colored block is located within the bounding box of the main azure shape.
    *   If a quadrant within the azure shape's bounding box does not contain a colored block, the corresponding cell in the output 2x2 grid is white (0).

*   **facts**
    
```yaml
    objects:
      - type: background
        color: white (0)
        location: surrounds other shapes
      - type: container
        color: azure (8)
        shape: large, irregular, contiguous
        location: encloses smaller objects
      - type: content
        color: various (red, green, blue, gray, yellow, etc., excluding white and azure)
        shape: small, rectangular, solid
        location: fully inside the container object
        count: variable (1 to 3 in examples)
    relationships:
      - container encloses content objects
      - content objects are spatially separated within the container
      - position of content object within container's bounds determines output position
    actions:
      - identify the container object (azure)
      - determine the bounding box of the container object
      - calculate the center (horizontal and vertical dividing lines) of the container's bounding box
      - identify all content objects (non-white, non-azure) inside the container
      - for each content object, determine which quadrant (TL, TR, BL, BR) relative to the container's center it resides in
      - create a 2x2 output grid, initialized to white (0)
      - place the color of each content object into the corresponding quadrant cell of the output grid
    output_grid:
      - dimensions: 2x2
      - cell_mapping:
          - Top-Left (TL) quadrant -> output[0, 0]
          - Top-Right (TR) quadrant -> output[0, 1]
          - Bottom-Left (BL) quadrant -> output[1, 0]
          - Bottom-Right (BR) quadrant -> output[1, 1]
      - cell_value: color of the content object in the corresponding quadrant, or white (0) if no content object exists in that quadrant
    ```


*   **natural language program**
    1.  Identify the largest contiguous object composed of azure (8) pixels in the input grid. This is the 'container'.
    2.  Determine the bounding box of the container object (minimum and maximum row and column indices).
    3.  Calculate the coordinates of the center point (or the vertical and horizontal center lines) of the container's bounding box.
    4.  Initialize a 2x2 output grid with all cells set to white (0).
    5.  Find all distinct contiguous objects within the input grid that are composed of colors other than white (0) and azure (8). These are the 'content' objects.
    6.  For each content object:
        a.  Determine its representative location (e.g., the coordinates of its top-left pixel or its centroid).
        b.  Compare the content object's location to the center lines of the container's bounding box to determine which quadrant it falls into: Top-Left, Top-Right, Bottom-Left, or Bottom-Right.
        c.  Based on the determined quadrant, update the corresponding cell in the 2x2 output grid with the color of the content object:
            *   Top-Left quadrant: Update cell (0, 0).
            *   Top-Right quadrant: Update cell (0, 1).
            *   Bottom-Left quadrant: Update cell (1, 0).
            *   Bottom-Right quadrant: Update cell (1, 1).
    7.  Return the final 2x2 output grid.
