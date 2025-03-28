
## train_1

**input:**
```
9 9 7 7 7 7 7 7 7 7
9 8 7 7 7 8 1 1 7 7
7 7 7 7 7 1 1 1 7 7
7 7 7 7 7 1 1 1 7 7
7 7 7 7 7 1 1 1 7 7
7 7 7 7 7 7 7 7 7 7
7 5 5 5 5 8 7 7 7 7
7 5 5 5 5 5 7 7 7 7
7 5 5 5 5 5 7 7 7 7
7 5 5 5 5 5 7 7 7 7
```


**output:**
```
7 7 7 7 1 1 1 7 7 7
7 9 9 7 1 1 1 7 7 7
7 9 9 7 1 1 1 7 7 7
7 7 7 7 1 1 1 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 7 7 7
7 7 7 7 7 7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7 7 7
7 2 2 2 2 8 7 7 7 7
7 2 2 2 2 2 7 7 7 7
7 2 2 2 2 2 7 7 7 7
7 2 2 2 2 2 7 7 7 7
7 2 2 2 2 2 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 8 6 6 6 7
7 7 7 7 7 6 6 6 6 7
7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 2 2 2 2 2 7 7 7
7 7 2 2 2 2 2 7 7 7
7 7 2 2 2 2 2 7 7 7
7 7 2 2 2 2 2 7 7 7
7 7 2 2 2 2 2 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 6 6 6 6 7 7
7 7 7 7 6 6 6 6 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 9 9 9 7
2 2 2 2 7 7 7 9 9 9 7
2 2 2 2 7 7 7 9 9 9 7
2 2 2 2 7 7 7 9 9 8 7
2 2 2 8 7 7 7 7 3 3 3
7 7 7 7 7 7 7 7 3 3 3
7 7 7 7 7 7 7 7 8 3 3
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 9 9 9
7 2 2 2 2 7 7 7 9 9 9
7 2 2 2 2 7 7 7 9 9 9
7 2 2 2 2 7 7 7 9 9 9
7 2 2 2 2 7 7 3 3 3 7
7 7 7 7 7 7 7 3 3 3 7
7 7 7 7 7 7 7 3 3 3 7
7 7 7 7 7 7 7 7 7 7 7
```

*   **Perception of the Elements:**
    *   Each input grid contains several distinct objects composed of pixels of a single color, set against a background color (Orange=7 in all examples).
    *   There are also isolated pixels of Azure (8).
    *   Each Azure pixel appears to be adjacent (sharing an edge or corner) to exactly one of the larger colored objects.
    *   In the output grids, the larger colored objects have shifted their positions by one pixel.
    *   The Azure pixels present in the input are absent in the output, replaced by the background color.
    *   The direction of the shift for each object seems to be determined by the relative position of the adjacent Azure pixel. The object moves "towards" the Azure pixel.
    *   The space previously occupied by the moved object is filled with the background color (Orange=7).

*   **Facts:**
    
```yaml
    task_context:
      background_color: 7 # Orange
      marker_color: 8 # Azure
    
    objects:
      - type: contiguous_shape
        description: Blocks of pixels with the same color, excluding the background color and the marker color.
        properties:
          - color: The specific color of the shape (e.g., Maroon=9, Blue=1, Gray=5, Red=2, Magenta=6, Green=3).
          - pixels: List of coordinates for each pixel in the shape.
      - type: marker
        description: Single pixels of the marker color (Azure=8).
        properties:
          - color: 8
          - position: Coordinate of the marker pixel.
    
    relationships:
      - type: adjacency
        description: A marker pixel is adjacent (shares an edge or corner) to exactly one contiguous_shape object. Each contiguous_shape object has exactly one adjacent marker pixel.
    
    actions:
      - action: identify_background_marker
        description: Determine the background color (most frequent color) and the marker color (Azure=8).
      - action: identify_objects
        description: Find all contiguous shapes (not background or marker) and all marker pixels.
      - action: determine_adjacency
        description: For each shape, find the unique adjacent marker pixel.
      - action: calculate_translation
        description: For each shape, calculate the 1-step translation vector required to move the shape towards its adjacent marker pixel.
      - action: apply_translation
        description: Create the output grid initialized with the background color. For each shape, place its translated version onto the output grid.
        details:
          - The original position of the shape in the input is filled with the background color in the output.
          - The marker pixels from the input are not copied to the output; their positions are filled with the background color.
    
    goal:
      description: Move each identified shape one step towards its adjacent marker pixel, removing the marker pixel and filling the vacated space with the background color.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with the background color (Orange=7).
    2.  Identify all contiguous shapes in the input grid that are *not* the background color (Orange=7) and *not* the marker color (Azure=8).
    3.  For each identified shape:
        a.  Find the single Azure (8) pixel that is adjacent (shares an edge or corner) to any pixel of this shape.
        b.  Determine the direction of translation (up, down, left, right, or diagonal) from the shape towards the adjacent Azure pixel. This is a one-step move. For example, if the Azure pixel is directly to the right of a shape pixel, the translation is one step right (+1 column). If it's diagonally down-left, the translation is one step down (+1 row) and one step left (-1 column).
        c.  Apply this one-step translation to all pixels belonging to the current shape.
        d.  Draw the translated shape onto the output grid using its original color.
    4.  Return the completed output grid. (Note: The Azure pixels are implicitly removed because the output grid starts empty and only the translated shapes are drawn).
