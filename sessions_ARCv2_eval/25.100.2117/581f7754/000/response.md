**Initial Perception**

The input and output are grids of the same dimensions (18 rows, 8 columns) containing integer values 1, 4, and 8. The value '1' appears to function as a background color or empty space. The values '4' and '8' form distinct shapes or objects within the grid.

The core transformation seems to involve identifying these objects (composed of 4s and 8s) and shifting them horizontally. There appear to be multiple distinct objects in the input. Most objects are shifted, but one object (a single '4') remains in its original position. The direction and magnitude of the shift seem to vary between the objects that do move. Specifically, two objects shift right by 3 columns, and one object shifts left by 1 column. The background '1's remain unchanged in their positions relative to the grid boundaries.

**Observed Facts**


```yaml
Grid:
  Dimensions: 18x8
  BackgroundValue: 1
  ObjectValues: [4, 8]

Objects:
  - id: 1
    description: Cluster of 8s with a central 4 (looks like 3x3 minus corner)
    input_location:
      rows: [3, 4]
      cols: [1, 2, 3]
    output_location:
      rows: [3, 4]
      cols: [4, 5, 6]
    transformation:
      type: horizontal_shift
      columns_shifted: +3
    properties:
      leftmost_column: 1
      is_single_4: false

  - id: 2
    description: Cluster of 8s with a central 4 (looks like 3x3 minus corner)
    input_location:
      rows: [8, 9, 10]
      cols: [4, 5, 6]
    output_location:
      rows: [8, 9, 10]
      cols: [3, 4, 5]
    transformation:
      type: horizontal_shift
      columns_shifted: -1
    properties:
      leftmost_column: 4
      is_single_4: false

  - id: 3
    description: Hollow square/plus shape of 8s with a central 4
    input_location:
      rows: [13, 14, 15, 16]
      cols: [1, 2, 3]
    output_location:
      rows: [13, 14, 15, 16]
      cols: [4, 5, 6]
    transformation:
      type: horizontal_shift
      columns_shifted: +3
    properties:
      leftmost_column: 1
      is_single_4: false

  - id: 4
    description: Single cell with value 4
    input_location:
      rows: [17]
      cols: [5]
    output_location:
      rows: [17]
      cols: [5]
    transformation:
      type: no_change
      columns_shifted: 0
    properties:
      leftmost_column: 5
      is_single_4: true

TransformationRule:
  - Identify connected components (objects) composed of values other than 1.
  - For each object:
    - If the object consists of a single cell with value 4, it remains unchanged.
    - Otherwise, determine the object's leftmost column index (0-based).
    - If the leftmost column index is 1, shift the entire object 3 columns to the right.
    - If the leftmost column index is 4, shift the entire object 1 column to the left.
  - The background (value 1) remains unchanged.
  - Construct the output grid by placing the transformed (or unchanged) objects onto a background of 1s.

```


**Natural Language Program**

1.  Create an output grid of the same dimensions as the input grid, filled entirely with the background value '1'.
2.  Identify all distinct connected components (objects) in the input grid that consist of cells with values '4' or '8'. Treat cells connected horizontally or vertically as part of the same component.
3.  For each identified object:
    a.  Check if the object consists of only a single cell containing the value '4'.
    b.  If it is a single '4', copy its value and position directly to the corresponding cell in the output grid.
    c.  If it is *not* a single '4':
        i.  Determine the column index of the leftmost cell belonging to this object.
        ii. Calculate the horizontal shift amount:
            - If the leftmost column index is 1, the shift is +3 columns.
            - If the leftmost column index is 4, the shift is -1 column.
            - (Assume 0 shift for any other starting column based on this example, though none exist here).
        iii. For every cell belonging to this object in the input grid, copy its value to the output grid at the original row index and the original column index plus the calculated shift amount.
4.  Return the completed output grid.