## Perception

The input and output are both 1-dimensional arrays (rows) of pixels.
Each input array contains exactly one contiguous block of a non-white color (orange or yellow in the examples). The rest of the pixels are white (0).
The output array is the same size as the input array.
The transformation involves moving the non-white block horizontally.
Comparing the input and output in each example, the non-white block appears to be shifted exactly two positions to the right.
The pixels vacated by the block become white, and the pixels where the block moves take on the block's color.

## Facts


```yaml
task_type: array_transformation
dimensionality: 1D
input_components:
  - name: background
    type: pixel_value
    value: 0 (white)
  - name: colored_block
    type: object
    properties:
      - contiguity: contiguous
      - color: non-white (e.g., 7-orange, 4-yellow)
      - count: 1 per input array
      - location: variable start and end indices
      - size: variable length
output_components:
  - name: background
    type: pixel_value
    value: 0 (white)
  - name: shifted_block
    type: object
    properties:
      - color: same as input colored_block
      - size: same as input colored_block
      - location: shifted relative to input colored_block
transformation:
  - type: spatial_manipulation
    action: shift
    details:
      - object_to_shift: colored_block
      - direction: right
      - magnitude: 2 positions
      - effect_on_vacated_space: fill with background color (white)
      - effect_on_occupied_space: replace with block color
relationship:
  - input colored_block position determines output shifted_block position based on a fixed rightward shift of 2.
```


## Natural Language Program

1.  Identify the single contiguous block of non-white pixels in the input array. Note its color, starting position, and ending position.
2.  Create a new output array of the same size as the input array, initially filled entirely with the background color (white, 0).
3.  Calculate the new starting position of the block by adding 2 to its original starting position.
4.  Calculate the new ending position of the block by adding 2 to its original ending position.
5.  Place the original non-white block (using its original color) into the output array at the calculated new start and end positions.