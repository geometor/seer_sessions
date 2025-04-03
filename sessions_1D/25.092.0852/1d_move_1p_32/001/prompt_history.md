
## train_1

**input:**
```
0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0
```


**output:**
```
0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
```


## train_3

**input:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task operates on single-row grids (1xN).
    *   Each input grid contains a single contiguous block of a non-white color, surrounded by white pixels (color 0).
    *   The non-white color varies between examples (magenta, azure, red).
    *   The position and length of the colored block also vary.
    *   The transformation involves shifting the colored block horizontally.
    *   Comparing input and output, the colored block appears to move one position to the right. The leftmost pixel of the original block becomes white, and the white pixel immediately to the right of the original block takes on the block's color.

*   **Facts:**
    
```yaml
    Examples:
      - Input: 1x30 grid with a magenta (6) block from index 4 to 6.
        Output: 1x30 grid with the magenta block shifted to indices 5 to 7.
      - Input: 1x30 grid with an azure (8) block from index 0 to 25.
        Output: 1x30 grid with the azure block shifted to indices 1 to 26.
      - Input: 1x30 grid with a red (2) block from index 2 to 20.
        Output: 1x30 grid with the red block shifted to indices 3 to 21.
    Grid Properties:
      - Type: 1D array (single row).
      - Size: 1x30 in all examples.
      - Background Color: White (0).
    Objects:
      - Name: Colored Block
      - Type: Contiguous segment of non-white pixels.
      - Quantity: 1 per grid.
      - Properties:
        - Color: Varies (magenta, azure, red).
        - Start Index: Position of the leftmost pixel of the block.
        - End Index: Position of the rightmost pixel of the block.
        - Length: Number of pixels in the block.
    Transformation:
      - Action: Horizontal Shift
      - Direction: Right
      - Magnitude: 1 pixel
      - Details:
        - The pixel at the original 'Start Index' of the block becomes white (0).
        - The pixel at the original 'End Index + 1' (which was white) becomes the color of the block.
        - All other pixels retain their original color.
    ```


*   **Natural Language Program:**
    1.  Identify the single contiguous block of non-white pixels in the input row. Determine its color, start index, and end index.
    2.  Create a copy of the input row to serve as the basis for the output row.
    3.  In the output row, change the color of the pixel at the original start index of the block to white (0).
    4.  In the output row, change the color of the pixel at the position immediately following the original end index of the block (i.e., end index + 1) to the identified color of the block.
    5.  Return the modified row as the output.
