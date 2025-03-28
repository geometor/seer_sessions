```python
import numpy as np
from collections import Counter

"""
Modifies a grid based on a unique 'trigger' pixel (Azure, Red, or Magenta) by applying color-specific propagation patterns and border modifications, including a conditional update to the row below the top border for Azure and Red triggers.

1.  **Identify Background Color:** Determine the most frequent pixel color in the input grid.
2.  **Identify Trigger Pixel:** Find the unique pixel `(trigger_r, trigger_c)` whose color `trigger_color` is one of Azure (8), Red (2), or Magenta (6), appears exactly once, and is not the background color. If no such pixel exists, return the original input grid.
3.  **Initialize Output Grid:** Create a copy of the input grid.
4.  **Apply Conditional Propagation:** Modify the output grid based on `trigger_color`:
    *   **If `trigger_color` is Azure (8) or Red (2):** Perform horizontal propagation. Move left and right from `(trigger_r, trigger_c)` in steps of 2, painting the pixel `(trigger_r, trigger_c +/- i)` with `trigger_color` if the intermediate pixel `(trigger_r, trigger_c +/- (i-1))` in the *input* grid is the background color. Stop propagation in a direction if out of bounds or the intermediate pixel is not the background color.
    *   **If `trigger_color` is Magenta (6):** Perform vertical (downward) propagation. Move down from `(trigger_r, trigger_c)` in steps of 2, painting the pixel `(trigger_r + i, trigger_c)` with `trigger_color` if the intermediate pixel `(trigger_r + i - 1, trigger_c)` in the *input* grid is the background color. Stop propagation if out of bounds or the intermediate pixel is not the background color.
5.  **Apply Border Modifications:** Modify the borders of the output grid based on `trigger_color`. Let H be height and W be width.
    *   **If `trigger_color` is Azure (8):**
        *   Set rightmost column (`output_grid[:, W-1]`) to Azure (8).
        *   Set top row (`output_grid[0, :]`) to Blue (1).
        *   Set top-right corner (`output_grid[0, W-1]`) to White (0).
        *   **Conditional Row 1 Update:** For each column `c`, if the pixel `input_grid[1, c]` was the background color AND Blue (1) exists anywhere in column `c` of the *input* grid (`input_grid[:, c]`), set `output_grid[1, c]` to Blue (1).
    *   **If `trigger_color` is Red (2):**
        *   Set leftmost column (`output_grid[:, 0]`) to Red (2).
        *   Set top row (`output_grid[0, :]`) to Green (3).
        *   Set top-left corner (`output_grid[0, 0]`) to White (0).
        *   **Conditional Row 1 Update:** For each column `c`, if the pixel `input_grid[1, c]` was the background color AND Green (3) exists anywhere in column `c` of the *input* grid (`input_grid[:, c]`), set `output_grid[1, c]` to Green (3).
    *   **If `trigger_color` is Magenta (6):**
        *   Set bottommost row (`output_grid[H-1, :]`) to Magenta (6).
6.  **Return Output:** Return the modified grid.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default to white for empty grid
    # If there's a tie for the most frequent color, the behavior might be undefined by the problem.
    # Let's assume Counter's behavior (returning one of the most frequent) is sufficient.
    return counts.most_common(1)[0][0]

def find_trigger_pixel_revised(grid, background_color):
    """
    Finds the color and location of the pixel that appears exactly once,
    is not the background color, and is one of {8, 2, 6}.
    Returns (trigger_color, trigger_r, trigger_c) or (None, None, None).
    """
    counts = Counter(grid.flatten())
    trigger_candidates = []
    trigger_colors_of_interest = {8, 2, 6} # Azure, Red, Magenta
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Check if color is potential trigger: correct color set, not background, unique count
            if color in trigger_colors_of_interest and \
               color != background_color and \
               counts[color] == 1:
                trigger_candidates.append({'color': color, 'pos': (r, c)})

    if len(trigger_candidates) == 1:
        trigger = trigger_candidates[0]
        return trigger['color'], trigger['pos'][0], trigger['pos'][1]
    else:
        # No unique trigger found matching criteria
        return None, None, None

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Identify Background Color
    background_color = find_background_color(input_grid_np)

    # 2. Identify Trigger Pixel
    trigger_color, trigger_r, trigger_c = find_trigger_pixel_revised(input_grid_np, background_color)

    # If no valid trigger found, return the original grid
    if trigger_color is None:
        # print("Debug: No valid trigger pixel found. Returning original grid.")
        return input_grid # Return original list of lists

    # 3. Initialize Output Grid
    output_grid = np.copy(input_grid_np)

    # 4. Apply Conditional Propagation
    if trigger_color == 8 or trigger_color == 2: # Azure or Red -> Horizontal
        # Rightward propagation
        # Iterate step size i = 2, 4, 6...
        for i in range(2, width * 2, 2):
            prop_c = trigger_c + i
            inter_c = trigger_c + i - 1
            # Check bounds for propagated and intermediate positions
            if 0 <= prop_c < width and 0 <= inter_c < width:
                # Check if intermediate pixel in *input* grid is background
                if input_grid_np[trigger_r, inter_c] == background_color:
                    output_grid[trigger_r, prop_c] = trigger_color
                else:
                    break # Stop rightward propagation if intermediate is blocked
            else:
                break # Stop rightward propagation if out of bounds

        # Leftward propagation
        # Iterate step size i = 2, 4, 6...
        for i in range(2, width * 2, 2):
            prop_c = trigger_c - i
            inter_c = trigger_c - i + 1
            # Check bounds for propagated and intermediate positions
            if 0 <= prop_c < width and 0 <= inter_c < width:
                 # Check if intermediate pixel in *input* grid is background
                 if input_grid_np[trigger_r, inter_c] == background_color:
                     output_grid[trigger_r, prop_c] = trigger_color
                 else:
                     break # Stop leftward propagation if intermediate is blocked
            else:
                 break # Stop leftward propagation if out of bounds

    elif trigger_color == 6: # Magenta -> Vertical (Downward)
        # Downward propagation
        # Iterate step size i = 2, 4, 6...
        for i in range(2, height * 2, 2):
             prop_r = trigger_r + i
             inter_r = trigger_r + i - 1
             # Check bounds for propagated and intermediate positions
             if 0 <= prop_r < height and 0 <= inter_r < height:
                 # Check if intermediate pixel in *input* grid is background
                 if input_grid_np[inter_r, trigger_c] == background_color:
                      output_grid[prop_r, trigger_c] = trigger_color
                 else:
                     break # Stop downward propagation if intermediate is blocked
             else:
                  break # Stop downward propagation if out of bounds

    # 5. Apply Border Modifications
    if trigger_color == 8: # Azure
        border_color = 1 # Top row becomes Blue
        # Set right column AFTER potential row 1 modifications affecting the last column
        # Set top row AFTER potential row 1 modifications affecting the top row (though unlikely)
        # Set top-right corner LAST to overwrite row/column changes

        # Conditional Row 1 Update (Check based on INPUT grid)
        if height > 1: # Only apply if row 1 exists
            for c in range(width):
                if input_grid_np[1, c] == background_color and border_color in input_grid_np[:, c]:
                    output_grid[1, c] = border_color

        # Apply basic border modifications
        output_grid[:, width - 1] = 8  # Rightmost column -> Azure (8)
        output_grid[0, :] = border_color  # Top row -> Blue (1)
        output_grid[0, width - 1] = 0  # Top-right corner -> White (0)

    elif trigger_color == 2: # Red
        border_color = 3 # Top row becomes Green
        # Set left column AFTER potential row 1 modifications affecting the first column
        # Set top row AFTER potential row 1 modifications affecting the top row
        # Set top-left corner LAST

        # Conditional Row 1 Update (Check based on INPUT grid)
        if height > 1: # Only apply if row 1 exists
            for c in range(width):
                if input_grid_np[1, c] == background_color and border_color in input_grid_np[:, c]:
                    output_grid[1, c] = border_color

        # Apply basic border modifications
        output_grid[:, 0] = 2  # Leftmost column -> Red (2)
        output_grid[0, :] = border_color  # Top row -> Green (3)
        output_grid[0, 0] = 0  # Top-left corner -> White (0)

    elif trigger_color == 6: # Magenta
        # No conditional update for adjacent row observed
        output_grid[height - 1, :] = 6 # Bottommost row -> Magenta (6)

    # 6. Return Output
    return output_grid.tolist() # Convert back to list of lists
```