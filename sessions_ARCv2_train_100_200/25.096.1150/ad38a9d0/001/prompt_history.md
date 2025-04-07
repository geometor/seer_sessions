
## train_1

**input:**
```
6 6 7 7 6 6 7 7 7
7 6 7 7 7 6 6 7 7
7 7 7 6 7 7 7 7 6
7 7 6 6 6 7 6 7 6
7 6 7 6 7 7 6 7 6
7 6 7 7 7 7 7 7 7
7 6 7 7 7 7 7 6 6
7 7 7 7 6 6 6 7 6
7 7 7 7 6 6 6 7 7
```


**output:**
```
4 4 7 7 8 8 7 7 7
7 4 7 7 7 8 8 7 7
7 7 7 3 7 7 7 7 2
7 7 3 3 3 7 9 7 2
7 2 7 3 7 7 9 7 2
7 2 7 7 7 7 7 7 7
7 2 7 7 7 7 7 4 4
7 7 7 7 5 5 5 7 4
7 7 7 7 5 5 5 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7 7
7 6 7 7 6 7 7 7 7
6 6 6 7 6 7 6 6 7
7 6 7 7 7 7 7 6 7
7 7 7 7 7 7 7 7 7
7 7 7 7 6 6 7 7 7
7 7 7 7 7 6 6 7 6
7 6 6 6 7 7 7 7 6
7 6 6 6 7 7 7 7 6
```


**output:**
```
7 7 7 7 7 7 7 7 7
7 3 7 7 9 7 7 7 7
3 3 3 7 9 7 4 4 7
7 3 7 7 7 7 7 4 7
7 7 7 7 7 7 7 7 7
7 7 7 7 8 8 7 7 7
7 7 7 7 7 8 8 7 2
7 5 5 5 7 7 7 7 2
7 5 5 5 7 7 7 7 2
```

Okay, let's analyze the transformation.

## Perception of Task Elements

1.  **Input/Output Format:** Both input and output are grids of numbers (specifically, single digits). The grid dimensions appear consistent (9x9 in the examples).
2.  **Key Values:** The input grids primarily contain the numbers '6' and '7'. The output grids contain '7' along with other numbers (2, 3, 4, 5, 8, 9).
3.  **Background Value:** The number '7' seems to act as a static background. Its position and value largely remain unchanged from input to output.
4.  **Target Value:** The number '6' in the input is the target for transformation. All '6's are replaced by other numbers in the output.
5.  **Transformation Pattern:** The transformation appears to operate on connected groups (components) of '6's. Cells containing '6' that are adjacent (up, down, left, right) form a single component.
6.  **Component Replacement:** Each connected component of '6's in the input is replaced entirely by a *single*, uniform number in the output.
7.  **Replacement Rule:** The specific number used for replacement depends on the properties of the component. Observing the examples, the size (number of cells) of the component is a primary factor. Furthermore, for components of size 3, the shape (specifically, whether it forms a straight line or an L-shape) determines the replacement value.

## YAML Fact Documentation


```yaml
task_description: Segment the input grid based on a specific value and replace segments with new values based on segment properties.

grid_properties:
  - type: 2D array of integers
  - dimensions: 9x9 (based on examples)
  - background_value: 7
  - target_value: 6

objects:
  - object: cell
    properties:
      - value: integer (0-9)
      - position: (row, column)
  - object: component
    properties:
      - constituent_value: 6 (in input)
      - cells: list of cell positions
      - size: integer (count of cells)
      - shape_descriptor:
          type: derived (e.g., bounding_box_area)
          relevance: distinguishes components of the same size (e.g., size 3)

relationships:
  - type: adjacency
    between: cells
    definition: sharing an edge (up, down, left, or right), also known as 4-way connectivity.
  - type: membership
    between: cell, component
    definition: a cell belongs to a specific connected component.

actions:
  - action: identify_components
    input: input_grid, target_value (6)
    output: list of components (each containing member cell positions)
    method: Use 4-way adjacency to find connected regions of the target_value.
  - action: determine_replacement_value
    input: component
    output: integer (replacement value for the output grid)
    logic:
      - Calculate component size.
      - If size is 3, calculate bounding box area (height * width).
      - Apply mapping rule:
          - Size 2 -> 9
          - Size 3, BBox Area 3 (Line) -> 2
          - Size 3, BBox Area 4 (L-shape) -> 4
          - Size 4 -> 8
          - Size 5 -> 3
          - Size 6 -> 5
  - action: construct_output_grid
    input: input_grid, list of components, replacement values map
    output: output_grid
    method:
      - Initialize output grid as a copy of the input grid.
      - For each identified component:
          - Get its calculated replacement value.
          - For each cell position within that component:
              - Update the cell's value in the output grid to the replacement value.
      - Keep background value (7) cells unchanged (unless they were part of a component, which shouldn't happen based on the target value '6').

constants:
  - background_value: 7
  - target_value: 6
  - replacement_map:
      - condition: size=2 -> value: 9
      - condition: size=3, bbox_area=3 -> value: 2
      - condition: size=3, bbox_area=4 -> value: 4
      - condition: size=4 -> value: 8
      - condition: size=5 -> value: 3
      - condition: size=6 -> value: 5

```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all connected components of cells containing the value '6' in the input grid, using 4-way adjacency (up, down, left, right neighbours). Keep track of the cell coordinates belonging to each component.
3.  For each identified component:
    a.  Calculate its size (the total number of cells in the component).
    b.  Determine the replacement value based on the component's size:
        i.  If the size is 3, calculate the area of its minimum bounding box (height * width).
            - If the bounding box area is 3 (indicating a 1x3 or 3x1 line shape), the replacement value is 2.
            - If the bounding box area is 4 (indicating a 2x2 L-shape), the replacement value is 4.
        ii. If the size is 2, the replacement value is 9.
        iii.If the size is 4, the replacement value is 8.
        iv. If the size is 5, the replacement value is 3.
        v.  If the size is 6, the replacement value is 5.
    c.  For every cell coordinate belonging to this component, update the corresponding cell in the output grid with the determined replacement value.
4.  Ensure that all cells originally containing '7' in the input grid retain the value '7' in the output grid (this should happen automatically if '7' is never part of a '6' component).
5.  Return the modified output grid.
