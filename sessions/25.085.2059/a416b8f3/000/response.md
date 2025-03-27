## Perception

The task demonstrates a simple transformation where the input grid is duplicated and placed side-by-side with itself to form the output grid.

*   **Input:** A grid of pixels with varying dimensions and colors.
*   **Output:** A grid that is twice the width of the input grid but has the same height. The content of the output grid consists of two identical copies of the input grid placed horizontally next to each other.

## Facts


```yaml
Task: Grid Duplication and Horizontal Concatenation

Examples:
  - Example 1:
    Input_Grid:
      Dimensions: 4x3 (height x width)
      Content: [[3, 0, 0], [2, 3, 0], [2, 1, 8], [0, 1, 0]]
    Output_Grid:
      Dimensions: 4x6 (height x width)
      Content: [[3, 0, 0, 3, 0, 0], [2, 3, 0, 2, 3, 0], [2, 1, 8, 2, 1, 8], [0, 1, 0, 0, 1, 0]]
      Relationship_to_Input: The output grid is formed by concatenating the input grid with itself horizontally. The left half (columns 0-2) is identical to the input grid, and the right half (columns 3-5) is also identical to the input grid.

  - Example 2:
    Input_Grid:
      Dimensions: 3x3 (height x width)
      Content: [[0, 5, 0], [5, 5, 2], [0, 0, 0]]
    Output_Grid:
      Dimensions: 3x6 (height x width)
      Content: [[0, 5, 0, 0, 5, 0], [5, 5, 2, 5, 5, 2], [0, 0, 0, 0, 0, 0]]
      Relationship_to_Input: The output grid is formed by concatenating the input grid with itself horizontally.

  - Example 3:
    Input_Grid:
      Dimensions: 4x4 (height x width)
      Content: [[5, 2, 3, 0], [2, 5, 3, 0], [5, 2, 8, 8], [0, 0, 6, 0]]
    Output_Grid:
      Dimensions: 4x8 (height x width)
      Content: [[5, 2, 3, 0, 5, 2, 3, 0], [2, 5, 3, 0, 2, 5, 3, 0], [5, 2, 8, 8, 5, 2, 8, 8], [0, 0, 6, 0, 0, 0, 6, 0]]
      Relationship_to_Input: The output grid is formed by concatenating the input grid with itself horizontally.

General_Observations:
  - The height of the output grid is always the same as the height of the input grid.
  - The width of the output grid is always exactly twice the width of the input grid.
  - The content of the output grid is consistently the input grid repeated twice, placed side-by-side.
```


## Natural Language Program

1.  Take the input grid.
2.  Create a new grid with the same height as the input grid and double its width.
3.  Copy the entire input grid into the left half of the new grid (from the first column up to the original width).
4.  Copy the entire input grid again into the right half of the new grid (from the column immediately after the original width to the last column).
5.  The resulting grid is the output.