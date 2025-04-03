
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0
```


## train_2

**input:**
```
0 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0
```


**output:**
```
0 4 0 0 0 0 0 0 0 0 0 0 4 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 5 5 5 5 5 5 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 5 0 0 0 0 5 0 0
```

**Perception:**

The input and output are 1-dimensional grids (or single rows). Each input contains a contiguous horizontal block of a single non-white color, surrounded by white pixels (color 0). The transformation involves modifying this non-white block. Specifically, only the first and the last pixel of the original colored block remain in their original color in the output. All the pixels *between* the first and last pixel of the block are changed to white (color 0). The white pixels outside the original block remain unchanged.

**Facts:**


```yaml
task_type: array_transformation
dimensionality: 1D
input_features:
  - background_color: 0 (white)
  - objects:
      - type: contiguous_horizontal_block
      - count: 1 per example
      - properties:
          - color: non-zero (8-azure, 4-yellow, 5-gray in examples)
          - length: variable (4, 12, 6 in examples)
          - location: surrounded by background_color
transformation:
  - action: modify_object
  - target: the contiguous_horizontal_block
  - modification:
      - keep the first pixel of the block
      - keep the last pixel of the block
      - change all pixels between the first and last pixel to background_color (0)
  - background: remains unchanged
output_features:
  - background_color: 0 (white)
  - objects:
      - type: pair_of_pixels (representing the ends of the original block)
      - properties:
          - color: same as the input block's color
          - separation: distance between them is original_block_length - 1
          - infill: background_color (0) between the pair
```


**Natural Language Program:**

1.  Identify the contiguous horizontal block of non-white pixels in the input grid. Note its color, starting index, and ending index.
2.  Create a new grid of the same size as the input, initially filled with the background color (0).
3.  Copy the non-white pixel from the starting index of the identified block in the input to the same index in the output grid.
4.  If the starting index and ending index are different (i.e., the block has a length greater than 1), copy the non-white pixel from the ending index of the identified block in the input to the same index in the output grid.
5.  Copy all the white pixels (0) from the input grid that were *outside* the identified block to their corresponding positions in the output grid. (Alternatively, steps 2-4 implicitly handle this if the output grid is initialized correctly or if the input is copied initially and then modified).
6.  A simpler approach: Copy the entire input grid to the output grid. Then, iterate from the starting index + 1 up to (but not including) the ending index of the identified block, changing the pixel color at each of these intermediate indices to white (0).
