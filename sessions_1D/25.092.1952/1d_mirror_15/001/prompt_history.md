
## train_1

**input:**
```
0 0 0 0 0 0 1 1 1 1 1 1 0 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 1 1 1 1 1 1 0 0 0
```


## train_2

**input:**
```
0 0 0 3 3 3 3 3 3 3 0 0 9 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 3 3 3 3 3 3 3 0 0
```


## train_3

**input:**
```
0 2 2 2 2 2 2 2 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 0 0 2 2 2 2 2 2 2 0 0 0 0
```

*   **Perception:** The input is a 1D array of pixels (represented as integers). It contains a background of white pixels (0), a single maroon pixel (9) acting as a separator, and a contiguous block of pixels of another single color (blue, green, or red in the examples). The transformation involves moving the colored block from one side of the maroon separator to the other, filling the original location with white pixels. The maroon pixel remains in its original position.

*   **Facts YAML:**
    
```yaml
    task_type: array_manipulation
    components:
      - item: background
        color: 0 (white)
        role: fills empty space
      - item: separator
        color: 9 (maroon)
        count: 1
        role: pivot point, remains stationary
      - item: colored_block
        color: any color except 0 (white) and 9 (maroon)
        structure: contiguous block of identical pixels
        count: 1
        role: mobile element
    actions:
      - action: identify
        target: separator (maroon pixel)
        result: position (index) of the separator
      - action: identify
        target: colored_block
        result: color, length, and original position (relative to the separator)
      - action: move
        target: colored_block
        from: original side of the separator
        to: opposite side of the separator
        details: place the block adjacent to the separator on the new side
      - action: fill
        target: original position of the colored_block
        with: background color (white)
    constraints:
      - The input array always contains exactly one separator (maroon pixel).
      - The input array always contains exactly one contiguous colored_block (non-white, non-maroon).
      - The separator's position does not change.
    output_construction:
      - Initialize an output array of the same size as the input, filled with the background color (white).
      - Place the separator at its original position in the output array.
      - Place the colored_block in the output array on the side of the separator opposite to its original position, immediately adjacent to the separator.
    ```


*   **Natural Language Program:**
    1.  Find the index of the single maroon pixel (9) in the input array.
    2.  Identify the contiguous block of pixels that are neither white (0) nor maroon (9). Record its color and length.
    3.  Determine whether this colored block is positioned entirely to the left or entirely to the right of the maroon pixel.
    4.  Create a new array of the same size as the input, initially filled entirely with white pixels (0).
    5.  Place the maroon pixel (9) into the new array at the same index it occupied in the input array.
    6.  If the colored block was originally to the left of the maroon pixel, place the block into the new array immediately to the right of the maroon pixel, using its recorded color and length.
    7.  If the colored block was originally to the right of the maroon pixel, place the block into the new array immediately to the left of the maroon pixel, ensuring it ends just before the maroon pixel's index, using its recorded color and length.
    8.  The resulting array is the output.
