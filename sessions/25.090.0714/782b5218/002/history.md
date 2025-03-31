
## train_1

**input:**
```
5 5 5 0 5 0 0 0 5 5
5 0 0 5 5 0 5 0 5 5
0 5 5 0 5 5 0 5 0 0
2 0 5 5 2 0 5 0 2 5
5 2 0 2 0 2 0 2 0 2
0 0 2 5 5 5 2 0 5 0
5 5 0 0 0 5 5 5 5 5
0 5 0 5 5 0 5 0 5 5
0 5 5 0 5 0 5 0 5 5
5 5 0 0 5 5 5 5 5 5
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 2 0
5 2 0 2 5 2 0 2 5 2
5 5 2 5 5 5 2 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
```


## train_2

**input:**
```
1 0 1 1 1 1 1 1 1 0
0 0 1 0 1 1 0 1 0 1
1 1 0 0 1 1 1 1 1 0
2 2 2 2 2 2 2 2 2 2
0 0 1 1 0 0 0 0 0 0
1 1 0 1 0 0 0 0 1 0
0 1 1 1 0 1 1 0 1 0
1 1 0 0 0 1 0 0 1 0
0 0 1 0 0 0 1 1 0 0
0 1 1 1 0 1 1 0 0 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
```


## train_3

**input:**
```
0 8 8 0 8 0 8 8 0 0
2 0 8 8 0 8 0 0 0 8
2 2 8 0 0 0 0 0 0 0
0 2 2 0 8 0 0 0 0 0
8 8 2 2 0 0 0 8 8 0
8 8 8 2 2 8 0 0 0 0
0 0 0 0 2 2 8 8 8 0
8 0 8 0 0 2 2 8 8 8
8 8 0 0 0 0 2 2 8 0
0 8 0 8 0 8 8 2 2 8
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
8 2 2 0 0 0 0 0 0 0
8 8 2 2 0 0 0 0 0 0
8 8 8 2 2 0 0 0 0 0
8 8 8 8 2 2 0 0 0 0
8 8 8 8 8 2 2 0 0 0
8 8 8 8 8 8 2 2 0 0
8 8 8 8 8 8 8 2 2 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of the Elements:**

1.  **Grid Structure:** Both input and output are 2D grids of colored pixels. The size appears consistent between input and output for each example (10x10).
2.  **Key Colors:**
    *   **Red (2):** Appears to act as a critical marker or boundary within the grid. Its position seems fundamental to the transformation.
    *   **White (0):** Acts as a background or reset color in the output, particularly in areas above the red markers and in columns lacking red markers.
    *   **Other Colors (Gray-5, Blue-1, Azure-8):** These colors participate in the transformation, either being copied or used as a fill color below the red markers, depending on the example.
3.  **Columnar Processing:** The transformation seems to operate independently on each column, guided by the position of the red pixels within that column.
4.  **Vertical Boundary:** The *highest* red pixel (minimum row index) in each column serves as a vertical boundary.
5.  **Transformation Rules:**
    *   **Above Boundary:** Pixels located *above* the highest red pixel in a column are consistently replaced with white (0).
    *   **At Boundary:** The highest red pixel itself is preserved in the output.
    *   **Below Boundary:** The treatment of pixels *below* the highest red pixel varies:
        *   In `train_1`, the original pixel colors from the input seem to be copied into the output for positions at or below the highest red pixel.
        *   In `train_2` and `train_3`, the pixels below the highest red pixel are *filled* with a single, uniform color (blue-1 in `train_2`, azure-8 in `train_3`).
    *   **No Boundary:** If a column contains no red pixels, the entire column in the output becomes white (0).
6.  **Determining Fill vs. Copy:** There must be a condition that differentiates `train_1` (copy below) from `train_2` and `train_3` (fill below). Let's examine the overall color composition:
    *   `train_1`: Contains gray (5), red (2), white (0). The most frequent non-white/non-red color is gray (5). Output uses "copy".
    *   `train_2`: Contains blue (1), red (2), white (0). The most frequent non-white/non-red color is blue (1). Output uses "fill" with blue (1).
    *   `train_3`: Contains azure (8), red (2), white (0). The most frequent non-white/non-red color is azure (8). Output uses "fill" with azure (8).
    *   This suggests a rule: Find the most frequent color in the input grid, ignoring white (0) and red (2). If this color is gray (5), use the "copy" method below the red markers. Otherwise, use the "fill" method with this most frequent color.

**Facts (YAML):**


```yaml
task_description: Processes a grid column-wise based on the highest red pixel, clearing above and either copying or filling below.

elements:
  - element: grid
    properties:
      - type: 2D array of integers (colors)
      - dimensions: height, width (variable, constant per example pair)
  - element: pixel
    properties:
      - color: integer 0-9
      - position: (row, column)
  - element: column
    properties:
      - index: integer
      - contains_pixels: list of pixels

key_colors:
  - color: red (2)
    role: vertical boundary marker (highest occurrence per column is key)
  - color: white (0)
    role: clear color (used above marker, for columns without marker), ignored in frequency counts
  - color: gray (5)
    role: special case trigger (if most frequent non-0/2 color, triggers 'copy' mode)
  - color: other (e.g., blue-1, azure-8)
    role: potential fill color (if most frequent non-0/2 color and not gray-5)

relationships:
  - relationship: position
    properties:
      - above/below: relative row indices
      - highest: minimum row index for a specific color (red) in a column
  - relationship: frequency
    properties:
      - most_frequent_color: calculated across the grid, excluding white (0) and red (2)

actions:
  - action: find_most_frequent_color
    inputs: input_grid
    outputs: dominant_color
    constraints: ignore white (0) and red (2)
  - action: determine_mode
    inputs: dominant_color
    outputs: mode ('copy' or 'fill'), fill_color (if mode is 'fill')
    logic: if dominant_color is gray (5), mode is 'copy'; else mode is 'fill' and fill_color is dominant_color.
  - action: process_column
    inputs: input_column, mode, fill_color
    outputs: output_column
    logic:
      - Find highest red (2) pixel row 'r_red'.
      - If no red pixel, output column is all white (0).
      - If red pixel exists:
        - Output rows < r_red are white (0).
        - Output row r_red is red (2).
        - If mode is 'copy', output rows > r_red are copied from input_column.
        - If mode is 'fill', output rows > r_red are set to fill_color.
```


**Natural Language Program:**

1.  **Analyze Input:** Examine the entire input grid. Count the occurrences of each color, excluding white (0) and red (2). Identify the color with the highest frequency (the `dominant_color`).
2.  **Determine Mode:**
    *   If the `dominant_color` is gray (5), set the operation mode to `copy`.
    *   Otherwise (if the `dominant_color` is any other color), set the operation mode to `fill` and identify the `fill_color` as the `dominant_color`.
3.  **Initialize Output:** Create a new grid (`output_grid`) with the
```python
import numpy as np
from collections import Counter

def find_dominant_color(grid_np):
    """
    Finds the most frequent color in the grid, excluding white (0) and red (2).
    Returns the color value or None if no such color exists.
    """
    # Flatten the grid to easily count colors
    flat_grid = grid_np.flatten()
    
    # Filter out white (0) and red (2)
    filtered_colors = [color for color in flat_grid if color != 0 and color != 2]
    
    # Count frequencies
    if not filtered_colors:
        return None  # No relevant colors found
        
    color_counts = Counter(filtered_colors)
    
    # Find the most common color
    # If there's a tie, most_common(1) returns one of the most frequent
    dominant_color, _ = color_counts.most_common(1)[0]
    
    return dominant_color

def transform(input_grid):
    """
    Processes a grid column-wise based on the highest red pixel (2).
    
    1. Determines the most frequent color excluding white (0) and red (2).
    2. If the dominant color is gray (5), operates in 'copy' mode below the red pixel.
    3. Otherwise, operates in 'fill' mode below the red pixel using the dominant color.
    4. Pixels above the highest red pixel in a column are set to white (0).
    5. Columns without any red pixels are set entirely to white (0).
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize the output grid with white (0)
    output_np = np.zeros_like(input_np)
    
    # Step 1: Find the dominant color (excluding 0 and 2)
    dominant_color = find_dominant_color(input_np)
    
    # Step 2: Determine the mode and fill color
    mode = 'copy'  # Default mode if no dominant color found (though unlikely based on examples)
    fill_color = 0 # Default fill color (won't be used if mode is 'copy')
    
    if dominant_color is not None:
        if dominant_color == 5: # Gray
            mode = 'copy'
        else:
            mode = 'fill'
            fill_color = dominant_color
            
    # Step 3 & 4: Process each column
    for c in range(width):
        column = input_np[:, c]
        
        # Find the indices of red pixels (color 2) in the current column
        red_indices = np.where(column == 2)[0]
        
        # If no red pixels are found in the column, the output column remains white (already initialized)
        if len(red_indices) == 0:
            continue
            
        # Find the highest red pixel (minimum row index)
        r_red = np.min(red_indices)
        
        # Set the pixel at the highest red position in the output
        output_np[r_red, c] = 2
        
        # Process pixels below the highest red pixel based on the mode
        if mode == 'copy':
            # Copy the pixels from the input grid below the red pixel
            for r in range(r_red + 1, height):
                 output_np[r, c] = input_np[r, c]
        elif mode == 'fill':
            # Fill the pixels below the red pixel with the fill_color
            for r in range(r_red + 1, height):
                output_np[r, c] = fill_color
                
    # Convert the numpy array back to a list of lists for the final output
    return output_np.tolist()
```
