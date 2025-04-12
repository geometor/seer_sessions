
## train_1

**input:**
```
7 7 7 7 7 6 7 4 7 7 7
7 7 7 7 7 6 7 4 4 4 7
7 7 7 7 7 6 7 7 7 4 7
7 2 2 2 7 6 7 7 7 4 7
7 7 2 7 7 6 7 7 7 4 7
6 6 6 6 6 6 6 6 6 6 6
7 7 7 1 7 6 7 7 3 7 7
7 1 1 1 7 6 7 3 3 7 7
7 1 1 1 7 6 7 3 7 7 7
7 1 1 1 7 6 7 3 7 7 7
7 7 7 7 7 6 7 3 7 7 7
```


**output:**
```
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
7 2 2 2 7
7 7 2 7 7
6 6 6 6 6
7 7 3 7 7
7 3 3 7 7
7 3 7 7 7
7 3 7 7 7
7 3 7 7 7
6 6 6 6 6
7 4 7 7 7
7 4 4 4 7
7 7 7 4 7
7 7 7 4 7
7 7 7 4 7
6 6 6 6 6
7 7 7 1 7
7 1 1 1 7
7 1 1 1 7
7 1 1 1 7
7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7
7 7 8 8 7
7 7 8 8 7
8 8 8 7 7
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
2 2 2 7 7
7 7 2 2 7
7 7 7 2 2
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
7 9 7 9 9
7 9 9 9 7
7 9 7 7 7
7 7 7 7 7
```


**output:**
```
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
7 9 7 9 9 6 2 2 2 7 7 6 7 7 8 8 7
7 9 9 9 7 6 7 7 2 2 7 6 7 7 8 8 7
7 9 7 7 7 6 7 7 7 2 2 6 8 8 8 7 7
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 6 7 7 1 7 7 6 7 7 9 7 7
7 8 8 8 7 6 7 7 1 7 7 6 7 9 9 9 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
```


**output:**
```
7 7 7 7 7
7 8 8 8 7
7 7 8 7 7
7 7 8 7 7
7 7 8 7 7
6 6 6 6 6
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
6 6 6 6 6
7 7 9 7 7
7 9 9 9 7
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
```

*   **Perception**: The task involves rearranging subgrids extracted from an input grid. The input grids contain subgrids separated by lines or columns composed entirely of the digit '6'. The arrangement of these separators (horizontal, vertical, or both) determines how the subgrids are extracted and how they are reassembled in the output. The reassembly involves changing the orientation (e.g., vertically stacked input blocks become horizontally arranged output blocks) and potentially the order of the blocks.

*   **Facts**:
    ```yaml
    task_type: grid_rearrangement
    components:
      - object: grid
        attributes:
          - type: input_grid
          - type: output_grid
          - content: matrix of digits
      - object: separator
        attributes:
          - value: 6
          - role: delimiter
          - type: horizontal_line (row of 6s)
          - type: vertical_column (column of 6s)
      - object: subgrid
        attributes:
          - content: portion of the input grid delimited by separators
          - role: element_to_be_rearranged
    relationships:
      - separators divide the input_grid into subgrids
      - subgrids from input_grid are assembled into output_grid
    actions:
      - identify_separators: Find horizontal lines and vertical columns of '6's in the input_grid.
      - split_grid: Divide the input_grid into subgrids based on the identified separators.
      - determine_arrangement: Classify the input arrangement based on separator orientation (vertical blocks, horizontal blocks, or quadrants).
      - reassemble_grid: Construct the output_grid by arranging the extracted subgrids according to specific rules based on the input arrangement.
        rules:
          - if input has horizontal separators only (vertical blocks):
              - arrange blocks horizontally in output
              - use vertical '6' columns as separators
              - reverse the order of blocks (bottom block first)
          - if input has vertical separators only (horizontal blocks):
              - arrange blocks vertically in output
              - use horizontal '6' lines as separators
              - preserve the order of blocks (left block first)
          - if input has central horizontal and vertical separators (quadrants):
              - arrange quadrants vertically in output
              - use horizontal '6' lines as separators
              - specific order: Top-Left, Bottom-Right, Top-Right, Bottom-Left
    ```

*   **Natural Language Program**:
    1.  Scan the input grid to locate all complete horizontal rows and complete vertical columns consisting solely of the digit '6'. These are the separators.
    2.  Analyze the configuration of separators:
        a.  **Vertical Blocks**: If only horizontal separator rows exist, they divide the grid into vertically stacked subgrids.
        b.  **Horizontal Blocks**: If only vertical separator columns exist, they divide the grid into horizontally arranged subgrids.
        c.  **Quadrants**: If a central horizontal row and a central vertical column of separators exist, they divide the grid into four quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right).
    3.  Extract the subgrids, excluding the separator lines/columns themselves.
    4.  Construct the output grid based on the identified configuration:
        a.  For **Vertical Blocks**: Arrange the extracted subgrids horizontally, placing the bottom-most input subgrid first (on the left), followed by the next subgrid up, and so on, ending with the top-most input subgrid (on the right). Separate adjacent subgrids in the output with a single vertical column of '6's.
        b.  For **Horizontal Blocks**: Arrange the extracted subgrids vertically, placing the left-most input subgrid first (at the top), followed by the next subgrid to its right, and so on, ending with the right-most input subgrid (at the bottom). Separate adjacent subgrids in the output with a single horizontal row of '6's.
        c.  For **Quadrants**: Arrange the extracted quadrants vertically in the specific order: Top-Left, Bottom-Right, Top-Right, Bottom-Left. Separate adjacent quadrants in the output with a single horizontal row of '6's.
