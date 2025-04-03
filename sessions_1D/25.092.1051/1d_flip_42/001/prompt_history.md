
## train_1

**input:**
```
0 0 0 0 0 3 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 1 1 1 3 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 8 2 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 8 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 8 2 2 2 2 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 8 0 0 0 0 0
```

*   **Perception:**
    *   The input consists of a 1D array (or a 1xN grid) containing mostly white pixels (0).
    *   There are two non-white elements present:
        1.  A single pixel of one color (the "marker"). In the examples, this is green (3) or azure (8).
        2.  A contiguous horizontal block of pixels of another color (the "block"). In the examples, this is blue (1) or red (2).
    *   The marker pixel is always located immediately to the left of the block.
    *   The transformation involves moving the marker pixel from its original position to the position immediately to the right of the block.
    *   The block itself remains unchanged in position and color.
    *   The pixel at the original marker position becomes white (0).

*   **Facts:**
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D # Effectively 1xN
    objects:
      - type: marker_pixel
        count: 1
        properties:
          - color: non-white (distinct from block color)
          - size: 1 pixel
          - initial_position: immediately precedes the block
      - type: color_block
        count: 1
        properties:
          - color: non-white (distinct from marker color)
          - shape: contiguous horizontal line
          - size: variable length (>= 1 pixel)
          - position: immediately follows the marker
    relationships:
      - type: adjacency
        object1: marker_pixel
        object2: color_block
        details: marker is immediately left-adjacent to the block in the input.
    actions:
      - action: move
        object: marker_pixel
        from: initial position (left of block)
        to: position immediately right of the block
      - action: recolor
        location: initial position of marker_pixel
        new_color: white (0)
    background: white (0)
    ```


*   **Natural Language Program:**
    1.  Scan the input array to find the non-white pixels.
    2.  Identify the single pixel that is immediately followed by a different non-white color; this is the "marker" pixel. Record its color and original index.
    3.  Identify the contiguous sequence of the *other* non-white color that follows the marker; this is the "block". Record the index of the last pixel in this block.
    4.  Create a copy of the input array to serve as the output.
    5.  Set the pixel at the marker's original index in the output array to white (0).
    6.  Set the pixel at the index immediately following the last pixel of the block in the output array to the marker's color.
    7.  Return the modified output array.
