**Perception:**

The input and output are both 4x4 grids containing single-digit integers. The input grids feature a 2x2 block of non-zero numbers centered within a border of zeros. The output grids show these same non-zero numbers relocated to the four corner positions, while the rest of the grid is filled with zeros. The transformation appears to extract the central 2x2 subgrid from the input and place its elements into the corners of the output grid, maintaining their relative positions (top-left of the subgrid goes to top-left corner, top-right to top-right corner, etc.).

**Facts:**


```yaml
task_elements:
  - element: grid
    properties:
      - type: 2D array of integers
      - dimensions: 4x4
      - role: input, output
  - element: subgrid
    properties:
      - location: central 2x2 area of the input grid (rows 1-2, columns 1-2, 0-indexed)
      - content: non-zero integers
  - element: corners
    properties:
      - location: cells (0,0), (0,3), (3,0), (3,3) of the output grid
      - content: integers originally from the input subgrid
  - element: background
    properties:
      - value: 0
      - location: all cells not part of the central subgrid in the input, and all cells not corners in the output
relationship:
  - type: mapping
    source: input grid central 2x2 subgrid
    target: output grid corners
    details:
      - input[1,1] maps to output[0,0]
      - input[1,2] maps to output[0,3]
      - input[2,1] maps to output[3,0]
      - input[2,2] maps to output[3,3]
action:
  - type: extraction
    object: central 2x2 subgrid from input
  - type: placement
    object: extracted elements
    destination: corners of the output grid
  - type: initialization
    object: output grid
    value: all zeros before placement
```


**Natural Language Program:**

1.  Initialize a 4x4 output grid with all values set to 0.
2.  Identify the central 2x2 subgrid within the input grid, specifically the elements at indices (1,1), (1,2), (2,1), and (2,2).
3.  Copy the value from the input grid at index (1,1) to the output grid at index (0,0).
4.  Copy the value from the input grid at index (1,2) to the output grid at index (0,3).
5.  Copy the value from the input grid at index (2,1) to the output grid at index (3,0).
6.  Copy the value from the input grid at index (2,2) to the output grid at index (3,3).
7.  The resulting grid is the final output.