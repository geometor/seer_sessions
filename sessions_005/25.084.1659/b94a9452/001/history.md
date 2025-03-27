
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 1 3 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3
3 1 3
3 3 3
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0 0
0 0 0 2 4 4 2 0 0 0 0 0 0
0 0 0 2 4 4 2 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4
4 2 2 4
4 2 2 4
4 4 4 4
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 6 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6
6 6 6 6 6
6 6 4 6 6
6 6 6 6 6
6 6 6 6 6
```

*   **Perception:** The task involves identifying a single, distinct non-background (non-white) object within a larger input grid. This object is always composed of exactly two different non-white colors. The transformation extracts this object and then swaps the two non-white colors within it to produce the output grid. The output grid's dimensions match the bounding box of the identified object in the input.

*   **YAML Facts:**
    
```yaml
    task_description: Extract a multi-colored object and swap its constituent colors.
    
    elements:
      - element: background
        color: white (0)
        role: Surrounds the main object, ignored in the transformation.
      - element: object
        description: A single contiguous block of non-white pixels.
        properties:
          - consists of exactly two distinct non-white colors (color1, color2).
          - forms a specific shape (e.g., square with a center pixel, square with a 2x2 center).
          - located somewhere within the input grid.
        actions:
          - identify: Find the bounding box containing all non-white pixels.
          - extract: Crop the input grid to this bounding box.
      - element: color1
        description: One of the two non-white colors comprising the object.
      - element: color2
        description: The other non-white color comprising the object.
    
    transformation:
      - action: swap_colors
        input: extracted object grid, color1, color2
        output: new grid
        logic: Iterate through the extracted grid. Replace all instances of color1 with color2, and all instances of color2 with color1.
    
    relationships:
      - The output grid has the same dimensions as the bounding box of the object in the input grid.
      - The pattern of pixels within the object is preserved, but the colors assigned to the pattern elements are swapped.
    
    examples_summary:
      - train_1: Blue (1) and Green (3) swapped within a 3x3 object.
      - train_2: Red (2) and Yellow (4) swapped within a 4x4 object.
      - train_3: Yellow (4) and Magenta (6) swapped within a 5x5 object.
    ```


*   **Natural Language Program:**
    1.  Identify all non-white pixels in the input grid.
    2.  Determine the minimum bounding box that encloses all these non-white pixels.
    3.  Extract the subgrid corresponding to this bounding box.
    4.  Identify the two distinct non-white colors present within this extracted subgrid (let's call them `color_A` and `color_B`).
    5.  Create a new output grid with the same dimensions as the extracted subgrid.
    6.  Iterate through each pixel of the extracted subgrid:
        *   If the pixel's color is `color_A`, set the color of the corresponding pixel in the output grid to `color_B`.
        *   If the pixel's color is `color_B`, set the color of the corresponding pixel in the output grid to `color_A`.
    7.  Return the newly created output grid.
