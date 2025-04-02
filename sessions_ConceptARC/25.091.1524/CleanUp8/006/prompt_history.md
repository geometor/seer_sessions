
## train_1

**input:**
```
2 2 0 0 0 0 0 0 0 0
6 2 0 0 3 0 0 1 0 0
0 0 1 6 0 0 0 0 0 0
0 0 1 1 0 0 6 0 0 6
0 0 0 0 3 3 0 0 0 0
0 3 0 0 3 3 0 1 0 0
0 0 0 0 0 3 4 4 0 0
0 1 0 0 7 0 4 6 0 0
7 0 0 0 0 0 0 0 5 5
0 0 0 0 3 0 0 0 7 5
```


**output:**
```
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 5 5
```


## train_2

**input:**
```
0 0 0 4 0 0 0 4 4 3
0 6 0 0 0 0 0 0 3 3
0 0 0 0 0 0 7 7 0 0
0 0 0 4 0 0 6 7 0 0
4 0 0 0 6 6 0 0 0 0
0 1 0 0 6 8 0 0 0 0
0 0 5 5 0 0 0 0 6 0
0 0 1 5 0 0 6 0 0 0
9 9 0 0 0 0 0 0 0 1
8 9 0 0 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0
```

Okay, let's analyze the transformation logic from the input to the output grid based on the provided examples.

## Perception

1.  **Input Grid:** The input grids contain various small colored shapes (single pixels, 1x2 rectangles, 2x1 rectangles) scattered across a white background (color 0).
2.  **Output Grid:** The output grids are much sparser, containing only 2x2 squares of solid color on a white background.
3.  **Transformation:** The transformation appears to involve identifying specific structures in the input, filtering them based on certain criteria, and then replacing those selected structures with larger 2x2 squares in the output. All other elements from the input are discarded.
4.  **Identifying Structures:** The structures that seem relevant are pairs of adjacent pixels (sharing an edge, forming 1x2 or 2x1 rectangles) of the same color. Single pixels or larger shapes are ignored.
5.  **Filtering Criteria:** Not all pairs are transformed. By comparing the pairs present in the input with the squares in the output, a pattern emerges related to the coordinates. Specifically, only pairs whose top-left pixel (the one with the minimum row and minimum column index) resides at a location where *both* the row index and the column index are even numbers (0, 2, 4, ...) are selected for transformation.
6.  **Replacement:** Each selected pair is replaced by a 2x2 square of the *same* color. The top-left corner of the 2x2 square in the output corresponds exactly to the top-left corner coordinate of the original pair in the input.
7.  **Output Construction:** The final output grid is initialized as white, and then the 2x2 squares derived from the filtered input pairs are drawn onto it.

## Facts


```yaml
task_elements:
  - element: Grid
    properties:
      - type: 2D array of integers (0-9) representing colors
      - background_color: white (0)
  - element: Objects
    description: Contiguous blocks of non-background color. Relevant objects in this task are specifically pairs of adjacent pixels of the same color (forming 1x2 or 2x1 rectangles).
    properties:
      - color: The color of the pixels in the pair (1-9)
      - location: Coordinates of the two pixels comprising the pair.
      - top_left_coordinate: The coordinate (row, col) with the minimum row and minimum column index for the pair.
  - element: Transformation
    description: A filtering and replacement process.
    steps:
      - step: Identify all pairs of adjacent (sharing an edge), same-colored pixels in the input grid.
      - step: Filter these pairs based on their top-left coordinate (r, c). Keep only pairs where both 'r' and 'c' are even numbers (0, 2, 4, ...).
      - step: Create a new output grid initialized with the background color (white).
      - step: For each filtered pair, draw a 2x2 square of the pair's color onto the output grid, starting at the pair's top-left coordinate.
relationships:
  - type: Selection
    description: Only pairs of adjacent, same-colored pixels whose top-left coordinates (r, c) have both r and c as even numbers are selected from the input.
  - type: Mapping
    description: Each selected input pair maps to a 2x2 square of the same color in the output grid.
  - type: Positional_Conservation
    description: The top-left coordinate of the output 2x2 square is identical to the top-left coordinate of the corresponding input pair.
```


## Natural Language Program

1.  Initialize an empty output grid of the same dimensions as the input grid, filled with the background color (white, 0).
2.  Iterate through each pixel (r, c) of the input grid.
3.  For each non-background pixel at (r, c) with color `C`:
    a.  Check its right neighbor at (r, c+1). If it exists and also has color `C`, this forms a horizontal pair. The top-left coordinate is (r, c).
    b.  Check its bottom neighbor at (r+1, c). If it exists and also has color `C`, this forms a vertical pair. The top-left coordinate is (r, c).
4.  Create a list of all unique pairs found, storing their color `C` and their top-left coordinate (r, c). Ensure each pair is only counted once (e.g., don't count the pair starting at (r, c+1) if you already counted the one starting at (r, c)).
5.  Filter this list of pairs: Keep only those pairs whose top-left coordinate (r, c) satisfies the condition that both `r` is an even number AND `c` is an even number.
6.  For each pair (color `C`, top-left coordinate (r, c)) remaining after filtering:
    a.  Paint a 2x2 square of color `C` onto the output grid, starting at position (r, c). Specifically, set the pixels at (r, c), (r, c+1), (r+1, c), and (r+1, c+1) to color `C`. Handle boundary conditions if the grid is too small for a full 2x2 square (although example dimensions suggest this won't happen).
7.  Return the completed output grid.
```python
import numpy as np

"""
Identifies pairs of adjacent pixels (horizontal or vertical) of the same non-background color in the input grid. 
Filters these pairs, keeping only those whose top-left coordinate (r, c) has both r and c as even numbers.
For each filtered pair, draws a 2x2 square of the same color onto the output grid, starting at the pair's top-left coordinate.
The output grid is initialized with the background color (white, 0).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on finding specific adjacent pairs and replacing them with 2x2 squares.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Set to store found pairs to avoid duplicates and facilitate filtering
    # Stores tuples of (color, top_left_row, top_left_col)
    found_pairs = set()

    # Iterate through each pixel to find potential pairs
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            # Skip background color
            if color == 0:
                continue

            # Check for horizontal pair (pixel to the right)
            if c + 1 < width and input_grid[r, c + 1] == color:
                # Top-left coordinate is (r, c)
                found_pairs.add((color, r, c))

            # Check for vertical pair (pixel below)
            if r + 1 < height and input_grid[r + 1, c] == color:
                # Top-left coordinate is (r, c)
                found_pairs.add((color, r, c))

    # Filter pairs and draw 2x2 squares on the output grid
    for color, r, c in found_pairs:
        # Apply the filtering condition: row and column indices must both be even
        if r % 2 == 0 and c % 2 == 0:
            # Check if the 2x2 square fits within the grid boundaries
            if r + 1 < height and c + 1 < width:
                # Draw the 2x2 square with the pair's color
                output_grid[r:r+2, c:c+2] = color

    return output_grid

```
```python
import numpy as np

"""
The transformation identifies 2x2 regions in the input grid starting at coordinates (r, c) where both r and c are even.
If such a 2x2 region contains at least one pair of adjacent (horizontal or vertical) pixels of the same non-background color, 
then the corresponding 2x2 region in the output grid (at the same coordinates (r, c)) is filled entirely with that color. 
Otherwise, the 2x2 output region remains the background color (white, 0).
The output grid is initialized with the background color.
"""

def find_pair_color_in_2x2(subgrid: np.ndarray) -> int:
    """
    Checks a 2x2 subgrid for any adjacent pair of identical, non-background pixels.

    Args:
        subgrid: A 2x2 numpy array.

    Returns:
        The color of the first found pair, or 0 if no such pair is found.
    """
    # Check horizontal pair in top row
    if subgrid[0, 0] != 0 and subgrid[0, 0] == subgrid[0, 1]:
        return subgrid[0, 0]
    # Check horizontal pair in bottom row
    if subgrid[1, 0] != 0 and subgrid[1, 0] == subgrid[1, 1]:
        return subgrid[1, 0]
    # Check vertical pair in left column
    if subgrid[0, 0] != 0 and subgrid[0, 0] == subgrid[1, 0]:
        return subgrid[0, 0]
    # Check vertical pair in right column
    if subgrid[0, 1] != 0 and subgrid[0, 1] == subgrid[1, 1]:
        return subgrid[0, 1]
    # No non-background adjacent pair found
    return 0

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by finding adjacent pairs within 2x2 regions 
    starting at even coordinates and creating corresponding 2x2 colored squares in the output.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through potential top-left corners (r, c) of 2x2 blocks
    # where r and c are even
    for r in range(0, height - 1, 2):  # Stop before the last row if height is odd
        for c in range(0, width - 1, 2): # Stop before the last col if width is odd
            
            # Extract the 2x2 subgrid from the input
            input_subgrid = input_grid[r:r+2, c:c+2]

            # Check if this subgrid contains a qualifying adjacent pair
            pair_color = find_pair_color_in_2x2(input_subgrid)

            # If a pair was found (color is not 0)
            if pair_color != 0:
                # Fill the corresponding 2x2 region in the output grid with the pair's color
                output_grid[r:r+2, c:c+2] = pair_color

    return output_grid
```
```python
import numpy as np

"""
Identifies pairs of adjacent pixels (horizontal or vertical) of the same non-background color in the input grid. 
Filters these pairs, keeping only those whose top-left coordinate (r, c) has both r and c as even numbers.
For each uniquely identified filtered pair location (r, c) and its associated color, draws a 2x2 square of that color onto the output grid, starting at (r, c).
The output grid is initialized with the background color (white, 0).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on finding specific adjacent pairs 
    at even coordinates and replacing them with 2x2 squares.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Set to store unique tuples (color, top_left_row, top_left_col) 
    # for the 2x2 squares to be drawn.
    squares_to_draw = set()

    # Iterate through each cell (r, c) of the input grid
    for r in range(height):
        for c in range(width):
            current_color = input_grid[r, c]

            # Skip background color
            if current_color == 0:
                continue

            # Check for horizontal pair (pixel to the right)
            if c + 1 < width and input_grid[r, c + 1] == current_color:
                # The top-left coordinate of this pair is (r, c)
                # Check if both row and column indices are even
                if r % 2 == 0 and c % 2 == 0:
                    squares_to_draw.add((current_color, r, c))

            # Check for vertical pair (pixel below)
            if r + 1 < height and input_grid[r + 1, c] == current_color:
                # The top-left coordinate of this pair is (r, c)
                # Check if both row and column indices are even
                if r % 2 == 0 and c % 2 == 0:
                    squares_to_draw.add((current_color, r, c))

    # Draw the identified 2x2 squares onto the output grid
    for color, r, c in squares_to_draw:
        # Double-check boundary conditions for the 2x2 square
        # (Although the loops above implicitly handle the start r, c, 
        # we ensure the square doesn't go out of bounds)
        if r + 1 < height and c + 1 < width:
            # Color the 2x2 block in the output grid
            output_grid[r:r+2, c:c+2] = color

    return output_grid

```
