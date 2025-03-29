
## train_1

**input:**
```
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 0 4 0 0 0 0 2 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0
1 4 1 1 1 8 1 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 8 0 0
1 1 1 1 1 1 1 0 0 8 0 8 0
1 1 1 1 1 1 1 0 0 0 8 0 0
1 3 1 1 1 2 1 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0
```


**output:**
```
0 4 0 0 0 8 0
4 4 4 0 8 0 8
0 4 0 0 0 8 0
0 0 0 0 0 0 0
3 0 3 0 2 2 0
3 3 0 0 2 0 2
0 3 0 0 0 2 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 2 0 0 0 0 0 1 2 1 1 1 4 1
0 0 2 2 2 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 2 2 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 1 6 1 1 1 3 1
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 2 0 0 4 0
2 2 2 0 4 4 4
0 2 2 0 0 4 4
0 0 0 0 0 0 0
6 0 6 0 3 3 0
0 6 0 0 3 0 3
6 6 6 0 0 3 0
```


## train_3

**input:**
```
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 5 1 1 1 4 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 4 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 4 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 4 4 4 0 0 0 0
1 2 1 1 1 3 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0 6 0 0
0 0 3 0 3 0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 3 3 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 5 0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 0 0 0 0 4
5 5 0 0 0 4 0
0 0 5 0 4 4 4
0 0 0 0 0 0 0
0 2 0 0 3 0 3
2 0 2 0 0 3 3
2 2 2 0 0 0 3
```

*   **Perception:** The input grid consistently features a large rectangular frame made of blue (1) pixels. Inside this frame, at specific locations (often corners relative to the frame's internal area), there are single pixels of other colors (excluding blue and white). Outside the blue frame, there are distinct shapes (connected components of non-white pixels) corresponding in color to the single pixels found inside the frame. The output grid contains only these shapes from outside the frame, rearranged. The arrangement of the shapes in the output grid mirrors the relative spatial arrangement of their corresponding single-colored "key" pixels within the blue frame. The shapes in the output maintain their original structure and are separated by a single row/column of white (0) pixels.

*   **Facts:**
    
```yaml
    task_elements:
      - Input Grid: 2D array of integers (0-9).
      - Output Grid: Smaller 2D array of integers (0-9).

    objects:
      - type: Frame
        description: The largest connected component of blue (1) pixels in the input grid. Typically forms a rectangle.
        properties:
          - color: 1 (blue)
          - connectivity: Largest component
          - shape: Rectangular (usually hollow)
          - location: Variable within the input grid.
          - bounding_box: The min/max row/col containing the frame pixels.
      - type: Key Pixel
        description: Single pixels of non-blue(1), non-white(0) color located within the bounding box of the blue Frame.
        properties:
          - color: Any color except 0 or 1.
          - size: 1x1 pixel.
          - location: Within the Frame's bounding box.
          - role: Acts as a selector for a Target Shape of the same color.
          - relative_position: Its position relative to other Key Pixels within the Frame's bounding box (e.g., top-left, bottom-right).
      - type: Target Shape
        description: Connected components of non-white(0) pixels located entirely outside the bounding box of the blue Frame.
        properties:
          - color: Matches the color of a Key Pixel.
          - connectivity: Forms a contiguous shape.
          - location: Outside the Frame's bounding box.
          - role: Selected by a Key Pixel of the same color.
          - structure: The specific arrangement of pixels forming the shape.

    relationships:
      - type: Selection
        description: Each Key Pixel selects one Target Shape.
        condition: The color of the Key Pixel must match the color of the Target Shape.
        scope: Only Target Shapes outside the Frame's bounding box are considered.
      - type: Arrangement
        description: The relative spatial arrangement of the Target Shapes in the Output Grid corresponds to the relative spatial arrangement of their respective Key Pixels within the Frame's bounding box.
      - type: Spacing
        description: Selected Target Shapes are placed in the output grid such that adjacent shapes (horizontally or vertically based on the key pixel arrangement) are separated by exactly one row or column of white (0) pixels.

    transformations:
      - Identify and isolate the blue Frame object and its bounding box.
      - Identify all Key Pixels within the Frame's bounding box. Record their colors and relative positions.
      - Identify all potential Target Shapes outside the Frame's bounding box.
      - For each Key Pixel, select the Target Shape of the matching color.
      - Determine the minimum bounding box required to contain all selected Target Shapes, arranged according to the relative positions of their corresponding Key Pixels, with a 1-pixel white border inserted between adjacent shapes.
      - Create the output grid of the determined size, initially filled with white (0).
      - Place each selected Target Shape into the output grid at the determined position, preserving its original pixel structure.
    ```


*   **Natural Language Program:**
    1.  Identify the largest connected component of blue (1) pixels in the input grid; this is the "Frame". Determine the bounding box of this Frame.
    2.  Scan the area within the Frame's bounding box to find all single pixels whose color is not blue (1) or white (0). These are the "Key Pixels". Store the color and coordinates of each Key Pixel.
    3.  Identify all connected components of non-white (0) pixels that lie entirely outside the Frame's bounding box. These are the potential "Target Shapes". Store the shape (pixel coordinates and colors) and the primary color of each potential Target Shape.
    4.  Create a list of "Selected Shapes" by matching each Key Pixel's color to the color of a potential Target Shape found in step 3.
    5.  Determine the relative spatial arrangement of the Key Pixels within the Frame's bounding box (e.g., which key is top-left, top-right, bottom-left, bottom-right relative to the others).
    6.  Calculate the dimensions required for the output grid. This involves arranging the bounding boxes of the Selected Shapes according to the relative arrangement of their corresponding Key Pixels, adding a 1-pixel gap (white color 0) between shapes that are adjacent in the arrangement (horizontally or vertically), and finding the total height and width.
    7.  Initialize the output grid with the calculated dimensions, filled with the background color (white, 0).
    8.  Place each Selected Shape into the output grid at its calculated position, preserving its internal structure, based on the arrangement determined in step 5 and the spacing rules.
