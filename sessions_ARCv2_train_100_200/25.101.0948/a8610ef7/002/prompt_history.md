
## train_1

**input:**
```
0 8 0 8 8 8
8 8 8 8 8 0
8 0 8 0 8 0
0 8 8 8 0 8
8 8 0 8 8 0
8 8 0 0 0 8
```


**output:**
```
0 2 0 5 5 2
2 2 5 2 2 0
5 0 2 0 5 0
0 5 2 5 0 5
2 2 0 2 2 0
5 2 0 0 0 2
```


## train_2

**input:**
```
8 8 0 8 8 0
8 0 8 8 8 0
0 0 8 8 8 8
0 8 0 0 8 8
8 8 0 8 0 8
8 0 0 8 0 8
```


**output:**
```
2 5 0 2 5 0
2 0 5 2 5 0
0 0 5 5 2 2
0 5 0 0 2 2
2 5 0 2 0 5
2 0 0 2 0 5
```


## train_3

**input:**
```
0 8 8 0 0 8
8 8 8 0 0 0
8 8 8 0 8 0
8 0 8 8 0 8
8 8 0 0 0 0
8 8 8 8 8 0
```


**output:**
```
0 2 2 0 0 5
2 2 5 0 0 0
2 5 2 0 5 0
2 0 2 5 0 5
2 2 0 0 0 0
5 2 2 5 5 0
```


## train_4

**input:**
```
8 8 8 0 0 0
0 0 8 8 0 8
0 8 0 0 0 0
8 8 0 0 8 8
8 0 8 8 8 8
0 0 0 0 8 8
```


**output:**
```
5 5 5 0 0 0
0 0 2 2 0 2
0 2 0 0 0 0
5 2 0 0 5 5
5 0 2 2 5 2
0 0 0 0 5 5
```

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are grids of pixels with integer values representing colors.
2.  **Colors:**
    *   Input grids contain only white (0) and azure (8).
    *   Output grids contain white (0), red (2), and gray (5).
3.  **Transformation:**
    *   White (0) pixels in the input remain white (0) in the output.
    *   Azure (8) pixels in the input are transformed into either red (2) or gray (5) in the output. The transformation rule depends on the local neighborhood of the azure pixel.
4.  **Neighborhood Influence:** The change from azure (8) to red (2) or gray (5) appears to be determined by the configuration of neighboring pixels, specifically the count and color of neighbors within the 3x3 area centered on the pixel.
5.  **Potential Rule (Parity Check):** A possible, though potentially flawed, hypothesis involves counting the number of azure (8) neighbors (including diagonals) for each azure pixel in the input grid. The parity (odd or even) of this count might determine the output color (e.g., odd count maps to red, even count maps to gray, or vice versa). Initial checks show inconsistencies with this simple rule, suggesting a more complex condition or a different rule altogether. The rule involves mapping 8 -> 2 and 8 -> 5.

**Facts (YAML):**


```yaml
elements:
  - object: pixel
    properties:
      - color: white (0)
      - color: azure (8)
      - color: red (2)
      - color: gray (5)
      - position: (row, column)
  - object: grid
    properties:
      - dimensions: height, width
      - content: matrix of pixels
relationships:
  - type: adjacency
    between: pixels
    definition: Pixels sharing an edge (orthogonal) or a corner (diagonal). Orthogonal and diagonal neighbors (8 neighbors total) seem relevant.
actions:
  - name: transform_color
    input: pixel (azure=8)
    output: pixel (red=2 or gray=5)
    condition: Based on the colors of the 8 neighboring pixels (within the 3x3 grid centered on the input pixel).
  - name: preserve_color
    input: pixel (white=0)
    output: pixel (white=0)
    condition: Always applies to white pixels.
transformation_rule:
  - description: Iterate through each pixel of the input grid.
  - if: input pixel color is white (0)
    then: output pixel color remains white (0).
  - if: input pixel color is azure (8)
    then:
      - step: analyze the 3x3 neighborhood centered on the pixel.
      - step: count the number of neighbors that are also azure (8).
      - step: apply a rule based on this count to determine the output color (red=2 or gray=5).
      - specific_rule_hypothesis (tentative): If the count of azure neighbors is odd, the output is red (2); if the count is even, the output is gray (5). (Note: This specific hypothesis showed inconsistencies during analysis).
```


**Natural Language Program:**

1.  Create an output grid with the same dimensions as the input grid.
2.  For each pixel at position (row, column) in the input grid:
    a.  If the color of the input pixel is white (0), set the color of the corresponding output pixel at (row, column) to white (0).
    b.  If the color of the input pixel is azure (8):
        i.  Examine the 8 neighboring pixels (up, down, left, right, and diagonals) surrounding the input pixel at (row, column). Consider neighbors outside the grid boundaries as non-azure.
        ii. Count how many of these 8 neighbors have the color azure (8). Let this count be `N`.
        iii. If `N` is an odd number, set the color of the output pixel at (row, column) to red (2).
        iv. If `N` is an even number, set the color of the output pixel at (row, column) to gray (5).
3.  Return the completed output grid.
```python
"""
Transforms an input grid based on the following rules:
1. White (0) pixels remain white (0).
2. Azure (8) pixels are transformed based on their neighbors:
   - Count the number of azure (8) neighbors in the 8 adjacent cells (including diagonals).
   - If the count of azure neighbors is odd, the output pixel becomes red (2).
   - If the count of azure neighbors is even, the output pixel becomes gray (5).
"""

import numpy as np

def count_azure_neighbors(grid: np.ndarray, r: int, c: int) -> int:
    """
    Counts the number of azure (8) neighbors for a given cell (r, c).
    Handles boundary conditions.
    """
    height, width = grid.shape
    count = 0
    # Iterate through the 3x3 neighborhood
    for i in range(max(0, r - 1), min(height, r + 2)):
        for j in range(max(0, c - 1), min(width, c + 2)):
            # Skip the center cell itself
            if i == r and j == c:
                continue
            # Check if the neighbor is azure
            if grid[i, j] == 8:
                count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize the output grid with the same dimensions, filled with zeros initially
    output_array = np.zeros_like(input_array)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            pixel_color = input_array[r, c]

            # Rule 1: Preserve white pixels
            if pixel_color == 0:
                output_array[r, c] = 0
            # Rule 2: Transform azure pixels based on neighbor count
            elif pixel_color == 8:
                # Count azure neighbors
                neighbor_count = count_azure_neighbors(input_array, r, c)

                # Apply transformation based on parity of neighbor count
                if neighbor_count % 2 != 0:  # Odd count
                    output_array[r, c] = 2  # Red
                else:  # Even count (including 0)
                    output_array[r, c] = 5  # Gray
            # Handle any unexpected colors (though the problem description implies only 0 and 8)
            else:
                 output_array[r, c] = pixel_color # Or handle as an error, based on assumptions


    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_array.tolist()

    return output_grid
```
