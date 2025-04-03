
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 3 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 3 0 0
```


## train_2

**input:**
```
0 0 0 0 5 5 5 5 5 5 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 5 5 5 5 5 5 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

1.  **Grid Structure:** The input and output are both 1-dimensional arrays (single rows) of pixels represented by integers (colors).
2.  **Key Elements:**
    *   A single green pixel (color 3) appears in each input. It seems to act as a fixed point or target.
    *   A contiguous block of pixels of a single color (yellow, gray, or orange in the examples) is present. This block is not green or white. This appears to be the 'moving' element.
    *   The rest of the grid is composed of white pixels (color 0), acting as the background.
3.  **Transformation:** The primary transformation observed is the horizontal movement (shift to the right) of the non-green, non-white colored block.
4.  **Movement Rule:** The colored block moves rightwards until its rightmost pixel is immediately adjacent to the left side of the green pixel. The gap of white pixels initially between the block and the green pixel is closed.
5.  **Pixel Replacement:** The pixels originally occupied by the left part of the block before the shift become white pixels (background color) in the output. The relative positions of the green pixel and the block (block is to the left of green) are maintained. The size and color of the moving block and the green pixel remain unchanged.

## Facts


```yaml
grid_dimensionality: 1
objects:
  - id: target
    type: pixel
    color: green # 3
    quantity: 1
    attributes: [fixed_position]
  - id: mover
    type: block # contiguous pixels of the same color
    color: any_except [white, green] # [yellow (4), gray (5), orange (7)] in examples
    quantity: 1
    attributes: [mobile, solid]
  - id: background
    type: pixel
    color: white # 0
    quantity: variable
relationships:
  - type: spatial
    from: mover
    to: target
    details: mover is initially to the left of target, separated by one or more background pixels.
actions:
  - id: shift_right
    actor: mover
    target_relation: adjacent_left_of(target)
    details: |
      Calculate the number of background pixels (gap_size) between the rightmost pixel
      of the mover block and the target pixel.
      Shift the entire mover block rightwards by gap_size positions.
  - id: fill_background
    actor: grid
    target_area: pixels originally occupied by the mover block before the shift
    details: |
      Change the color of the leftmost gap_size pixels originally occupied by the
      mover block to the background color (white).
```


## Natural Language Program

1.  Identify the unique green pixel (color 3) in the input row and note its position. Call this the `target_pixel`.
2.  Identify the contiguous block of pixels that are neither white (color 0) nor green (color 3). Note its color, start position, and end position. Call this the `moving_block`.
3.  Calculate the gap size: `gap = position(target_pixel) - position(rightmost_pixel_of_moving_block) - 1`. This is the number of white pixels between the `moving_block` and the `target_pixel`.
4.  Create the output row initially as a copy of the input row.
5.  Shift the `moving_block` `gap` positions to the right in the output row. This means for each pixel in the `moving_block` at input position `i`, its new position in the output row is `i + gap`.
6.  Fill the `gap` positions immediately to the left of the original `moving_block` start position with the background color (white, 0) in the output row. Specifically, change the pixels from the original `start_position` of the `moving_block` up to `start_position + gap - 1` to white (0).
