
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 0 0 0 0 0
2 1 1 1 0 0 0 0
0 1 1 1 0 0 0 0
0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 0 0 0 0 0
1 1 1 0 0 0 0 0
1 1 1 0 0 0 0 0
1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0
0 0 0 4 4 4 4 0
0 0 0 4 4 3 3 3
0 0 0 4 4 3 3 3
0 0 0 0 0 3 3 3
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0
0 0 0 4 4 4 4 0
0 0 0 4 3 3 3 0
0 0 0 4 3 3 3 0
0 0 0 0 3 3 3 0
```


## train_3

**input:**
```
0 4 4 4 0 0 0 0
0 4 4 4 0 0 0 0
0 4 4 4 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 0 0 0 0 0
4 4 4 0 0 0 0 0
4 4 4 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0
0 0 5 1 5 0 0 0
0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0
0 0 1 5 5 0 0 0
0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of Elements:**

The task involves grids containing two distinct non-white colored objects. The transformation depends on the specific pair of colors present. There appear to be two main types of transformations:
1.  **Object Shift:** One of the objects shifts its position horizontally (specifically, one column to the left). The object retains its color, overwriting pixels in its new path. Its original location becomes white.
2.  **Color Bleed:** One object remains static, while specific pixels of the *other* object, adjacent to the first, change their color to match the first object's color.

The key seems to be identifying which color pair triggers which transformation, which object is affected, and the precise rule for the change (which object shifts, or exactly which pixels change color).

**Observations:**

*   Each input grid contains exactly two non-white colors.
*   The relative positions vary: one object might be lower-right, or one might be inside the other.
*   The transformation rule depends on the specific pair of colors involved.
    *   Pairs {Blue(1), Red(2)} and {Yellow(4), Magenta(6)} result in the object with the *lower* color index (Blue=1, Yellow=4) shifting left by one column.
    *   Pairs {Green(3), Yellow(4)} and {Blue(1), Gray(5)} result in a "color bleed" where the color with the *lower* index (Green=3, Blue=1) changes the color of specific adjacent pixels of the *higher* index object.
*   For the "Color Bleed" cases:
    *   {Green(3), Yellow(4)}: Yellow pixels adjacent to Green pixels change to Green if the Green neighbor is directly to the right or directly below the Yellow pixel.
    *   {Blue(1), Gray(5)}: The single Gray pixel adjacent to the Blue pixel(s) that has the minimum column index (with row index as a tie-breaker) changes to Blue.

**YAML Facts:**

```
yaml
task_type: object_transformation
components:
  - role: grid
    elements:
      - role: background
        color: white
      - role: object
        count: 2 # Exactly two distinct non-white objects per grid
        properties:
          - color: non-white (1-9)
          - shape: variable (L-shape, rectangle, C-shape, single pixel)
          - connectivity: contiguous pixels of the same color

relationships:
  - type: color_pair_dependency
    description: The transformation rule is determined by the specific pair of non-white colors present.
  - type: spatial
    description: Objects can be adjacent, or one can enclose the other.

actions:
  - name: identify_colors
    inputs: input_grid
    outputs: color1, color2
  - name: determine_rule_type
    inputs: color1, color2
    outputs: action_type ('shift' or 'bleed'), lower_color_object, higher_color_object
    logic: |
      Based on the set {color1, color2}:
      If {1, 2} or {4, 6}, action_type is 'shift', lower_color_object is the actor.
      If {1, 5} or {3, 4}, action_type is 'bleed', lower_color_object dictates change on higher_color_object.
  - name: execute_shift
    inputs: input_grid, lower_color_object
    outputs: output_grid
    description: Translate the lower_color_object one column left, overwriting existing cells. Original object location becomes white.
  - name: execute_bleed
    inputs: input_grid, lower_color_object, higher_color_object, color_pair
    outputs: output_grid
    description: |
      Identify pixels P of higher_color_object adjacent to lower_color_object.
      If color_pair is {1, 5}:
        Find the single pixel P with min column index (tie-break min row). Change P to lower_color.
      If color_pair is {3, 4}:
        Find all pixels P that have a lower_color neighbor directly right OR directly below. Change these P to lower_color.

```

**Natural Language Program:**

1.  Identify the two unique non-white colors present in the input grid. Call them C1 and C2.
2.  Determine the color with the lower index (C_low = min(C1, C2)) and the color with the higher index (C_high = max(C1, C2)).
3.  Identify the object composed of C_low pixels (Object_low) and the object composed of C_high pixels (Object_high).
4.  Check the specific pair of colors {C_low, C_high}:
    a.  **If the pair is {1, 2} (Blue, Red) OR {4, 6} (Yellow, Magenta):**
        i.  The transformation is **Shift Left**.
        ii. Create the output grid by copying the input grid.
        iii. Find all coordinates originally occupied by Object_low. Clear these locations in the output grid (set to white/0).
        iv. Calculate the new coordinates for Object_low by subtracting 1 from the column index of each original pixel.
        v.  Fill these new coordinates in the output grid with the color C_low, overwriting any existing colors at those locations.
    b.  **If the pair is {1, 5} (Blue, Gray) OR {3, 4} (Green, Yellow):**
        i.  The transformation is **Color Bleed**.
        ii. Create the output grid by copying the input grid.
        iii. Find all pixels P belonging to Object_high that are adjacent (sharing an edge or corner) to any pixel belonging to Object_low. These are the candidate pixels.
        iv. **If the pair is {1, 5}:**
            1. From the candidate pixels, find the single pixel P that has the minimum column index. If multiple candidates share the minimum column index, choose the one among them with the minimum row index.
            2. Change the color of this selected pixel P in the output grid from C_high (Gray) to C_low (Blue).
        v.  **If the pair is {3, 4}:**
            1. For each candidate pixel P (color Yellow), check its neighbours.
            2. If P has a neighbour Q (color Green) located directly to its right (relative coordinate (0, 1)) OR directly below it (relative coordinate (1, 0)), then mark P for change.
            3. Change the color of all marked pixels P in the output grid from C_high (Yellow) to C_low (Green).
5.  Return the modified output grid.
```python
import copy

"""
Transforms the input grid based on the pair of non-white colors present.
The transformation depends on the specific pair of non-white colors (C1, C2) found in the grid.
Let C_low be the color with the lower index and C_high be the color with the higher index.

1.  If the pair is {1 (Blue), 2 (Red)} or {4 (Yellow), 6 (Magenta)}:
    - The object composed of C_low pixels is identified.
    - This object is shifted one column to the left.
    - The original positions of the shifted object become background (white, 0).
    - The shifted object overwrites any pixels in its new path.

2.  If the pair is {3 (Green), 4 (Yellow)}:
    - Pixels of color C_high (Yellow) are changed to color C_low (Green) if they have a C_low (Green) neighbor directly to their right OR directly below them.

3.  If the pair is {1 (Blue), 5 (Gray)}:
    - Pixels of color C_high (Gray) are changed to color C_low (Blue) if they have a C_low (Blue) neighbor directly to their right.
"""

def find_colors(grid: list[list[int]]) -> tuple[int | None, int | None]:
    """Finds the two unique non-background colors in the grid.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing the lower and higher color index (c_low, c_high),
        or (None, None) if exactly two non-white colors are not found.
    """
    colors = set()
    height = len(grid)
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                colors.add(grid[r][c])
    # Ensure exactly two colors are found
    if len(colors) != 2:
        return None, None
    color_list = sorted(list(colors))
    # Returns the color with the lower index first (c_low), then higher (c_high)
    return color_list[0], color_list[1]

def find_object_pixels(grid: list[list[int]], color: int) -> list[tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with the specified color.

    Args:
        grid: The input grid.
        color: The color value to find.

    Returns:
        A list of (row, col) tuples for pixels matching the color.
    """
    pixels = []
    height = len(grid)
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] == color:
                pixels.append((r, c))
    return pixels

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the pair of non-white colors present.
    """
    # Initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])

    # 1. Identify the two unique non-white colors and determine low/high index
    c_low, c_high = find_colors(input_grid)

    # If colors are not as expected (e.g., not exactly 2 non-white), return the original grid
    if c_low is None:
        print("Warning: Expected exactly two non-white colors, found different.")
        return output_grid

    color_pair = {c_low, c_high}

    # 2. Determine and execute the transformation based on the color pair

    # Case 1: Shift Left (pairs {1, 2} or {4, 6})
    if color_pair == {1, 2} or color_pair == {4, 6}:
        # Find original pixels of the object to be shifted (c_low)
        pixels_to_shift = find_object_pixels(input_grid, c_low)

        # Calculate new locations after shifting left
        new_pixel_locations = []
        for r, c in pixels_to_shift:
            new_c = c - 1
            # Check boundary conditions for the new column
            if 0 <= new_c < width:
                 new_pixel_locations.append((r, new_c))

        # Clear original locations in output grid
        # Note: This happens *before* painting new locations, correctly handling overlaps
        for r, c in pixels_to_shift:
            output_grid[r][c] = 0 # Set to white/background

        # Fill new locations in output grid with c_low
        for r, new_c in new_pixel_locations:
             output_grid[r][new_c] = c_low

    # Case 2: Color Bleed (pairs {1, 5} or {3, 4})
    elif color_pair == {1, 5} or color_pair == {3, 4}:
        # Find pixels of the higher color object (potential targets for change)
        pixels_high = find_object_pixels(input_grid, c_high)
        pixels_to_change = []

        # Iterate through the higher color pixels to check for required adjacency
        for r_high, c_high_px in pixels_high:
            change_pixel = False

            # Rule for {3, 4} (Green changes adjacent Yellow)
            if color_pair == {3, 4}:
                # Check if neighbor to the RIGHT (r_high, c_high_px + 1) is c_low (Green)
                has_green_right = (c_high_px + 1 < width and input_grid[r_high][c_high_px + 1] == c_low)
                # Check if neighbor BELOW (r_high + 1, c_high_px) is c_low (Green)
                has_green_below = (r_high + 1 < height and input_grid[r_high + 1][c_high_px] == c_low)
                # If either condition is true, mark for change
                if has_green_right or has_green_below:
                    change_pixel = True

            # Rule for {1, 5} (Blue changes adjacent Gray)
            elif color_pair == {1, 5}:
                 # Check if neighbor to the RIGHT (r_high, c_high_px + 1) is c_low (Blue)
                 # Rule: Gray pixel (r_high, c_high_px) changes if Blue pixel is at (r_high, c_high_px + 1)
                 if c_high_px + 1 < width and input_grid[r_high][c_high_px + 1] == c_low:
                     change_pixel = True

            # If conditions met, mark this pixel for color change
            if change_pixel:
                pixels_to_change.append((r_high, c_high_px))

        # Apply the color changes to the output grid
        for r_change, c_change in pixels_to_change:
            output_grid[r_change][c_change] = c_low

    # 3. Return the modified output grid
    return output_grid
```
