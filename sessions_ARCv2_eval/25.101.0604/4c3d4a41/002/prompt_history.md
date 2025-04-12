
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 3 0 2 0 5 0 5 0 5
0 5 0 0 0 0 0 5 0 5 0 3 0 2 0 4 0 7 0 5
0 5 0 5 0 0 0 5 0 5 0 3 0 2 0 4 0 7 0 5
0 5 0 5 0 5 0 5 0 0 0 0 0 2 0 4 0 0 0 5
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
```


**output:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 3 0 2 0 4 0 7 0 5
0 0 0 0 0 0 0 0 0 5 0 5 0 2 0 4 0 5 0 5
0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 4 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0 5
0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 5 0 5 0 4 0 5 0 5 0 8 0 5
0 5 0 0 0 0 0 5 0 5 0 4 0 6 0 7 0 8 0 5
0 5 0 5 0 5 0 5 0 0 0 0 0 6 0 7 0 0 0 5
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
```


**output:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 4 0 5 0 5 0 8 0 5
0 0 0 0 0 0 0 0 0 5 0 4 0 6 0 7 0 5 0 5
0 0 0 0 0 0 0 0 0 5 0 5 0 6 0 7 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0 5
0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
```

**Perception of Elements:**

1.  **Grid Structure:** The input and output are 2D grids of integers, representing colors (0=black, 5=blue, etc.). The grid dimensions remain constant (8x20 in the examples).
2.  **Background Color:** The color 0 acts as the background.
3.  **Frame Color:** The color 5 is significant. It forms a prominent, often rectangular or near-rectangular, "frame" or border in both input and output. This main frame appears largely preserved.
4.  **Other Colors:** Colors other than 0 and 5 exist within the frame. These colors change between input and output.
5.  **Positional Relationships:** The transformation seems highly dependent on the vertical relationship between adjacent cells (the cell directly below).
6.  **Types of 5s:** There appear to be three types of cells with color 5 in the input:
    *   **Main Frame:** A large connected component of 5s, usually touching the grid edges. These persist in the output.
    *   **Internal 5s:** Isolated 5s or small groups of 5s located *inside* the area enclosed by the Main Frame (e.g., `train_1` input at (1,15), (1,17)). These seem to change based on the cell below.
    *   **External 5s:** 5s located *outside* the area enclosed by the Main Frame (e.g., `train_1` input at (2,1), (3,3), etc.). These are removed (changed to 0) in the output.
7.  **Transformation Logic:** The core transformation involves:
    *   Preserving the Main Frame.
    *   Removing External 5s.
    *   Modifying Internal 5s based on the color of the cell below them.
    *   Modifying other internal colors (non-0, non-5) based on the color of the cell below them (specifically, changing to 5 if the cell below is 0 or potentially if it's the same color under certain conditions).

**YAML Facts:**

```yaml
elements:
  - object: grid
    properties:
      - type: 2D array of integers (colors)
      - size: constant (e.g., 8x20)
  - object: cell
    properties:
      - coordinates: (row, column)
      - color: integer (0-9)
  - object: color
    properties:
      - value: integer
      - role:
          - 0: background
          - 5: frame_color
          - others: content_colors
  - object: main_frame
    properties:
      - color: 5 (frame_color)
      - connectivity: largest connected component of frame_color cells
      - location: typically forms a border, potentially touching grid edges
    relationships:
      - encloses: inner_area
  - object: inner_area
    properties:
      - location: region enclosed by main_frame
      - content: cells containing background, frame_color, or content_colors
  - object: non_frame_5
    properties:
      - color: 5 (frame_color)
    relationships:
      - location: not part of main_frame
      - classification:
          - internal (inside inner_area)
          - external (outside inner_area)

actions:
  - action: identify_main_frame
    inputs:
      - input_grid
      - frame_color
    outputs:
      - set of main_frame cell coordinates
  - action: classify_non_frame_5s
    inputs:
      - input_grid
      - frame_color
      - main_frame coordinates
    outputs:
      - set of external_5 coordinates
      - set of internal_5 coordinates
  - action: transform_cell
    inputs:
      - current_cell (r, c)
      - input_grid
      - main_frame coordinates
    process:
      - determine current color `V_curr = input[r][c]`
      - determine color below `V_below = input[r+1][c]` (handle boundaries)
      - check if `(r, c)` is main_frame, internal_5, external_5, or other
      - apply rules based on type and `V_below`
    outputs:
      - output_color for cell (r, c)

rules:
  - rule: preserve_main_frame
    condition: cell is part of main_frame
    action: output_color = frame_color
  - rule: remove_external_5s
    condition: cell is an external_5
    action: output_color = background_color
  - rule: propagate_into_internal_5s
    condition: cell is an internal_5
    action: |
      if V_below is a content_color:
        output_color = V_below
      else:
        output_color = background_color
  - rule: fill_above_background
    condition: V_curr is a content_color AND V_below is background_color
    action: output_color = frame_color
  - rule: handle_vertical_repeats (less certain)
    condition: V_curr is a content_color AND V_below == V_curr
    action: output_color = frame_color (potentially only if at end of repeat sequence)
  - rule: default_copy
    condition: none of the above apply
    action: output_color = V_curr

```

**Natural Language Program:**

1.  Define the Frame Color as 5 and the Background Color as 0.
2.  Initialize the output grid as a copy of the input grid.
3.  Identify the largest connected component of Frame Color cells in the input grid that touches any edge of the grid; this is the "Main Frame".
4.  Identify all input cells `(r, c)` that have the Frame Color but are *not* part of the Main Frame. These are "Non-Frame 5s".
5.  Iterate through each Non-Frame 5 cell `(r, c)` identified in step 4:
    a.  Examine the color of the cell directly below it in the input grid, `V_below = input[r+1][c]` (treating out-of-bounds as Background Color).
    b.  If `V_below` is not the Background Color and not the Frame Color (i.e., it's a content color), set the `output[r][c]` to `V_below`.
    c.  Otherwise (if `V_below` is Background Color or Frame Color), set `output[r][c]` to Background Color.
6.  Iterate through all cells `(r, c)` in the grid, excluding the last row (i.e., for `r` from 0 to height-2):
    a.  Consider the input color `V_curr = input[r][c]` and the input color below `V_below = input[r+1][c]`.
    b.  If `V_curr` is *not* the Frame Color and *not* the Background Color (i.e., it's a content color):
        i.  If `V_below` is the Background Color, set `output[r][c]` to the Frame Color.
        (*Note: Leave other content colors unchanged from the initial copy, unless modified by step 5 or step 6.b.i. The rule for vertical repeats seems inconsistent or complex and is omitted for clarity, relying on the above two rules which cover many observed changes.*)
7.  The final output grid contains the result of these modifications.
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms a 2D grid based on the following rules:
1. Defines a Frame Color (5) and a Background Color (0).
2. Identifies the "Main Frame": the largest connected component of Frame Color cells that touches any edge of the grid.
3. Initializes the output grid as a copy of the input grid.
4. Modifies cells that have the Frame Color in the input but are *not* part of the Main Frame ("Non-Frame 5s"):
    a. If the cell directly below a Non-Frame 5 in the input grid contains a "content color" (neither Frame Color nor Background Color), the Non-Frame 5 cell in the output grid takes the color of the cell below.
    b. Otherwise (if the cell below is Frame Color or Background Color, or if it's the last row), the Non-Frame 5 cell in the output grid becomes Background Color.
5. Modifies cells that contain a "content color" in the input grid:
    a. If the cell directly below such a cell in the input grid is Background Color, the content color cell in the output grid becomes Frame Color.
6. Cells belonging to the Main Frame and cells not otherwise modified retain their original color.
"""

def find_main_frame_mask(grid: np.ndarray, frame_color: int) -> np.ndarray:
    """
    Identifies the largest connected component of frame_color cells
    that touches any edge of the grid.
    Returns a boolean mask where True indicates a cell is part of the main frame.
    """
    H, W = grid.shape
    # Create a binary mask where frame_color cells are True
    binary_mask = (grid == frame_color)
    
    # Label connected components
    labeled_array, num_features = label(binary_mask)
    
    if num_features == 0:
        return np.zeros_like(grid, dtype=bool) # No frame color cells found

    # Find the locations of each labeled component
    component_slices = find_objects(labeled_array)
    
    largest_edge_component_label = 0
    max_size = -1

    for i in range(1, num_features + 1):
        component_mask = (labeled_array == i)
        component_size = np.sum(component_mask)
        
        # Check if this component touches any edge
        touches_edge = False
        coords = np.argwhere(component_mask)
        for r, c in coords:
            if r == 0 or r == H - 1 or c == 0 or c == W - 1:
                touches_edge = True
                break
        
        # If it touches an edge and is larger than the current max, update
        if touches_edge and component_size > max_size:
            max_size = component_size
            largest_edge_component_label = i
            
    if largest_edge_component_label == 0:
         # Fallback: if no component touches the edge, maybe it's just the largest? 
         # Or maybe there's no 'main frame' according to the definition.
         # Let's stick to the definition: if none touch edge, return empty mask.
         # Revisit if tests fail.
         # Alternative: Find largest overall component if none touch edge?
         # Let's check if any component exists first. If so, maybe pick the largest regardless of edge.
         # Re-evaluating: The examples clearly show a large frame, usually touching edges.
         # If no component touches the edge, assume there's no main frame by this definition.
         return np.zeros_like(grid, dtype=bool)


    # Create the final mask for the largest edge-touching component
    main_frame_mask = (labeled_array == largest_edge_component_label)
    
    return main_frame_mask


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Convert input to numpy array for easier processing
    input_arr = np.array(input_grid, dtype=int)
    H, W = input_arr.shape
    
    # Initialize output grid as a copy of the input
    output_arr = np.copy(input_arr)
    
    FRAME_COLOR = 5
    BACKGROUND_COLOR = 0

    # 1. Identify the Main Frame
    main_frame_mask = find_main_frame_mask(input_arr, FRAME_COLOR)

    # 2. Process Non-Frame 5s
    for r in range(H):
        for c in range(W):
            # Check if the current cell is a '5' but NOT part of the main frame
            if input_arr[r, c] == FRAME_COLOR and not main_frame_mask[r, c]:
                # Check the cell below
                if r + 1 < H:
                    v_below = input_arr[r + 1, c]
                    # Rule 4a: If below is content color, propagate up
                    if v_below != BACKGROUND_COLOR and v_below != FRAME_COLOR:
                        output_arr[r, c] = v_below
                    # Rule 4b: Otherwise, set to background
                    else:
                        output_arr[r, c] = BACKGROUND_COLOR
                else:
                    # Rule 4b (boundary case): Last row, set to background
                    output_arr[r, c] = BACKGROUND_COLOR

    # 3. Process Content Colors (check input, modify output)
    # Note: We iterate up to H-2 because we look at the cell below (r+1)
    for r in range(H - 1):
        for c in range(W):
            current_color = input_arr[r, c]
            # Check if it's a content color
            if current_color != BACKGROUND_COLOR and current_color != FRAME_COLOR:
                v_below = input_arr[r + 1, c]
                # Rule 5a: If cell below is background, change current cell to Frame Color
                if v_below == BACKGROUND_COLOR:
                    output_arr[r, c] = FRAME_COLOR
                    
    # Convert the result back to a list of lists
    output_grid = output_arr.tolist()
    
    return output_grid

```
