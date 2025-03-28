
Previous Code:
```python
import numpy as np
from collections import Counter, deque

"""
Transformation Rule:

1.  Identify the `Input Frame Color` from the second row (index 1) of the input grid.
2.  Define the `Inner Area` as rows 2 through 8 (indices 2 to 8) and columns 1 through 8 (indices 1 to 8).
3.  Count the frequency of each color within the input grid's `Inner Area`, excluding white (color 0) and the `Input Frame Color`.
4.  Determine the `Output Fill Color` as the color with the highest frequency count from step 3.
5.  Create an output grid of the same dimensions as the input grid.
6.  Copy the first row (index 0) from the input grid to the output grid.
7.  Fill the entire second row (index 1) of the output grid with the `Output Fill Color`.
8.  Fill the outer frame columns (index 0 and index 9) from row 2 downwards (indices 2 to 9) with the `Output Fill Color`.
9.  Fill the bottom frame row (index 9), between columns 1 and 8 (indices 1 to 8), with the `Output Fill Color`.
10. Fill the top inner frame row (index 2), between columns 1 and 8 (indices 1 to 8), with the `Output Fill Color`.
11. Initialize the rest of the `Inner Area` in the output grid (rows 3-8, columns 1-8) to white (color 0).
12. Identify all `Seed Points`: the coordinates (row, column) within the input grid's `Inner Area` where the color matches the `Output Fill Color`.
13. For each `Seed Point` (r, c), set the corresponding cell `output_grid[r, c]` to the `Output Fill Color`.
14. Perform a flood fill operation starting from all `Seed Points` simultaneously on the output grid:
    *   Use a queue and a set of visited coordinates, initialized with the `Seed Points`.
    *   While the queue is not empty, dequeue a coordinate (r, c).
    *   For each 4-way adjacent neighbor (nr, nc) of (r, c):
        *   Check if (nr, nc) is within the bounds of the `Inner Area` (rows 2-8, columns 1-8).
        *   Check if the neighbor has not been visited yet.
        *   Check if `output_grid[nr, nc]` is currently white (0).
        *   Check if the corresponding cell in the *input* grid, `input_grid[nr, nc]`, is also white (0).
        *   If all these conditions are true:
            *   Set `output_grid[nr, nc]` to the `Output Fill Color`.
            *   Mark (nr, nc) as visited.
            *   Enqueue (nr, nc).
15. Return the completed output grid.
"""

def _find_most_frequent_inner_color(input_grid, frame_color):
    """
    Counts colors in the inner area (rows 2-8, cols 1-8), excluding white 
    and the frame_color, and returns the most frequent one.
    """
    rows, cols = input_grid.shape
    # Inner area: rows 2 to rows-2, cols 1 to cols-2 (inclusive indices)
    # For 10x10 grid: rows 2-8, cols 1-8
    inner_area = input_grid[2:rows-1, 1:cols-1] 
    
    color_counts = Counter()
    for r in range(inner_area.shape[0]):
        for c in range(inner_area.shape[1]):
            color = inner_area[r, c]
            if color != 0 and color != frame_color:
                color_counts[color] += 1
                
    if not color_counts:
        # Fallback if no valid colors found - this shouldn't happen based on examples
        # Returning 0 might be safer than None if required by caller.
        # Let's assume a color will always be found as per analysis.
        # If this assumption breaks, we need error handling or a defined fallback.
        return 0 

    # Find the color with the maximum count.
    most_frequent_color = max(color_counts, key=color_counts.get)
    return most_frequent_color

def _flood_fill(output_grid, input_grid, start_coords, fill_color):
    """
    Performs a 4-way flood fill on the output_grid's inner area (rows 2-8, cols 1-8).
    Starts from start_coords, fills only cells that are white (0) in output_grid 
    AND were also white (0) in input_grid.
    Modifies the output_grid in place.
    """
    rows, cols = output_grid.shape
    q = deque(start_coords)
    visited = set(start_coords) # Keep track of initial seeds and filled cells

    # Initial seed points are already colored in the main function.
    # The queue starts with these seed points.

    while q:
        r, c = q.popleft()

        # Explore neighbours (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check boundaries (inner area: rows 2-8, cols 1-8)
            # Indices: rows 2 to rows-2, cols 1 to cols-2
            if 2 <= nr <= rows - 2 and 1 <= nc <= cols - 2:
                # Check if the neighbor hasn't been visited
                if (nr, nc) not in visited:
                    # Check if the neighbor is white (0) in the output grid
                    # AND the corresponding cell was white (0) in the input grid
                    if output_grid[nr, nc] == 0 and input_grid[nr, nc] == 0:
                        output_grid[nr, nc] = fill_color
                        visited.add((nr, nc))
                        q.append((nr, nc))


def transform(input_grid_list):
    """
    Applies the transformation rule derived from the examples.
    """
    input_np = np.array(input_grid_list, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_np)

    # 1. Identify Input Frame Color (from row index 1)
    input_frame_color = input_np[1, 0] 

    # 2. Define Inner Area (implicit in helper function and flood fill)

    # 3. & 4. Analyze inner area and determine Output Fill Color
    output_fill_color = _find_most_frequent_inner_color(input_np, input_frame_color)

    # 5. Create output grid (already done with zeros)

    # 6. Copy the first row
    output_grid[0, :] = input_np[0, :]

    # 7. Fill the second row (index 1) with Output Fill Color
    output_grid[1, :] = output_fill_color
    
    # 8. Fill the outer frame columns (0 and cols-1) from row 2 down
    output_grid[2:rows, 0] = output_fill_color  
    output_grid[2:rows, cols-1] = output_fill_color 

    # 9. Fill the bottom frame row (rows-1) inner part
    output_grid[rows-1, 1:cols-1] = output_fill_color 

    # 10. Fill the top inner frame row (row 2) inner part
    output_grid[2, 1:cols-1] = output_fill_color 

    # 11. Initialize the rest of the Inner Area (rows 3-8, cols 1-8) to white (0)
    # Indices: rows 3 to rows-2, cols 1 to cols-2
    if rows > 3 and cols > 2: # Check if this area exists
         output_grid[3:rows-1, 1:cols-1] = 0
    # Note: Pixels initialized to 0 by np.zeros_like, but this explicitly sets the core inner area

    # 12. Identify Seed Points in the input's inner area
    seed_coords = []
    for r in range(2, rows - 1): # Rows 2 to rows-2 (e.g., 2-8 for 10x10)
        for c in range(1, cols - 1): # Cols 1 to cols-2 (e.g., 1-8 for 10x10)
            if input_np[r, c] == output_fill_color:
                # Ensure seed point is within the flood fill boundary (redundant check, but safe)
                 if 2 <= r <= rows - 2 and 1 <= c <= cols - 2:
                    seed_coords.append((r, c))

    # 13. Set Seed Points in the output grid
    for r, c in seed_coords:
        # Check bounds just in case, though seed_coords generation should guarantee this
        if 2 <= r <= rows - 2 and 1 <= c <= cols - 2:
            output_grid[r, c] = output_fill_color

    # 14. Perform flood fill on the output grid's inner area
    # Pass both output_grid (to modify) and input_np (to check original white cells)
    _flood_fill(output_grid, input_np, seed_coords, output_fill_color)

    # 15. Return the completed output grid as a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 2 2 3 3 4 4 5 5
4 4 4 4 4 4 4 4 4 4
4 0 0 0 0 0 0 0 0 4
4 0 0 0 0 0 0 5 0 4
4 0 0 0 5 5 0 0 0 4
4 0 0 0 5 1 1 0 0 4
4 0 5 0 5 0 0 0 0 4
4 0 1 0 0 0 0 0 0 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
1 1 2 2 3 3 4 4 5 5
5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 0 0 0 5
5 0 5 5 5 5 5 5 0 5
5 0 5 0 0 0 0 5 0 5
5 0 5 0 0 0 0 5 0 5
5 0 5 5 5 5 5 5 0 5
5 0 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```
Transformed Output:
```
1 1 2 2 3 3 4 4 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 0 0 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 0 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
```
Match: False
Pixels Off: 37
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 74.0

## Example 2:
Input:
```
1 1 2 2 3 3 4 4 5 5
2 2 2 2 2 2 2 2 2 2
2 0 0 3 3 3 0 0 4 2
2 0 3 3 0 3 3 4 3 2
2 0 3 0 3 0 4 3 3 2
2 0 3 4 0 0 0 3 4 2
2 0 3 0 3 3 3 4 0 2
2 0 3 3 3 4 3 3 3 2
2 0 0 0 0 0 0 0 4 2
2 2 2 2 2 2 2 2 2 2
```
Expected Output:
```
1 1 2 2 3 3 4 4 5 5
3 3 3 3 3 3 3 3 3 3
3 0 3 3 3 3 3 3 3 3
3 0 3 0 0 0 0 0 3 3
3 0 3 0 0 0 0 0 3 3
3 0 3 0 0 0 0 0 3 3
3 0 3 0 0 0 0 0 3 3
3 0 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
1 1 2 2 3 3 4 4 5 5
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 0 3 3
3 3 3 3 3 3 0 3 3 3
3 3 3 0 3 3 3 3 0 3
3 3 3 3 3 3 3 0 3 3
3 3 3 3 3 0 3 3 3 3
3 3 3 3 3 3 3 3 0 3
3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 31
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 62.0

## Example 3:
Input:
```
1 1 2 2 3 3 4 4 5 5
1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 2 1
1 0 0 2 0 0 0 0 0 1
1 0 0 0 0 0 0 4 0 1
1 4 0 0 0 4 0 0 0 1
1 0 0 0 0 0 0 0 0 1
1 0 0 4 0 0 4 0 0 1
1 0 0 0 0 0 0 0 2 1
1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 2 2 3 3 4 4 5 5
4 4 4 4 4 4 4 4 4 4
4 0 0 0 0 0 0 0 0 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 0 4
4 4 0 0 0 0 0 4 0 4
4 4 0 0 0 0 0 4 0 4
4 4 4 4 4 4 4 4 0 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
1 1 2 2 3 3 4 4 5 5
4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4
4 4 4 0 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 0 4
4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 36
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 72.0
The metrics confirm the Input Frame Color and Output Fill Color derived previously. The core logic for selecting the color and defining the areas seems robust. The main issue lies in constructing the output grid's content area.

Now, construct the YAML facts and the refined natural language program.**General Assessment**

The previous code correctly identified the core mechanism: determining an `Input Frame Color` from row 1, finding the most frequent non-background color (`Output Fill Color`) within an inner area (excluding the `Input Frame Color`), and using this `Output Fill Color` to create a new frame in the output. However, the code failed to correctly replicate the content *within* the new frame. The transformed outputs showed that the inner area was almost entirely filled with the `Output Fill Color`, whereas the expected outputs indicated a more complex transformation involving preserving specific pixels from the input and performing a constrained fill.

The primary error was identified in step 10 of the previous natural language program, which incorrectly filled the inner part of row 2 with the `Output Fill Color`. Additionally, the initialization and flood fill logic needed refinement to ensure they only operated on the intended "content" area (rows 2-8, cols 1-8) and respected the original white space boundaries from the input.

**Strategy for Resolution**

1.  **Correct Frame Construction:** Maintain the logic for identifying the `Input Frame Color` and `Output Fill Color`. Ensure the output frame is constructed correctly: Row 1, Columns 0 and 9 (from Row 1 down), and Row 9 are filled with the `Output Fill Color`. Row 0 is copied directly from the input.
2.  **Correct Inner Area Initialization:** Initialize the entire inner content area (defined as rows 2 through `height-2` and columns 1 through `width-2`) of the output grid to white (0).
3.  **Identify Seed Pixels:** Locate all pixels within the input grid's inner content area that have the `Output Fill Color`.
4.  **Place Seed Pixels:** Copy the identified seed pixels (and only those pixels) from the input's inner content area to the corresponding locations in the output grid's inner content area.
5.  **Refine Flood Fill:** Perform a 4-way flood fill starting *only* from the placed seed pixels. The fill should propagate the `Output Fill Color` into adjacent cells *within* the inner content area boundaries, but *only* if the target cell is currently white (0) in the output grid *and* the corresponding cell in the *input* grid was also white (0). This prevents the fill from overwriting non-seed colored pixels from the input and ensures it only fills the original background areas connected to the seed pixels.

**Metrics**


*code_execution:*
```python
import numpy as np
from collections import Counter

def analyze_example(input_grid_list):
    input_grid = np.array(input_grid_list)
    rows, cols = input_grid.shape
    metrics = {}

    # Grid Dimensions
    metrics['dimensions'] = {'height': rows, 'width': cols}

    # 1. Input Frame Color (derived from input_grid[1, 0])
    input_frame_color = 0
    if rows > 1 and cols > 0:
        input_frame_color = input_grid[1, 0]
    metrics['input_frame_color'] = int(input_frame_color)

    # 2. Inner Area Definition (Content Area)
    inner_row_start, inner_row_end = 2, rows - 2
    inner_col_start, inner_col_end = 1, cols - 2
    metrics['inner_area_indices'] = {
        'row_start': inner_row_start, 'row_end': inner_row_end,
        'col_start': inner_col_start, 'col_end': inner_col_end
    }

    # 3. Count inner colors (excluding white and frame color)
    color_counts = Counter()
    valid_inner_area = (inner_row_start <= inner_row_end and inner_col_start <= inner_col_end)
    seed_coords = []
    
    if valid_inner_area:
        inner_area = input_grid[inner_row_start:inner_row_end+1, inner_col_start:inner_col_end+1]
        for r_idx, r_val in enumerate(range(inner_row_start, inner_row_end + 1)):
            for c_idx, c_val in enumerate(range(inner_col_start, inner_col_end + 1)):
                color = inner_area[r_idx, c_idx]
                # Count for most frequent color determination
                if color != 0 and color != input_frame_color:
                    color_counts[color] += 1
                # Temporarily store all coordinates for potential seed identification later
                # (We need output_fill_color first)

    metrics['inner_color_counts_excluding_white_frame'] = dict(color_counts)

    # 4. Determine Output Fill Color
    output_fill_color = 0 # Default / fallback
    if color_counts:
        # Find the color with the maximum count.
        output_fill_color = max(color_counts, key=color_counts.get)
    metrics['output_fill_color'] = int(output_fill_color)

    # 5. Identify Seed Coordinates (Pixels in input inner area matching output_fill_color)
    if valid_inner_area and output_fill_color != 0:
         inner_area = input_grid[inner_row_start:inner_row_end+1, inner_col_start:inner_col_end+1]
         for r_idx, r_val in enumerate(range(inner_row_start, inner_row_end + 1)):
            for c_idx, c_val in enumerate(range(inner_col_start, inner_col_end + 1)):
                 if inner_area[r_idx, c_idx] == output_fill_color:
                     seed_coords.append({'row': r_val, 'col': c_val}) # Use absolute grid coords
                     
    metrics['seed_coordinates_count'] = len(seed_coords)
    # metrics['seed_coordinates'] = seed_coords # Keep output smaller for now

    return metrics

# Example Inputs (as lists of lists)
inputs = [
    [ # Example 1
        [1, 1, 2, 2, 3, 3, 4, 4, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 5, 0, 4],
        [4, 0, 0, 0, 5, 5, 0, 0, 0, 4], [4, 0, 0, 0, 5, 1, 1, 0, 0, 4],
        [4, 0, 5, 0, 5, 0, 0, 0, 0, 4], [4, 0, 1, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ],
    [ # Example 2
        [1, 1, 2, 2, 3, 3, 4, 4, 5, 5], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 3, 3, 3, 0, 0, 4, 2], [2, 0, 3, 3, 0, 3, 3, 4, 3, 2],
        [2, 0, 3, 0, 3, 0, 4, 3, 3, 2], [2, 0, 3, 4, 0, 0, 0, 3, 4, 2],
        [2, 0, 3, 0, 3, 3, 3, 4, 0, 2], [2, 0, 3, 3, 3, 4, 3, 3, 3, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 4, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ],
    [ # Example 3
        [1, 1, 2, 2, 3, 3, 4, 4, 5, 5], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 1], [1, 0, 0, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 4, 0, 1], [1, 4, 0, 0, 0, 4, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 4, 0, 0, 4, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]

print("--- Metrics Report ---")
for i, input_grid in enumerate(inputs):
    print(f"\nExample {i+1}:")
    metrics = analyze_example(input_grid)
    print(metrics)
print("--- End Report ---")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Metrics Report ---

Example 1:
{'dimensions': {'height': 10, 'width': 10}, 'input_frame_color': 4, 'inner_area_indices': {'row_start': 2, 'row_end': 8, 'col_start': 1, 'col_end': 8}, 'inner_color_counts_excluding_white_frame': {np.int64(5): 6, np.int64(1): 3}, 'output_fill_color': 5, 'seed_coordinates_count': 6}

Example 2:
{'dimensions': {'height': 10, 'width': 10}, 'input_frame_color': 2, 'inner_area_indices': {'row_start': 2, 'row_end': 8, 'col_start': 1, 'col_end': 8}, 'inner_color_counts_excluding_white_frame': {np.int64(3): 24, np.int64(4): 8}, 'output_fill_color': 3, 'seed_coordinates_count': 24}

Example 3:
{'dimensions': {'height': 10, 'width': 10}, 'input_frame_color': 1, 'inner_area_indices': {'row_start': 2, 'row_end': 8, 'col_start': 1, 'col_end': 8}, 'inner_color_counts_excluding_white_frame': {np.int64(2): 3, np.int64(4): 5}, 'output_fill_color': 4, 'seed_coordinates_count': 5}
--- End Report ---

```
**Facts**


```yaml
observations:
  - task_type: "frame_and_fill"
  - grid_dimensions: Consistent 10x10 in examples.
  - input_components:
      - top_row: A sequence of colors (indices 0,0 to 0,width-1). Seems decorative and is copied directly to the output.
      - input_frame: Defined by row 1 and potentially columns 0, width-1 and row height-1, though only row 1 is needed to determine its color.
      - content_area: A subgrid defined by rows 2 to height-2 and columns 1 to width-2. Contains various colored pixels and white (0) background pixels.
  - output_components:
      - top_row: Identical to the input top_row.
      - output_frame: Surrounds the content area. Consists of row 1, columns 0 and width-1 (from row 1 down), and row height-1. All pixels in the output frame are filled with the `Output Fill Color`.
      - content_area: Same dimensions as input content_area (rows 2 to height-2, columns 1 to width-2). Its content is derived from the input content_area.
  - color_determination:
      - input_frame_color: The color found in the input grid at row 1, column 0.
      - output_fill_color: The color that appears most frequently within the input content_area, excluding white (0) and the `input_frame_color`.
  - transformation_logic:
      - frame: The input frame is discarded. A new output frame is created using the `output_fill_color`.
      - content_area:
          - identify_seeds: Pixels within the input content_area that match the `output_fill_color` are identified as 'seeds'.
          - initialize_output_content: The output content_area is initially set to all white (0).
          - place_seeds: The identified seed pixels are copied from the input to their corresponding locations in the output content_area, overwriting the white background.
          - flood_fill: A fill operation starts from all seed pixels simultaneously. The `output_fill_color` spreads to adjacent (4-way) white pixels within the content_area boundaries, but only if the corresponding pixel in the *input* content_area was also white (0). Pixels in the input content_area that were neither white nor the `output_fill_color` are effectively ignored and remain white (0) in the output unless reached by the flood fill.

```


**Natural Language Program**

1.  **Get Input Dimensions:** Determine the height (`H`) and width (`W`) of the input grid.
2.  **Identify Input Frame Color:** Read the color value at `input_grid[1, 0]`. Store this as `Input Frame Color`.
3.  **Define Content Area:** Specify the boundaries for the content area: rows 2 to `H-2` (inclusive) and columns 1 to `W-2` (inclusive).
4.  **Count Content Colors:** Iterate through each pixel within the input grid's `Content Area`. Count the occurrences of each color, *excluding* white (0) and the `Input Frame Color`.
5.  **Determine Output Fill Color:** Find the color with the highest frequency count from Step 4. Store this as `Output Fill Color`. If no such colors exist or there's a tie (tie-breaking rule not explicitly defined, assume first max found), handle appropriately (though examples suggest a unique max exists).
6.  **Initialize Output Grid:** Create a new grid of the same dimensions (`H` x `W`) as the input grid, filled entirely with white (0).
7.  **Copy Top Row:** Copy the first row (index 0) from the input grid to the output grid.
8.  **Construct Output Frame:**
    *   Fill the entire second row (index 1) of the output grid with the `Output Fill Color`.
    *   Fill the first column (index 0) from row 1 down (rows 1 to `H-1`) with the `Output Fill Color`.
    *   Fill the last column (index `W-1`) from row 1 down (rows 1 to `H-1`) with the `Output Fill Color`.
    *   Fill the last row (index `H-1`) from column 1 to `W-2` (inclusive) with the `Output Fill Color`. (Note: Corners `[H-1, 0]` and `[H-1, W-1]` are already filled by the column fill).
9.  **Identify Seed Points:** Find all coordinates `(r, c)` within the input grid's `Content Area` (rows 2 to `H-2`, cols 1 to `W-2`) where the pixel color equals the `Output Fill Color`. Store these as `Seed Points`.
10. **Place Seeds in Output:** For each `(r, c)` in `Seed Points`, set the corresponding pixel `output_grid[r, c]` to the `Output Fill Color`. (The rest of the output `Content Area` remains white from Step 6).
11. **Perform Constrained Flood Fill:**
    *   Initialize a queue with all `Seed Points`.
    *   Initialize a set `visited` with all `Seed Points`.
    *   While the queue is not empty:
        *   Dequeue a coordinate `(r, c)`.
        *   For each 4-way adjacent neighbor `(nr, nc)` of `(r, c)`:
            *   Check if `(nr, nc)` is within the `Content Area` boundaries (rows 2 to `H-2`, cols 1 to `W-2`).
            *   Check if `(nr, nc)` has not been visited.
            *   Check if the target pixel in the output grid `output_grid[nr, nc]` is currently white (0).
            *   Check if the corresponding pixel in the *input* grid `input_grid[nr, nc]` is also white (0).
            *   If all conditions are true:
                *   Set `output_grid[nr, nc]` to the `Output Fill Color`.
                *   Mark `(nr, nc)` as visited.
                *   Enqueue `(nr, nc)`.
12. **Return Output Grid:** The final `output_grid` is the result.
