
Previous Code:
```python
import numpy as np

"""
Transforms an input grid by iteratively propagating specific colors (Red=2, Yellow=4, Azure=8) downwards onto background cells (White=0, Blue=1).

The propagation follows these rules:
1.  The process iterates until no changes occur in a full pass over the grid.
2.  Propagation only occurs into cells that were originally background (White or Blue) in the input grid AND are currently background in the grid being updated.
3.  Green (3) pixels are static and block propagation; they are never overwritten.
4.  Red (2) pixels attempt to propagate straight down (r+1, c). If blocked or invalid, they attempt to propagate down-left (r+1, c-1).
5.  Yellow (4) pixels attempt to propagate straight down (r+1, c). If blocked or invalid, they attempt to propagate down-right (r+1, c+1).
6.  Azure (8) pixels attempt to propagate *both* down-left (r+1, c-1) and down-right (r+1, c+1) independently in each step.
7.  Changes within one iteration step are based on the grid state at the *start* of that step and are applied simultaneously before the next iteration begins.
"""

def transform(input_grid):
    """
    Applies the iterative color propagation rules to the input grid.

    Args:
        input_grid: A list of lists representing the initial grid state.

    Returns:
        A list of lists representing the final grid state after propagation stops.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = input_np.copy()
    height, width = input_np.shape
    
    # Define background and mobile colors
    background_colors = {0, 1} # white, blue
    mobile_colors = {2, 4, 8} # red, yellow, azure

    # Loop until no more changes occur in a full iteration
    while True:
        changed = False
        # Create a grid for the next state based on the current state.
        # This prevents changes within one iteration from immediately affecting
        # subsequent checks in the same iteration.
        next_output_grid = output_grid.copy()

        # --- Helper function to check propagation validity ---
        # Checks bounds, original background status, and current background status in the next_grid
        def is_valid_target(nr, nc):
            # Check bounds
            if not (0 <= nr < height and 0 <= nc < width):
                return False
            # Check if the target was originally background in the input
            if input_np[nr, nc] not in background_colors:
                return False
            # Check if the target in the *next* state grid is currently background
            # (meaning it hasn't been claimed by another propagation in this iteration)
            if next_output_grid[nr, nc] not in background_colors:
                return False
            return True

        # Iterate row by row, from top to bottom
        # We check pixels in row 'r' to potentially modify row 'r+1'
        for r in range(height - 1): # Last row cannot propagate downwards
            for c in range(width):
                # Get the color from the *current* state grid
                current_color = output_grid[r, c]

                # --- Propagation Logic ---
                if current_color == 2: # Red
                    propagated_down = False
                    # Try down
                    target_r, target_c = r + 1, c
                    if is_valid_target(target_r, target_c):
                        # Check if the target isn't already Red to avoid redundant changes flag
                        if next_output_grid[target_r, target_c] != 2:
                           next_output_grid[target_r, target_c] = 2
                           changed = True
                        propagated_down = True # Mark attempt down successful even if already red
                    
                    # If down attempt failed (blocked/invalid OR already red), try down-left
                    # Note: The original logic was "If down failed" -> try diag.
                    # Let's refine: Try down first. If that specific target cell is invalid, try diagonal.
                    # If the target cell *was* valid but already contained the color, we don't try diagonal.
                    
                    # More accurate: Try down. If target is invalid, try down-left.
                    target_r_down, target_c_down = r + 1, c
                    is_down_valid = is_valid_target(target_r_down, target_c_down)

                    if is_down_valid:
                        if next_output_grid[target_r_down, target_c_down] != 2:
                            next_output_grid[target_r_down, target_c_down] = 2
                            changed = True
                    else: # Down target was invalid, try down-left
                        target_r_dl, target_c_dl = r + 1, c - 1
                        if is_valid_target(target_r_dl, target_c_dl):
                           if next_output_grid[target_r_dl, target_c_dl] != 2:
                                next_output_grid[target_r_dl, target_c_dl] = 2
                                changed = True


                elif current_color == 4: # Yellow
                    # Try down. If target is invalid, try down-right.
                    target_r_down, target_c_down = r + 1, c
                    is_down_valid = is_valid_target(target_r_down, target_c_down)

                    if is_down_valid:
                        if next_output_grid[target_r_down, target_c_down] != 4:
                            next_output_grid[target_r_down, target_c_down] = 4
                            changed = True
                    else: # Down target was invalid, try down-right
                        target_r_dr, target_c_dr = r + 1, c + 1
                        if is_valid_target(target_r_dr, target_c_dr):
                            if next_output_grid[target_r_dr, target_c_dr] != 4:
                                next_output_grid[target_r_dr, target_c_dr] = 4
                                changed = True

                elif current_color == 8: # Azure
                    # Propagates both ways *if possible*, independently.
                    # Try down-left
                    target_r_left, target_c_left = r + 1, c - 1
                    if is_valid_target(target_r_left, target_c_left):
                        if next_output_grid[target_r_left, target_c_left] != 8:
                            next_output_grid[target_r_left, target_c_left] = 8
                            changed = True
                    # Try down-right
                    target_r_right, target_c_right = r + 1, c + 1
                    if is_valid_target(target_r_right, target_c_right):
                        if next_output_grid[target_r_right, target_c_right] != 8:
                            next_output_grid[target_r_right, target_c_right] = 8
                            changed = True

        # Update the main grid for the next iteration
        # Check if the grid actually changed to avoid infinite loops if logic is flawed
        if np.array_equal(output_grid, next_output_grid):
           #print("No change detected, breaking loop.")
           break
           
        output_grid = next_output_grid

        # If no changes were flagged in this full pass, the simulation is stable
        # The np.array_equal check above is a more robust break condition
        # if not changed:
        #    print("Changed flag is False, breaking loop.")
        #    break

    # Return the final state as a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 8 0 1 0 1 0 1
1 0 1 0 1 0 3 0 8 0 1 0 1 0
0 1 0 1 0 3 0 3 0 8 0 1 0 1
1 0 1 0 3 0 1 0 3 0 1 0 1 0
0 1 0 8 0 3 0 3 0 1 0 1 0 1
1 0 1 0 8 0 3 0 1 0 1 0 1 0
0 1 0 1 0 8 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
```
Expected Output:
```
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 8
1 0 1 0 1 0 1 0 1 0 1 0 8 0
0 1 0 1 0 1 0 1 0 1 0 8 0 1
1 0 1 0 1 0 1 0 1 0 8 0 1 0
0 1 0 1 0 1 0 1 0 8 0 1 0 8
1 0 1 0 1 0 1 0 8 0 1 0 8 0
0 1 0 1 0 1 0 8 0 1 0 8 0 1
1 0 1 0 1 0 3 0 8 0 8 0 1 0
0 1 0 1 0 3 0 3 0 8 0 1 0 1
1 0 1 0 3 0 1 0 3 0 1 0 1 0
0 1 0 8 0 3 0 3 0 1 0 1 0 1
1 0 8 0 8 0 3 0 1 0 1 0 1 0
0 8 0 1 0 8 0 1 0 1 0 1 0 1
8 0 1 0 8 0 1 0 1 0 1 0 1 0
0 1 0 8 0 1 0 1 0 1 0 1 0 1
1 0 8 0 1 0 1 0 1 0 1 0 1 0
0 8 0 1 0 1 0 1 0 1 0 1 0 1
8 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
```
Transformed Output:
```
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 8 0 1 0 1 0 1
1 0 1 0 1 0 3 0 8 0 1 0 1 0
0 1 0 1 0 3 0 3 0 8 0 1 0 1
1 0 1 0 3 0 1 0 3 0 8 0 1 0
0 1 0 8 0 3 0 3 0 8 0 8 0 1
1 0 8 0 8 0 3 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8
8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8
8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8
8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8
```
Match: False
Pixels Off: 57
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 40.71428571428572

## Example 2:
Input:
```
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 2 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 2 0 3 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 2 0 3 0 3 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 3 0 1 0 3 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 4 0 3 0 3 0 2 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 4 0 3 0 2 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 4 0 2 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
```
Expected Output:
```
1 0 2 0 1 0 2 0 1 0 1 0 1 0 4 0 1 0 4 0 1 0 1 0 1 0 1 0 1 0
0 1 0 2 0 1 0 2 0 1 0 1 0 4 0 1 0 4 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 2 0 1 0 2 0 1 0 4 0 1 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 2 0 1 0 2 0 4 0 1 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 2 0 2 0 3 0 4 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 2 0 3 0 3 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 3 0 1 0 3 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 4 0 3 0 3 0 2 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 4 0 4 0 3 0 2 0 2 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 4 0 1 0 4 0 2 0 1 0 2 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 4 0 1 0 4 0 1 0 2 0 1 0 2 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 4 0 1 0 4 0 1 0 1 0 2 0 1 0 2 0 1 0 1 0 1 0 1 0 1 0 1
1 0 4 0 1 0 4 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0 1 0 1 0 1 0 1 0
0 4 0 1 0 4 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0 1 0 1 0 1 0 1
4 0 1 0 4 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0 1 0 1 0 1 0
0 1 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0 1 0 1 0 1
1 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0 1 0 1 0
0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0 1 0 1
4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 2 0 1 0 2
```
Transformed Output:
```
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 1 0 2 0 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 1 0 2 2 3 4 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 1 0 2 2 3 0 3 4 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 1 0 2 2 3 0 1 0 3 4 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 1 0 2 2 4 0 3 0 3 0 2 4 4 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 0 1 0 2 2 2 4 4 0 3 0 2 2 4 4 4 0 1 0 1 0 1 0 1 0 1 0 1 0
0 1 0 2 2 2 2 4 4 4 0 2 2 2 4 4 4 4 0 1 0 1 0 1 0 1 0 1 0 1
1 0 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 0 1 0 1 0 1 0 1 0 1 0
0 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 0 1 0 1 0 1 0 1 0 1
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 0 1 0 1 0 1 0 1 0
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 0 1 0 1 0 1 0 1
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 0 1 0 1 0 1 0
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 0 1 0 1 0 1
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 0 1 0 1 0
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 0 1 0 1
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 0 1 0
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 1
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
2 2 2 2 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 395
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 109.72222222222221
