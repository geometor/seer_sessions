
## train_1

**input:**
```
4 0 0 0 0
0 4 0 0 0
0 4 4 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 4
0 0 0 4 0
0 0 4 4 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 3 3 3 0
0 3 0 3 0
3 3 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
3 3 0 0 0
0 3 0 3 0
0 3 3 3 0
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
4 4 0 0 0
4 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
0 0 0 4 4
0 0 0 0 4
```


## train_4

**input:**
```
0 0 3 0 0
0 0 3 3 3
0 0 3 0 0
0 0 3 0 0
0 0 3 0 0
```


**output:**
```
0 0 3 0 0
0 0 3 0 0
0 0 3 0 0
0 0 3 3 3
0 0 3 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are represented as 5x5 grids containing single digits.
2.  **Grid Contents:** The grids contain a background value (digit '0') and object pixels represented by non-zero digits ('3' or '4' in the examples).
3.  **Object Preservation:** The non-zero digits present in the input seem to be the same as those in the output, but their positions change. The overall shape or collection of non-zero pixels is preserved but transformed.
4.  **Transformation Type:** The transformation appears to be a reflection (mirroring) of the input grid's contents.
5.  **Reflection Axis:** The axis of reflection seems dependent on the specific non-zero digit present:
    *   When the grid contains '4's (train\_1, train\_3), the reflection is *horizontal* (across the vertical centerline).
    *   When the grid contains '3's (train\_2, train\_4), the reflection is *vertical* (across the horizontal centerline).
6.  **Consistency:** In all examples, only one type of non-zero digit is present in any given input grid.

**YAML Facts:**


```yaml
Grid:
  Properties:
    - type: 2D array
    - dimensions: 5x5 (constant)
    - content: Cells
Cells:
  Properties:
    - value: integer (0, 3, or 4 observed)
    - position: (row, column)
Objects:
  - type: Pattern/Shape
  - formed_by: non-zero Cells
  - properties:
      - digit_value: the specific non-zero digit (e.g., 3 or 4)
Transformation:
  type: Reflection
  axis_determination:
    - rule: Based on the digit_value of the Objects in the input Grid
    - condition_1:
        - if: digit_value is 4
        - then: reflection_axis is vertical_centerline
        - result: Horizontal reflection
    - condition_2:
        - if: digit_value is 3
        - then: reflection_axis is horizontal_centerline
        - result: Vertical reflection
  input: Input Grid
  output: Output Grid (reflected Input Grid)
Relationships:
  - The Output Grid is a reflection of the Input Grid.
  - The type of reflection (horizontal or vertical) is determined by the specific non-zero digit present in the Input Grid.
```


**Natural Language Program:**

1.  Examine the input grid to identify the non-zero digit present (assume only one type of non-zero digit exists, based on examples).
2.  If the non-zero digit found is '4', perform a horizontal reflection of the entire input grid across its central vertical axis to produce the output grid.
3.  If the non-zero digit found is '3', perform a vertical reflection of the entire input grid across its central horizontal axis to produce the output grid.
4.  If the input grid contains only '0's, the output grid is identical to the input grid.
