
## train_1

**input:**
```
7 5 7 7 5 5 7 7 5 7
0 0 0 7 7 5 5 7 7 5
0 0 0 7 5 5 7 5 7 7
0 0 0 5 7 5 7 5 7 7
7 7 5 5 5 5 7 5 5 5
7 5 7 5 7 7 5 5 7 5
7 5 7 7 5 5 5 7 7 7
7 0 0 5 5 5 7 5 7 5
5 0 0 7 5 0 0 7 5 7
7 0 0 5 5 0 0 5 7 7
```


**output:**
```
7 0 0 7 5 0 0 7 5 7
7 0 0 7 7 0 0 0 0 0
7 0 0 7 7 7 7 0 0 0
7 7 7 7 7 7 7 0 0 0
7 7 7 5 5 7 7 5 5 5
7 7 7 5 7 7 7 5 7 5
7 7 7 7 5 7 7 7 7 7
7 7 7 5 5 7 7 5 7 5
5 7 7 7 5 7 7 7 5 7
7 7 7 5 5 7 7 5 7 7
```


## train_2

**input:**
```
7 7 5 7 5 7 5 7
7 5 7 7 5 7 7 7
7 7 5 7 7 0 0 0
5 7 7 5 7 0 0 0
7 7 7 7 7 0 0 0
5 7 5 7 5 5 7 7
```


**output:**
```
7 7 5 7 5 7 5 7
7 5 7 7 5 7 7 7
0 0 0 7 7 7 7 7
0 0 0 7 7 7 7 7
0 0 0 7 7 7 7 7
5 7 5 7 5 5 7 7
```


## train_3

**input:**
```
5 5 5 7 0 0 0 0 5 5 5 7
5 7 5 5 0 0 0 0 7 5 5 5
5 7 7 7 0 0 0 0 7 5 7 7
5 7 7 5 5 7 5 5 5 7 7 5
7 7 5 7 5 5 7 5 5 7 7 5
7 5 7 5 5 5 5 5 5 7 7 5
7 5 7 7 5 5 5 5 0 0 0 0
7 7 7 5 7 7 5 5 0 0 0 0
5 7 7 7 7 7 5 7 5 7 5 5
7 5 5 5 7 5 5 7 5 5 7 5
7 5 0 5 7 5 7 7 5 7 5 5
7 5 0 7 5 5 5 5 5 7 5 5
```


**output:**
```
5 5 0 7 7 7 7 7 5 5 5 7
5 7 0 5 7 7 7 7 7 5 5 5
5 7 7 7 7 7 7 7 7 5 7 7
5 7 7 5 7 7 7 7 5 7 7 5
7 7 7 7 7 7 7 7 5 7 7 5
7 5 7 5 7 7 7 7 5 7 7 5
0 0 0 0 7 7 7 7 7 7 7 7
0 0 0 0 7 7 7 7 7 7 7 7
5 7 7 7 7 7 7 7 5 7 5 5
7 5 7 5 0 0 0 0 5 5 7 5
7 5 7 5 0 0 0 0 5 7 5 5
7 5 7 7 0 0 0 0 5 7 5 5
```

*   **Perception:**
    The task involves transforming pixels in a grid based on their local neighborhood. The transformation logic centers around the interaction between three specific colors: white (0), gray (5), and orange (7). The core rule depends on whether a pixel has *both* a gray neighbor and an orange neighbor within its 3x3 Moore neighborhood (including diagonals). The pixel's own color determines the outcome of the transformation when this neighborhood condition is met. Other colors and pixels not meeting the neighborhood condition remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: pixel_transformation
    transformation_scope: local_neighborhood
    neighborhood_type: Moore (3x3 including diagonals)
    key_colors:
      - name: white
        value: 0
      - name: gray
        value: 5
      - name: orange
        value: 7
    conditions:
      - name: neighbor_check
        description: Check if a pixel has at least one gray (5) neighbor AND at least one orange (7) neighbor.
        applies_to: all pixels
      - name: white_pixel_rule
        description: If neighbor_check is true AND the pixel's color is white (0), change the pixel's color to orange (7).
        input_color: 0
        output_color: 7
      - name: non_white_pixel_rule
        description: If neighbor_check is true AND the pixel's color is NOT white (0), change the pixel's color to white (0).
        input_color: non-0
        output_color: 0
      - name: default_rule
        description: If neighbor_check is false, the pixel's color remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Create a new grid with the same dimensions as the input grid, initially copying all pixel values from the input.
    2.  Iterate through each pixel (cell) of the input grid using its row and column index.
    3.  For the current pixel, examine its 8 neighbors (Moore neighborhood: adjacent horizontally, vertically, and diagonally).
    4.  Determine if at least one neighbor has the color gray (5) AND at least one neighbor has the color orange (7).
    5.  **If** this neighborhood condition (having both a gray and an orange neighbor) is **true**:
        *   Check the color of the current pixel in the *input* grid.
        *   **If** the current pixel's color is white (0), set the corresponding pixel in the *output* grid to orange (7).
        *   **Else if** the current pixel's color is *not* white (0), set the corresponding pixel in the *output* grid to white (0).
    6.  **Else if** the neighborhood condition (having both a gray and an orange neighbor) is **false**:
        *   The corresponding pixel in the *output* grid keeps its original color (copied in step 1).
    7.  After iterating through all pixels, the new grid represents the final output.
```python
import numpy as np

def transform(input_grid):
    """
    Transforms a grid based on the following rules applied to each pixel:
    1. Examine the 8 neighbors (Moore neighborhood) of the current pixel.
    2. Check if at least one neighbor is gray (5) AND at least one neighbor is orange (7).
    3. If this condition is true:
        a. If the current pixel is white (0), change it to orange (7) in the output grid.
        b. If the current pixel is NOT white (0), change it to white (0) in the output grid.
    4. If the condition is false, the pixel's color remains unchanged in the output grid.
    """

    # Convert input list of lists to a numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize the output grid as a copy of the input grid
    output_array = np.copy(input_array)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            has_gray_neighbor = False
            has_orange_neighbor = False

            # Iterate through the 8 neighbors (Moore neighborhood)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # Skip the center pixel itself
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_color = input_array[nr, nc]
                        # Check for gray neighbor
                        if neighbor_color == 5:
                            has_gray_neighbor = True
                        # Check for orange neighbor
                        if neighbor_color == 7:
                            has_orange_neighbor = True
            
            # Apply transformation rules if both gray and orange neighbors are found
            if has_gray_neighbor and has_orange_neighbor:
                current_pixel_color = input_array[r, c]
                # If the current pixel is white (0), change it to orange (7)
                if current_pixel_color == 0:
                    output_array[r, c] = 7
                # If the current pixel is not white (non-0), change it to white (0)
                else:
                    output_array[r, c] = 0
            # Otherwise (condition false), the pixel in output_array retains its original value (already copied)

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
```

Previous Code:
```python
import numpy as np

def transform(input_grid):
    """
    Transforms a grid based on the following rules applied to each pixel:
    1. Examine the 8 neighbors (Moore neighborhood) of the current pixel.
    2. Check if at least one neighbor is gray (5) AND at least one neighbor is orange (7).
    3. If this condition is true:
        a. If the current pixel is white (0), change it to orange (7) in the output grid.
        b. If the current pixel is NOT white (0), change it to white (0) in the output grid.
    4. If the condition is false, the pixel's color remains unchanged in the output grid.
    """

    # Convert input list of lists to a numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize the output grid as a copy of the input grid
    output_array = np.copy(input_array)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            has_gray_neighbor = False
            has_orange_neighbor = False

            # Iterate through the 8 neighbors (Moore neighborhood)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # Skip the center pixel itself
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_color = input_array[nr, nc]
                        # Check for gray neighbor
                        if neighbor_color == 5:
                            has_gray_neighbor = True
                        # Check for orange neighbor
                        if neighbor_color == 7:
                            has_orange_neighbor = True
            
            # Apply transformation rules if both gray and orange neighbors are found
            if has_gray_neighbor and has_orange_neighbor:
                current_pixel_color = input_array[r, c]
                # If the current pixel is white (0), change it to orange (7)
                if current_pixel_color == 0:
                    output_array[r, c] = 7
                # If the current pixel is not white (non-0), change it to white (0)
                else:
                    output_array[r, c] = 0
            # Otherwise (condition false), the pixel in output_array retains its original value (already copied)

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 5 7 7 5 5 7 7 5 7
0 0 0 7 7 5 5 7 7 5
0 0 0 7 5 5 7 5 7 7
0 0 0 5 7 5 7 5 7 7
7 7 5 5 5 5 7 5 5 5
7 5 7 5 7 7 5 5 7 5
7 5 7 7 5 5 5 7 7 7
7 0 0 5 5 5 7 5 7 5
5 0 0 7 5 0 0 7 5 7
7 0 0 5 5 0 0 5 7 7
```
Expected Output:
```
7 0 0 7 5 0 0 7 5 7
7 0 0 7 7 0 0 0 0 0
7 0 0 7 7 7 7 0 0 0
7 7 7 7 7 7 7 0 0 0
7 7 7 5 5 7 7 5 5 5
7 7 7 5 7 7 7 5 7 5
7 7 7 7 5 7 7 7 7 7
7 7 7 5 5 7 7 5 7 5
5 7 7 7 5 7 7 7 5 7
7 7 7 5 5 7 7 5 7 7
```
Transformed Output:
```
7 5 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
5 7 7 7 0 7 7 0 0 0
7 7 7 0 0 0 7 0 0 0
```
Match: False
Pixels Off: 69
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 138.0

## Example 2:
Input:
```
7 7 5 7 5 7 5 7
7 5 7 7 5 7 7 7
7 7 5 7 7 0 0 0
5 7 7 5 7 0 0 0
7 7 7 7 7 0 0 0
5 7 5 7 5 5 7 7
```
Expected Output:
```
7 7 5 7 5 7 5 7
7 5 7 7 5 7 7 7
0 0 0 7 7 7 7 7
0 0 0 7 7 7 7 7
0 0 0 7 7 7 7 7
5 7 5 7 5 5 7 7
```
Transformed Output:
```
0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
5 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0
5 0 5 0 0 0 0 7
```
Match: False
Pixels Off: 33
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 137.5

## Example 3:
Input:
```
5 5 5 7 0 0 0 0 5 5 5 7
5 7 5 5 0 0 0 0 7 5 5 5
5 7 7 7 0 0 0 0 7 5 7 7
5 7 7 5 5 7 5 5 5 7 7 5
7 7 5 7 5 5 7 5 5 7 7 5
7 5 7 5 5 5 5 5 5 7 7 5
7 5 7 7 5 5 5 5 0 0 0 0
7 7 7 5 7 7 5 5 0 0 0 0
5 7 7 7 7 7 5 7 5 7 5 5
7 5 5 5 7 5 5 7 5 5 7 5
7 5 0 5 7 5 7 7 5 7 5 5
7 5 0 7 5 5 5 5 5 7 5 5
```
Expected Output:
```
5 5 0 7 7 7 7 7 5 5 5 7
5 7 0 5 7 7 7 7 7 5 5 5
5 7 7 7 7 7 7 7 7 5 7 7
5 7 7 5 7 7 7 7 5 7 7 5
7 7 7 7 7 7 7 7 5 7 7 5
7 5 7 5 7 7 7 7 5 7 7 5
0 0 0 0 7 7 7 7 7 7 7 7
0 0 0 0 7 7 7 7 7 7 7 7
5 7 7 7 7 7 7 7 5 7 5 5
7 5 7 5 0 0 0 0 5 5 7 5
7 5 7 5 0 0 0 0 5 7 5 5
7 5 7 7 0 0 0 0 5 7 5 5
```
Transformed Output:
```
0 0 0 7 7 0 0 7 0 0 0 7
0 0 0 0 7 0 0 7 0 0 0 0
0 0 0 0 7 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 7 7 7 7
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 5
```
Match: False
Pixels Off: 102
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 141.66666666666666
