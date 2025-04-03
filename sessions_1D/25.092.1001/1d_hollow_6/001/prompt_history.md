
## train_1

**input:**
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
```


**output:**
```
5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0
```


## train_2

**input:**
```
0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0
```


**output:**
```
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0
```


## train_3

**input:**
```
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
```

**Perception:**

The examples present 1D arrays (or potentially single-row 2D grids represented linearly). Each input array contains a single contiguous block of a non-white color (e.g., gray '5', magenta '6', green '3') surrounded by white pixels ('0'). The transformation modifies this non-white block. In the output, only the first and the last pixel of the original non-white block retain their color. All the pixels that were originally between the first and last pixel of the block are changed to white ('0'). The white pixels outside the original block remain unchanged. The length of the output array is identical to the length of the input array.

**Facts:**


```yaml
task_type: array_transformation_1d
components:
  - type: input_array
    description: A 1D array containing pixels.
  - type: output_array
    description: A 1D array derived from the input array, having the same length.
  - type: block
    description: A contiguous sequence of identical non-white pixels within the input array. Assumed to be unique per input based on examples.
    properties:
      - color: The color (non-zero value) of the pixels in the block.
      - start_index: The index of the first pixel of the block.
      - end_index: The index of the last pixel of the block.
      - length: The number of pixels in the block (end_index - start_index + 1).
  - type: background
    description: Pixels with the white color (value 0) in the input array, typically surrounding the block.
transformation:
  - action: identify_block
    description: Find the single contiguous block of non-white pixels in the input array. Determine its color, start index, and end index.
  - action: modify_block
    description: Create the output array based on the input array.
    steps:
      - Keep all white background pixels from the input unchanged in the output.
      - Keep the pixel at the start_index of the block unchanged in the output.
      - Keep the pixel at the end_index of the block unchanged in the output.
      - Change all pixels within the block (from start_index + 1 to end_index - 1) to white (0) in the output.
relationship: The output array is constructed by preserving the start and end points of the identified non-white block from the input, changing the interior of the block to white, and preserving the surrounding white background pixels.
```


**Natural Language Program:**

1.  Initialize the output array as a copy of the input array.
2.  Scan the input array to find the first index (`start_index`) and the last index (`end_index`) of the contiguous block of non-white pixels. Note the color of this block.
3.  If a non-white block is found and its length is greater than 1:
    a.  Iterate from the index immediately after the `start_index` up to (but not including) the `end_index`.
    b.  For each index in this range, set the corresponding pixel in the output array to white (0).
4.  Return the modified output array. (If no non-white block is found, or if the block has length 1, the output array will be identical to the input).
