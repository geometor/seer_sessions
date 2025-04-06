## Perception of Task Elements

The task involves transforming an input grid of numbers (0s and 3s) into an output grid of the same dimensions. The transformation rule appears to modify the number 3 based on its connectivity to other 3s. Zeros remain unchanged. Specifically, the number 3 seems to change to 8 only if it is part of a group of connected 3s (sharing a side, horizontally or vertically). Isolated 3s (not connected to any other 3s) remain as 3s.

## Facts


```yaml
elements:
  - object: grid
    description: A 2D array of integers.
    properties:
      - type: input_grid
        values: Contains integers 0 and 3.
      - type: output_grid
        values: Contains integers 0, 3, and 8.
        relation: Derived from the input_grid based on a transformation rule.
      - dimensions: Both input and output grids have the same height and width for a given example pair.
  - object: cell
    description: An individual element within the grid.
    properties:
      - value: An integer (0, 3, or 8).
      - position: Defined by row and column index.
      - neighbours: Cells directly adjacent horizontally or vertically.
  - object: connected_component
    description: A group of cells with the value 3 that are connected.
    properties:
      - connectivity: Cells are connected if they share a horizontal or vertical edge (not diagonal).
      - size: The number of cells in the component.
actions:
  - action: identify_components
    description: Find all connected components of cells containing the value 3 in the input grid.
    input: input_grid
    output: A set of connected components, each component being a set of cell positions.
  - action: transform_components
    description: Modify the values of cells based on the size of their connected component.
    input: input_grid, identified_components
    output: output_grid
    rule:
      - if: A cell belongs to a connected component of 3s with size >= 2.
        then: Change the cell's value from 3 to 8 in the output grid.
      - if: A cell belongs to a connected component of 3s with size == 1 (isolated 3).
        then: Keep the cell's value as 3 in the output grid.
      - if: A cell's value is 0.
        then: Keep the cell's value as 0 in the output grid.
relationships:
  - type: spatial
    description: Adjacency between cells (horizontal and vertical neighbors).
  - type: membership
    description: Cells belong to connected components.
  - type: transformation
    description: The value of a cell in the output grid depends on its value and the size of its connected component (if any) in the input grid.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all connected components of cells containing the value 3 in the input grid. Two cells are considered connected if they share a horizontal or vertical edge.
3.  For each identified connected component of 3s:
    a.  Determine the size (number of cells) of the component.
    b.  If the size of the component is greater than or equal to 2:
        i.  Iterate through all cells belonging to this component.
        ii. For each cell in the component, change its value in the output grid to 8.
4.  Cells containing 0 in the input grid remain 0 in the output grid.
5.  Cells containing 3 that belong to a component of size 1 (isolated 3s) remain 3 in the output grid.
6.  Return the modified output grid.