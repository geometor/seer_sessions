
## train_1

**input:**
```
0 0 0 0 0 0 0 3 3 3
0 0 5 5 5 5 5 3 4 3
0 5 0 0 0 0 0 3 3 3
0 5 4 4 4 0 0 0 0 0
5 0 4 2 4 0 0 6 6 6
0 5 4 4 4 0 5 6 1 6
0 5 5 5 5 5 0 6 6 6
0 0 1 1 1 0 0 0 0 0
0 0 1 3 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3
0 0 5 5 5 5 5 3 2 3
0 5 0 0 0 0 0 3 3 3
0 5 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 6 6 6
0 5 0 0 0 0 5 6 3 6
0 5 5 5 5 5 0 6 6 6
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 2 2 0 0 0 3 3 3 0
2 6 2 0 0 0 3 2 3 0
2 2 2 0 5 0 3 3 3 0
0 0 0 5 0 5 5 5 5 0
8 8 8 0 5 0 0 1 1 1
8 3 8 0 0 5 0 1 4 1
8 8 8 0 5 0 0 1 1 1
0 5 0 5 4 4 4 0 0 0
0 5 5 0 4 8 4 0 0 0
0 0 0 0 4 4 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 5 0 5 5 5 5 0
8 8 8 0 5 0 0 1 1 1
8 2 8 0 0 5 0 1 8 1
8 8 8 0 5 0 0 1 1 1
0 5 0 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
1 1 1 0 0 0 0 4 4 4
1 2 1 0 0 0 0 4 3 4
1 1 1 0 0 5 0 4 4 4
0 5 0 0 5 0 5 0 0 0
0 5 0 5 3 3 3 5 0 0
0 0 5 0 3 6 3 0 5 0
0 0 0 0 3 3 3 0 5 0
2 2 2 0 0 0 0 7 7 7
2 9 2 0 0 0 0 7 4 7
2 2 2 0 0 0 0 7 7 7
```


**output:**
```
1 1 1 0 0 0 0 0 0 0
1 9 1 0 0 0 0 0 0 0
1 1 1 0 0 5 0 0 0 0
0 5 0 0 5 0 5 0 0 0
0 5 0 5 0 0 0 5 0 0
0 0 5 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 7 7 7
```

Okay, let's break down this task.

**Perception:**

1.  **Grid Structure:** The input and output are consistently 10x10 grids.
2.  **Key Objects:** The most prominent features are 3x3 square patterns. These squares consist of a central pixel and 8 surrounding pixels (the "frame"). In the identified objects, the 8 frame pixels all share the same color (`FrameColor`), which is different from the central pixel's color (`CenterColor`).
3.  **Transformation Focus:** The changes between input and output grids exclusively involve these 3x3 "frame objects". Other pixels and structures (like the gray shapes in the examples) remain untouched.
4.  **Types of Changes:** Three distinct outcomes occur for these frame objects:
    *   **Removal:** The entire 3x3 object (frame and center) is replaced with white pixels (color 0).
    *   **Center Modification:** Only the central pixel's color is changed to a new color (`NewCenterColor`). The frame pixels remain unchanged.
    *   **No Change:** The 3x3 object remains identical in the output.
5.  **Rule Dependency:** The specific action (Remove, Change Center, No Change) depends entirely on the specific combination of the `FrameColor` and the `CenterColor`.

**YAML Facts:**


```yaml
task_description: Identify 3x3 'frame objects' and apply a transformation (removal, center color change, or no change) based on the specific colors of the frame and the center pixel.
grid_properties:
  - size: 10x10 for all examples.
objects:
  - type: frame_object
    definition: A 3x3 region where a center pixel is surrounded by 8 pixels of an identical color, different from the center pixel's color.
    properties:
      - FrameColor: The color of the 8 surrounding pixels.
      - CenterColor: The color of the central pixel.
transformations:
  - target: frame_object
    conditions_actions:
      - condition: The (FrameColor, CenterColor) pair matches a specific set of 'removal pairs'.
        action: Replace the entire 3x3 region with white (0).
        removal_pairs:
          - [4, 2] # Yellow frame, Red center
          - [1, 3] # Blue frame, Green center
          - [2, 6] # Red frame, Magenta center
          - [3, 2] # Green frame, Red center
          - [4, 8] # Yellow frame, Azure center
          - [3, 6] # Green frame, Magenta center
          - [2, 9] # Red frame, Maroon center
          - [4, 3] # Yellow frame, Green center
      - condition: The (FrameColor, CenterColor) pair matches a specific set of 'change pairs'.
        action: Change the CenterColor to a specific NewCenterColor. The FrameColor remains unchanged.
        change_map:
          (3, 4): 2 # Green frame, Yellow center -> Red center
          (6, 1): 3 # Magenta frame, Blue center -> Green center
          (8, 3): 2 # Azure frame, Green center -> Red center
          (1, 4): 8 # Blue frame, Yellow center -> Azure center
          (1, 2): 9 # Blue frame, Red center -> Maroon center
          (7, 4): 3 # Orange frame, Yellow center -> Green center
      - condition: The (FrameColor, CenterColor) pair does not match any removal or change pairs.
        action: No change to the 3x3 region.
        example_no_change_pairs:
          - [5, 0] # Gray frame, White center
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to find all instances of "frame objects". A frame object exists at center coordinates `(r, c)` if `r` and `c` are not on the grid border, the 8 neighbors of `(r, c)` all have the same color (`FrameColor`), and the pixel at `(r, c)` has a different color (`CenterColor`).
3.  For each identified frame object with its `FrameColor` and `CenterColor`:
    a.  Check if the pair `(FrameColor, CenterColor)` is in the predefined set of "removal pairs": `{(4, 2), (1, 3), (2, 6), (3, 2), (4, 8), (3, 6), (2, 9), (4, 3)}`. If it is, change all 9 pixels in the 3x3 region centered at `(r, c)` in the output grid to white (0).
    b.  If it's not a removal pair, check if the pair `(FrameColor, CenterColor)` is in the predefined set of "change pairs" `{(3, 4), (6, 1), (8, 3), (1, 4), (1, 2), (7, 4)}`. If it is, determine the corresponding `NewCenterColor` from the mapping (`(3, 4) -> 2`, `(6, 1) -> 3`, `(8, 3) -> 2`, `(1, 4) -> 8`, `(1, 2) -> 9`, `(7, 4) -> 3`) and change only the center pixel at `(r, c)` in the output grid to this `NewCenterColor`.
    c.  If the pair is neither a removal nor a change pair (e.g., `(5, 0)`), make no modifications to the output grid for this object (it remains as copied from the input).
4.  Return the final output grid.
