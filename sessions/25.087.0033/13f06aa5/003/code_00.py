import numpy as np
from collections import Counter

"""
Modifies a grid based on a uniquely occurring 'trigger' pixel (Azure, Red, or Magenta) and applies color-specific propagation patterns and border modifications.

1.  **Identify Background Color:** Determine the most frequent pixel color in the input grid.
2.  **Identify Trigger Pixel:** Find the unique pixel `(r, c)` whose color `C` is *not* the background color, appears exactly once in the grid, and is one of Azure (8), Red (2), or Magenta (6). If no such pixel exists, return the input grid.
3.  **Initialize Output Grid:** Create a copy of the input grid.
4.  **Apply Conditional Propagation:**
    *   **If `C` is Azure (8) or Red (2):** Perform horizontal propagation from `(r, c)`.
        *   Move right: For steps `i = 2, 4, 6,...`, check column `c+i`. If `c+i` is in bounds and the pixel at `(r, c+i-1)` in the *input* grid is the background color, set the output pixel `(r, c+i)` to `C`. Stop moving right if the column is out of bounds or the intermediate pixel `(r, c+i-1)` is not background.
        *   Move left: For steps `i = 2, 4, 6,...`, check column `c-i`. If `c-i` is in bounds and the pixel at `(r, c-i+1)` in the *input* grid is the background color, set the output pixel `(r, c-i)` to `C`. Stop moving left if the column is out of bounds or the intermediate pixel `(r, c-i+1)` is not background.
    *   **If `C` is Magenta (6):** Perform vertical (downward) propagation from `(r, c)`.
        *   Move down: For steps `i = 2, 4, 6,...`, check row `r+i`. If `r+i` is in bounds and the pixel at `(r+i-1, c)` in the *input* grid is the background color, set the output pixel `(r+i, c)` to `C`. Stop moving down if the row is out of bounds or the intermediate pixel `(r+i-1, c)` is not background.
5.  **Apply Border Modifications based on `C`:**
    *   **If `C` is Azure (8):** Set the rightmost column to Azure (8), the top row to Blue (1), and the top-right corner pixel to White (0).
    *   **If `C` is Red (2):** Set the leftmost column to Red (2), the top row to Green (3), and the top-left corner pixel to White (0).
    *   **If `C` is Magenta (6):** Set the bottommost row to Magenta (6).
6.  **Return Output:** Return the modified grid.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default to white for empty grid
    return counts.most_common(1)[0][0]

def find_trigger_pixel_revised(grid, background_color):
    """
    Finds the color and location of the pixel that appears exactly once,
    is not the background color, and is one of {8, 2, 6}.
    """
    counts = Counter(grid.flatten())
    trigger_candidates = []
    trigger_colors_of_interest = {8, 2, 6} # Azure, Red, Magenta

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != background_color and counts[color] == 1 and color in trigger_colors_of_interest:
                trigger_candidates.append({'color': color, 'pos': (r, c)})

    if len(trigger_candidates) == 1:
        trigger = trigger_candidates[0]
        return trigger['color'], trigger['pos'][0], trigger['pos'][1]
    else:
        # Handle cases where 0 or >1 triggers are found matching the criteria
        # For this specific problem based on examples, we expect exactly one.
        # If not found, signal failure.
        return None, None, None

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Identify Background Color
    background_color = find_background_color(input_grid_np)

    # 2. Identify Trigger Pixel
    trigger_color, trigger_r, trigger_c = find_trigger_pixel_revised(input_grid_np, background_color)

    # If no valid trigger found, return the original grid
    if trigger_color is None:
        print("Warning: No valid trigger pixel (unique, non-bg, color 8/2/6) found.")
        return input_grid # Return original as per requirement

    # 3. Initialize Output Grid
    output_grid = np.copy(input_grid_np)

    # 4. Apply Conditional Propagation
    if trigger_color == 8 or trigger_color == 2: # Azure or Red -> Horizontal
        # Rightward propagation
        for i in range(2, width * 2, 2): # Iterate step size, ensure large enough range
            check_c = trigger_c + i
            intermediate_c = trigger_c + i - 1
            if 0 <= check_c < width and 0 <= intermediate_c < width:
                if input_grid_np[trigger_r, intermediate_c] == background_color:
                    # Check if the target pixel isn't already the trigger color (avoid unnecessary change)
                    # Although copy ensures start state, this is conceptually cleaner
                    if output_grid[trigger_r, check_c] != trigger_color:
                         output_grid[trigger_r, check_c] = trigger_color
                else:
                    break # Stop rightward propagation
            else:
                break # Stop if out of bounds

        # Leftward propagation
        for i in range(2, width * 2, 2): # Iterate step size
            check_c = trigger_c - i
            intermediate_c = trigger_c - i + 1
            if 0 <= check_c < width and 0 <= intermediate_c < width:
                 if input_grid_np[trigger_r, intermediate_c] == background_color:
                     if output_grid[trigger_r, check_c] != trigger_color:
                         output_grid[trigger_r, check_c] = trigger_color
                 else:
                     break # Stop leftward propagation
            else:
                 break # Stop if out of bounds

    elif trigger_color == 6: # Magenta -> Vertical (Downward)
        # Downward propagation
        for i in range(2, height * 2, 2): # Iterate step size
             check_r = trigger_r + i
             intermediate_r = trigger_r + i - 1
             if 0 <= check_r < height and 0 <= intermediate_r < height:
                 if input_grid_np[intermediate_r, trigger_c] == background_color:
                      if output_grid[check_r, trigger_c] != trigger_color:
                         output_grid[check_r, trigger_c] = trigger_color
                 else:
                     break # Stop downward propagation
             else:
                  break # Stop if out of bounds

    # 5. Apply Border Modifications
    if trigger_color == 8: # Azure
        # Set right column to Azure (8)
        output_grid[:, width - 1] = 8
        # Set top row to Blue (1)
        output_grid[0, :] = 1
        # Set top-right corner to White (0)
        output_grid[0, width - 1] = 0
    elif trigger_color == 2: # Red
        # Set left column to Red (2)
        output_grid[:, 0] = 2
        # Set top row to Green (3)
        output_grid[0, :] = 3
         # Set top-left corner to White (0)
        output_grid[0, 0] = 0
    elif trigger_color == 6: # Magenta
        # Set bottom row to Magenta (6)
        output_grid[height - 1, :] = 6

    # 6. Return Output
    return output_grid.tolist()