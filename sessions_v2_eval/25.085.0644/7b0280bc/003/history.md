
Previous Code:
```python
import collections
import copy

"""
Identifies the background color (assumed to be the color of the top-left pixel).
Performs a flood fill starting from all background-colored pixels on the border of the grid. 
This marks all background pixels reachable from the outside ('outside' pixels).
Creates a copy of the input grid.
Iterates through each pixel of the grid. If a pixel is not background-colored and was not reached by the flood fill (i.e., it's 'inside' an enclosure formed by non-background colors), its color is potentially changed based on specific rules that depend on both the grid's background color and the pixel's original color:

Rule Set:
- If background is azure (8):
  - white (0) becomes gray (5)
  - red (2) becomes green (3)
- If background is maroon (9):
  - yellow (4) becomes gray (5)
  - orange (7) becomes green (3)
- If background is orange (7):
  - blue (1) becomes green (3)
  - magenta (6) becomes gray (5)

Pixels that are 'inside' but do not match any applicable rule for the specific background color retain their original color. Pixels that are part of the background or are 'outside' also retain their original color.
The modified grid is returned.
"""

def transform(input_grid):
    """
    Transforms the input grid based on enclosed regions and color-specific rules.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Handle edge case of empty grid
    if rows == 0 or cols == 0:
        return []

    # 1. Determine background color (assuming top-left corner)
    bg_color = input_grid[0][0]

    # 2. Perform flood fill to identify 'outside' background cells
    is_outside = [[False for _ in range(cols)] for _ in range(rows)]
    q = collections.deque()

    # Seed the queue with background-colored border cells
    for r in range(rows):
        if input_grid[r][0] == bg_color and not is_outside[r][0]:
            is_outside[r][0] = True
            q.append((r, 0))
        if input_grid[r][cols - 1] == bg_color and not is_outside[r][cols - 1]:
            is_outside[r][cols - 1] = True
            q.append((r, cols - 1))
    # Avoid adding corners twice
    for c in range(1, cols - 1):
        if input_grid[0][c] == bg_color and not is_outside[0][c]:
            is_outside[0][c] = True
            q.append((0, c))
        if input_grid[rows - 1][c] == bg_color and not is_outside[rows - 1][c]:
            is_outside[rows - 1][c] = True
            q.append((rows - 1, c))

    # Run the flood fill
    while q:
        r, c = q.popleft()
        # Explore 4-direction neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is background color and hasn't been visited
                if not is_outside[nr][nc] and input_grid[nr][nc] == bg_color:
                    is_outside[nr][nc] = True
                    q.append((nr, nc))

    # 3. Create the output grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # 4. Iterate through all cells and apply transformation rules to 'inside' non-background cells
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is 'inside' (not marked as outside) 
            # AND is not the background color itself
            if not is_outside[r][c] and input_grid[r][c] != bg_color:
                current_color = input_grid[r][c]
                new_color = current_color  # Default: color remains unchanged

                # Apply transformation rules based on background color
                if bg_color == 8:  # azure background
                    if current_color == 0: new_color = 5  # white -> gray
                    elif current_color == 2: new_color = 3  # red -> green
                elif bg_color == 9:  # maroon background
                    if current_color == 4: new_color = 5  # yellow -> gray
                    elif current_color == 7: new_color = 3  # orange -> green
                elif bg_color == 7:  # orange background
                    if current_color == 1: new_color = 3  # blue -> green
                    elif current_color == 6: new_color = 5  # magenta -> gray
                
                # Update the output grid if the color changed
                if new_color != current_color:
                    output_grid[r][c] = new_color

    # 5. Return the transformed grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 0 2 2 8 8 8 8 8 1 1 8
8 8 8 8 8 8 0 8 2 2 8 8 8 8 8 1 1 8
8 8 2 2 8 0 8 8 8 0 8 8 8 8 0 8 0 8
8 8 2 2 0 8 8 8 8 0 8 8 8 0 8 8 0 8
8 8 0 8 8 8 8 8 8 0 8 8 8 0 8 8 0 8
8 8 0 8 8 8 8 8 8 0 8 8 8 0 8 8 0 8
8 8 8 0 8 8 8 8 8 0 8 8 0 8 8 8 0 8
8 8 8 0 8 8 8 8 8 8 0 8 2 2 8 8 0 8
8 8 8 1 1 8 8 8 8 8 0 8 2 2 8 8 0 8
8 8 8 1 1 8 8 8 8 8 0 8 8 8 8 8 0 8
8 8 8 0 8 8 8 8 8 8 0 8 8 8 8 0 8 8
8 8 8 8 0 8 8 8 8 8 0 8 8 8 0 8 8 8
8 8 8 8 0 8 8 8 8 8 2 2 8 0 8 8 8 8
8 8 8 8 2 2 8 8 0 0 2 2 0 8 8 8 8 8
8 8 8 8 2 2 0 0 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 0 2 2 8 8 8 8 8 1 1 8
8 8 8 8 8 8 0 8 2 2 8 8 8 8 8 1 1 8
8 8 2 2 8 0 8 8 8 0 8 8 8 8 0 8 5 8
8 8 2 2 0 8 8 8 8 0 8 8 8 0 8 8 5 8
8 8 0 8 8 8 8 8 8 0 8 8 8 0 8 8 5 8
8 8 0 8 8 8 8 8 8 0 8 8 8 0 8 8 5 8
8 8 8 0 8 8 8 8 8 0 8 8 0 8 8 8 5 8
8 8 8 0 8 8 8 8 8 8 0 8 2 2 8 8 5 8
8 8 8 1 1 8 8 8 8 8 0 8 2 2 8 8 5 8
8 8 8 1 1 8 8 8 8 8 0 8 8 8 8 8 5 8
8 8 8 5 8 8 8 8 8 8 0 8 8 8 8 5 8 8
8 8 8 8 5 8 8 8 8 8 0 8 8 8 5 8 8 8
8 8 8 8 5 8 8 8 8 8 3 3 8 5 8 8 8 8
8 8 8 8 3 3 8 8 5 5 3 3 5 8 8 8 8 8
8 8 8 8 3 3 5 5 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 5 3 3 8 8 8 8 8 1 1 8
8 8 8 8 8 8 5 8 3 3 8 8 8 8 8 1 1 8
8 8 3 3 8 5 8 8 8 5 8 8 8 8 5 8 5 8
8 8 3 3 5 8 8 8 8 5 8 8 8 5 8 8 5 8
8 8 5 8 8 8 8 8 8 5 8 8 8 5 8 8 5 8
8 8 5 8 8 8 8 8 8 5 8 8 8 5 8 8 5 8
8 8 8 5 8 8 8 8 8 5 8 8 5 8 8 8 5 8
8 8 8 5 8 8 8 8 8 8 5 8 3 3 8 8 5 8
8 8 8 1 1 8 8 8 8 8 5 8 3 3 8 8 5 8
8 8 8 1 1 8 8 8 8 8 5 8 8 8 8 8 5 8
8 8 8 5 8 8 8 8 8 8 5 8 8 8 8 5 8 8
8 8 8 8 5 8 8 8 8 8 5 8 8 8 5 8 8 8
8 8 8 8 5 8 8 8 8 8 3 3 8 5 8 8 8 8
8 8 8 8 3 3 8 8 5 5 3 3 5 8 8 8 8 8
8 8 8 8 3 3 5 5 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 35
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 21.604938271604937

## Example 2:
Input:
```
9 9 9 9 9 9 4 7 7 4 9 9 9 9 9
9 9 9 7 7 4 9 7 7 9 4 6 6 9 9
9 9 9 7 7 9 9 9 9 9 9 6 6 4 9
9 9 9 4 9 4 9 9 9 9 9 9 9 9 4
9 9 9 4 9 9 4 9 9 9 9 9 9 9 4
9 4 6 6 9 9 9 4 9 9 9 9 9 4 9
4 9 6 6 9 9 9 4 9 9 9 9 7 7 9
4 9 9 9 9 9 9 7 7 4 4 4 7 7 9
4 9 9 9 9 9 9 7 7 9 9 9 9 4 9
4 9 7 7 4 9 9 9 4 9 9 9 9 4 9
4 9 7 7 9 4 9 9 9 4 9 9 4 9 9
4 9 9 9 9 4 9 9 9 4 9 9 4 9 9
9 4 9 9 9 7 7 9 9 7 7 9 4 9 9
9 9 4 4 4 7 7 9 9 7 7 9 7 7 9
9 9 9 9 9 9 9 9 9 9 9 9 7 7 9
```
Expected Output:
```
9 9 9 9 9 9 5 3 3 5 9 9 9 9 9
9 9 9 3 3 5 9 3 3 9 5 6 6 9 9
9 9 9 3 3 9 9 9 9 9 9 6 6 4 9
9 9 9 5 9 4 9 9 9 9 9 9 9 9 4
9 9 9 5 9 9 4 9 9 9 9 9 9 9 4
9 4 6 6 9 9 9 4 9 9 9 9 9 4 9
4 9 6 6 9 9 9 4 9 9 9 9 7 7 9
4 9 9 9 9 9 9 7 7 4 4 4 7 7 9
4 9 9 9 9 9 9 7 7 9 9 9 9 4 9
4 9 7 7 4 9 9 9 4 9 9 9 9 4 9
4 9 7 7 9 4 9 9 9 4 9 9 4 9 9
4 9 9 9 9 4 9 9 9 4 9 9 4 9 9
9 4 9 9 9 7 7 9 9 7 7 9 4 9 9
9 9 4 4 4 7 7 9 9 7 7 9 7 7 9
9 9 9 9 9 9 9 9 9 9 9 9 7 7 9
```
Transformed Output:
```
9 9 9 9 9 9 5 3 3 5 9 9 9 9 9
9 9 9 3 3 5 9 3 3 9 5 6 6 9 9
9 9 9 3 3 9 9 9 9 9 9 6 6 5 9
9 9 9 5 9 5 9 9 9 9 9 9 9 9 5
9 9 9 5 9 9 5 9 9 9 9 9 9 9 5
9 5 6 6 9 9 9 5 9 9 9 9 9 5 9
5 9 6 6 9 9 9 5 9 9 9 9 3 3 9
5 9 9 9 9 9 9 3 3 5 5 5 3 3 9
5 9 9 9 9 9 9 3 3 9 9 9 9 5 9
5 9 3 3 5 9 9 9 5 9 9 9 9 5 9
5 9 3 3 9 5 9 9 9 5 9 9 5 9 9
5 9 9 9 9 5 9 9 9 5 9 9 5 9 9
9 5 9 9 9 3 3 9 9 3 3 9 5 9 9
9 9 5 5 5 3 3 9 9 3 3 9 3 3 9
9 9 9 9 9 9 9 9 9 9 9 9 3 3 9
```
Match: False
Pixels Off: 57
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.66666666666666

## Example 3:
Input:
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 1 1 6 6 6 6 6 6 7 7 7 7 7 7 7 7 7 7
7 7 1 1 7 7 7 7 7 7 6 6 6 6 7 7 7 7 7 7
7 7 6 7 7 7 7 7 7 7 7 7 7 7 6 7 7 7 7 7
7 7 6 7 7 7 7 7 7 7 7 7 7 2 2 7 7 7 7 7
7 7 6 7 7 7 7 7 7 7 7 7 6 2 2 7 7 7 7 7
7 7 6 7 7 7 7 7 7 7 7 6 7 7 6 7 7 7 7 7
7 7 6 7 7 7 7 7 7 7 1 1 7 7 6 7 7 7 7 7
7 6 6 7 7 7 7 7 7 7 1 1 7 7 6 7 7 7 7 7
7 6 7 7 7 7 7 7 7 7 6 7 7 7 6 7 7 7 7 7
7 6 7 7 7 7 7 1 1 7 6 7 7 7 7 6 7 7 7 7
7 6 7 7 7 7 6 1 1 6 7 7 7 7 7 6 7 7 7 7
7 6 7 7 7 6 7 7 7 7 7 7 7 7 7 7 6 7 7 7
7 6 7 7 1 1 7 7 7 7 7 7 7 7 7 7 6 7 7 7
7 6 7 7 1 1 6 6 7 7 7 7 7 7 7 6 7 7 7 7
7 6 7 7 6 7 7 7 6 6 7 7 7 7 1 1 7 7 7 7
7 6 7 6 7 7 7 7 7 7 6 6 6 6 1 1 7 7 7 7
7 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 3 3 5 5 5 5 5 5 7 7 7 7 7 7 7 7 7 7
7 7 3 3 7 7 7 7 7 7 5 5 5 5 7 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 7 7 7 7 5 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 7 7 7 2 2 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 7 7 6 2 2 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 7 6 7 7 6 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 1 1 7 7 6 7 7 7 7 7
7 5 5 7 7 7 7 7 7 7 1 1 7 7 6 7 7 7 7 7
7 5 7 7 7 7 7 7 7 7 6 7 7 7 6 7 7 7 7 7
7 5 7 7 7 7 7 1 1 7 6 7 7 7 7 6 7 7 7 7
7 5 7 7 7 7 6 1 1 6 7 7 7 7 7 6 7 7 7 7
7 5 7 7 7 6 7 7 7 7 7 7 7 7 7 7 6 7 7 7
7 5 7 7 1 1 7 7 7 7 7 7 7 7 7 7 6 7 7 7
7 5 7 7 1 1 6 6 7 7 7 7 7 7 7 6 7 7 7 7
7 5 7 7 6 7 7 7 6 6 7 7 7 7 1 1 7 7 7 7
7 5 7 6 7 7 7 7 7 7 6 6 6 6 1 1 7 7 7 7
7 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Transformed Output:
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 3 3 5 5 5 5 5 5 7 7 7 7 7 7 7 7 7 7
7 7 3 3 7 7 7 7 7 7 5 5 5 5 7 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 7 7 7 7 5 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 7 7 7 2 2 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 7 7 5 2 2 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 7 5 7 7 5 7 7 7 7 7
7 7 5 7 7 7 7 7 7 7 3 3 7 7 5 7 7 7 7 7
7 5 5 7 7 7 7 7 7 7 3 3 7 7 5 7 7 7 7 7
7 5 7 7 7 7 7 7 7 7 5 7 7 7 5 7 7 7 7 7
7 5 7 7 7 7 7 3 3 7 5 7 7 7 7 5 7 7 7 7
7 5 7 7 7 7 5 3 3 5 7 7 7 7 7 5 7 7 7 7
7 5 7 7 7 5 7 7 7 7 7 7 7 7 7 7 5 7 7 7
7 5 7 7 3 3 7 7 7 7 7 7 7 7 7 7 5 7 7 7
7 5 7 7 3 3 5 5 7 7 7 7 7 7 7 5 7 7 7 7
7 5 7 7 5 7 7 7 5 5 7 7 7 7 3 3 7 7 7 7
7 5 7 5 7 7 7 7 7 7 5 5 5 5 3 3 7 7 7 7
7 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Match: False
Pixels Off: 42
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 21.0
Okay, let's analyze the results and refine the understanding of the task.

## General Assessment

The previous code correctly identified the core concepts: using the background color, finding enclosed areas via flood fill, and applying color transformations within those areas. However, the results show that the transformation rules were applied too broadly. The code changed *all* non-background pixels inside *any* enclosure, whereas the expected outputs indicate that the transformation should only apply under more specific conditions.

The key insight from comparing the failed examples is that the transformation seems dependent not only on the background color and the enclosed pixel's color but also on the color of the **immediate border** surrounding the enclosed pixel(s). Pixels enclosed by borders of certain colors change, while pixels enclosed by borders of other colors do not, even if they are the same color and within an enclosed region relative to the background.

**Strategy:**
1.  Refine the definition of "enclosed" pixels that are candidates for transformation. They must not only be unreachable by the background flood fill but also be directly adjacent only to non-background colors.
2.  Identify the color of the immediate border surrounding these candidate pixels.
3.  Update the transformation rules to include a condition based on this border color, which itself seems dependent on the background color.

## Metrics and Observations (Qualitative)

*   **Example 1 (BG=Azure, 8):**
    *   Input enclosed colors: White(0), Red(2), Blue(1).
    *   Expected changes: Only White(0) -> Gray(5) and Red(2) -> Green(3) when the immediate border is White(0). Pixels enclosed by Blue(1) or Red(2) borders remain unchanged.
    *   Code incorrectly changed pixels enclosed by Red(2) borders and some pixels enclosed by White(0) that were part of larger structures. The refined rule suggests checking the immediate neighbors.

*   **Example 2 (BG=Maroon, 9):**
    *   Input enclosed colors: Yellow(4), Orange(7), Magenta(6).
    *   Expected changes: Only Yellow(4) -> Gray(5) and Orange(7) -> Green(3) when the immediate border is Yellow(4). Pixels enclosed by Magenta(6) or Orange(7) borders remain unchanged.
    *   Code incorrectly changed pixels enclosed by Magenta(6) and Orange(7) borders.

*   **Example 3 (BG=Orange, 7):**
    *   Input enclosed colors: Blue(1), Magenta(6), Red(2).
    *   Expected changes: Only Blue(1) -> Green(3) and Magenta(6) -> Gray(5) when the immediate border is Magenta(6). Pixels enclosed by Blue(1) or Red(2) borders remain unchanged.
    *   Code incorrectly changed pixels enclosed by Blue(1) and Red(2) borders.

**Common Pattern:**
The transformation `(Original Color -> New Color)` happens only for pixels inside an enclosure formed by a specific `Trigger Border Color`. This `Trigger Border Color` is determined by the `Background Color`.

*   BG Azure(8) => Trigger Border White(0) => Rules: White(0)->Gray(5), Red(2)->Green(3)
*   BG Maroon(9) => Trigger Border Yellow(4) => Rules: Yellow(4)->Gray(5), Orange(7)->Green(3)
*   BG Orange(7) => Trigger Border Magenta(6) => Rules: Blue(1)->Green(3), Magenta(6)->Gray(5)

## Facts


```yaml
task_context:
  problem_type: color_transformation_based_on_enclosure_and_border
  grid_properties:
    - variable_size
    - uses_multiple_colors (0-9)
  background_color_determination: color_of_top_left_pixel

objects:
  - object: background
    definition: contiguous area of the background color reachable from the grid borders
    properties:
      - color: determined_by_top_left_pixel
      - location: extends_from_borders_inward

  - object: enclosure_border
    definition: contiguous structure of one or more non-background pixels separating an 'inside' area from the 'outside' background
    properties:
      - color: non_background_color
      - location: forms_boundary
      - role: potentially_triggers_transformation

  - object: enclosed_pixel
    definition: a single pixel not belonging to the background and not reachable by a flood fill starting from the background pixels on the border
    properties:
      - color: non_background_color
      - location: inside_an_enclosure
      - neighbors: adjacent_pixels_(4_directions)

actions_and_transformations:
  - action: identify_background_color
    source: pixel at (0, 0)
    target: global_variable (bg_color)

  - action: identify_outside_area
    method: flood_fill
    start_points: all background-colored pixels on the grid borders
    fill_color: background_color
    result: marks all reachable background pixels ('outside')

  - action: identify_candidate_pixels_for_change
    definition: pixels that are not 'outside' and not the background color
    condition: must be fully surrounded by non-background colors (check 4 neighbors)

  - action: determine_immediate_border_color
    input: candidate_pixel
    method: check the color of all 4-directional neighbors
    condition: requires neighbors to be consistent non-background color for transformation trigger (assumption: border is uniform color for trigger)
    output: border_color

  - action: apply_color_transformation
    target: candidate_pixels
    conditions:
      - candidate_pixel's location is 'inside' (not marked by flood fill)
      - candidate_pixel is not background_color
      - candidate_pixel's immediate border color matches the specific 'trigger_border_color' associated with the background_color
      - candidate_pixel's color matches one of the 'original_colors' in the rule set for the current background_color and trigger_border_color
    rule_sets:
      - condition: background_color == 8 (azure) AND trigger_border_color == 0 (white)
        rules:
          - original_color: 0 (white) => new_color: 5 (gray)
          - original_color: 2 (red) => new_color: 3 (green)
      - condition: background_color == 9 (maroon) AND trigger_border_color == 4 (yellow)
        rules:
          - original_color: 4 (yellow) => new_color: 5 (gray)
          - original_color: 7 (orange) => new_color: 3 (green)
      - condition: background_color == 7 (orange) AND trigger_border_color == 6 (magenta)
        rules:
          - original_color: 1 (blue) => new_color: 3 (green)
          - original_color: 6 (magenta) => new_color: 5 (gray)
    effect: changes the color of the matching candidate_pixel in the output grid

  - action: preserve_color
    target: all other pixels (background, outside pixels, enclosed pixels not meeting transformation conditions)
    effect: color remains unchanged in the output grid
```


## Natural Language Program

1.  **Determine Background Color**: Identify the background color (`bg_color`) from the top-left pixel of the input grid.
2.  **Identify Outside Area**: Perform a flood fill starting from all `bg_color` pixels located on the borders of the grid. Mark all reachable `bg_color` pixels as 'outside'.
3.  **Create Output Grid**: Initialize the output grid as a copy of the input grid.
4.  **Iterate Through Pixels**: For each pixel `(r, c)` in the grid:
    a.  **Check if Candidate**: Determine if the pixel at `(r, c)` is a potential candidate for transformation. It is a candidate if:
        i.  It was *not* marked as 'outside' by the flood fill.
        ii. Its color is *not* the `bg_color`.
    b.  **Check Immediate Border**: If the pixel is a candidate, examine its 4-directional neighbors (up, down, left, right).
        i.  If *any* neighbor is `bg_color` or outside the grid bounds, this pixel is touching the background directly or indirectly and is *not* eligible for transformation based on border color. Skip to the next pixel.
        ii. If *all* neighbors are within bounds and are *not* `bg_color`, determine the color(s) of these neighbors. Assume for the transformation trigger that these neighbors share a single, uniform color (`border_color`).
    c.  **Determine Trigger Border Color**: Based on the `bg_color`, identify the required `trigger_border_color`:
        *   If `bg_color` is Azure (8), `trigger_border_color` is White (0).
        *   If `bg_color` is Maroon (9), `trigger_border_color` is Yellow (4).
        *   If `bg_color` is Orange (7), `trigger_border_color` is Magenta (6).
    d.  **Apply Transformation Rules**: If the determined `border_color` from step 4.b.ii matches the `trigger_border_color` from step 4.c, apply the following color changes to the candidate pixel at `(r, c)` in the output grid:
        *   If `bg_color` is Azure (8) and `border_color` is White (0):
            *   Change White (0) to Gray (5).
            *   Change Red (2) to Green (3).
        *   If `bg_color` is Maroon (9) and `border_color` is Yellow (4):
            *   Change Yellow (4) to Gray (5).
            *   Change Orange (7) to Green (3).
        *   If `bg_color` is Orange (7) and `border_color` is Magenta (6):
            *   Change Blue (1) to Green (3).
            *   Change Magenta (6) to Gray (5).
    e.  **No Change**: If the pixel is not a candidate, or its border doesn't match the trigger color, or its color doesn't match a rule, its color in the output grid remains unchanged from the input grid.
5.  **Return Output Grid**: Return the completed output grid.
