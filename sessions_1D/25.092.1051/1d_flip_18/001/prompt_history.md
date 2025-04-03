
## train_1

**input:**
```
0 0 0 0 0 4 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 4 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 2 2 2 2 2 2 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 1 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 3 3 3 3 3 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 3 5 0 0 0 0 0 0 0 0
```

*   **Perception:**
    The input and output are 1D grids (or 1xN arrays). Each input contains a sequence of pixels, mostly white (0), but also includes two distinct non-white objects placed adjacent to each other. One object is always a single pixel of one color, and the other object is a contiguous block of pixels of another color. The output grid is identical to the input grid, except that the positions of the single non-white pixel and the adjacent block of non-white pixels are swapped. The white background pixels remain unchanged.

*   **Facts:**
    
```yaml
    examples:
      train_1:
        input: [0, 0, 0, 0, 0, 4, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0] # 1x17 grid
        output: [0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 4, 0, 0, 0, 0, 0, 0] # 1x17 grid
        objects_input:
          - color: 4 (yellow)
            pixels: [[0, 5]] # (row, col) assuming 1 row
            shape: single pixel
          - color: 5 (gray)
            pixels: [[0, 6], [0, 7], [0, 8], [0, 9], [0, 10]]
            shape: horizontal block (length 5)
        relationship: The yellow pixel is immediately to the left of the gray block.
        action: Swap the positions of the yellow pixel and the gray block.
      train_2:
        input: [0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0] # 1x17 grid
        output: [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0] # 1x17 grid
        objects_input:
          - color: 1 (blue)
            pixels: [[0, 4]]
            shape: single pixel
          - color: 2 (red)
            pixels: [[0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11]]
            shape: horizontal block (length 7)
        relationship: The blue pixel is immediately to the left of the red block.
        action: Swap the positions of the blue pixel and the red block.
      train_3:
        input: [0, 0, 5, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0] # 1x17 grid
        output: [0, 0, 3, 3, 3, 3, 3, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0] # 1x17 grid
        objects_input:
          - color: 5 (gray)
            pixels: [[0, 2]]
            shape: single pixel
          - color: 3 (green)
            pixels: [[0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8]]
            shape: horizontal block (length 6)
        relationship: The gray pixel is immediately to the left of the green block.
        action: Swap the positions of the gray pixel and the green block.
    grid_properties:
      dimensionality: 1D (or 1xN 2D)
      background_color: 0 (white)
      transformation_type: object rearrangement
    object_properties:
      - Two non-background objects per grid.
      - Objects are contiguous blocks of a single color.
      - One object is always a single pixel.
      - The other object is a block of one or more pixels.
      - The two objects are always adjacent.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through the input grid to find the start and end indices of all contiguous blocks of non-white (non-zero) pixels. Store these blocks along with their colors and pixel indices.
    3.  Identify the two adjacent non-white blocks. Let Block A be the block that appears first (leftmost) and Block B be the block that appears second (rightmost).
    4.  Determine the pixel indices occupied by Block A and Block B.
    5.  In the output grid, place the pixels corresponding to Block B into the indices originally occupied by Block A.
    6.  In the output grid, place the pixels corresponding to Block A into the indices originally occupied by Block B.
    7.  Return the modified output grid.
