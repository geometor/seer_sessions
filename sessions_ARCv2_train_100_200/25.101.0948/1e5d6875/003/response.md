```python
import copy

"""
Transforms the input grid based on identified L-shapes of gray (5) or red (2) pixels.

1.  Identify L-Shapes: Find all 2x2 squares containing exactly three pixels of the same color (gray 5 or red 2) and one background pixel (orange 7).
2.  For each L-shape, determine:
    - its color (gray or red).
    - the coordinates of its corner pixel `C = (cr, cc)` (the shape pixel diagonally opposite the background pixel).
    - the parity of `C` (odd/even for `cr` and `cc`).
    - the coordinates of the missing background pixel `MP = (mr, mc)`.
    - the relative position of MP to C: `relative_MP = (mr-cr, mc-cc)`.
3.  Process Gray L-Shapes (color 5):
    - If `relative_MP` is `(-1,-1)` or `(-1,+1)` (MP is "above" C):
        - Secondary color is Green (3) if `C_parity` is (odd, odd), else Yellow (4).
        - Add Yellow (4) at `MP+(-1,0)` and `MP`.
        - Add the secondary color at `MP+(0,+1)` and `MP+(+1,+1)`.
    - If `relative_MP` is `(+1,-1)` or `(+1,+1)` (MP is "below" C):
        - Add Yellow (4) at `MP+(-1,-1)`, `MP+(0,-1)`, `MP`, and `MP+(+1,0)`.
4.  Process Red L-Shapes (color 2):
    - Based on `C_parity` (0=even, 1=odd) and `relative_MP`:
        - If `C_parity`=(1, 1) and `relative_MP`=(-1,-1): Add Green (3) at `C+(0,+1)`.
        - If `C_parity`=(0, 0) and `relative_MP`=(-1,+1): Add Green (3) at `C+(+1,0)`.
        - If `C_parity`=(1, 0) and `relative_MP`=(+1,-1): Add Green (3) at `C+(-1,0)`, `C+(-1,+1)`, and `C+(0,+1)`.
        - If `C_parity`=(0, 1) and `relative_MP`=(-1,+1): Add Green (3) at `C+(0,-1)`, `C+(+1,-1)`, and `C+(+1,0)`.
5.  Add pixels only if the target cell is within grid bounds and contains the background color (7).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies transformations based on identified Gray and Red L-shapes.
    """
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Define colors
    background_color = 7
    gray = 5
    red = 2
    yellow = 4
    green = 3

    def is_valid(r, c):
        """Check if coordinates are within grid bounds."""
        return 0 <= r < height and 0 <= c < width

    def add_pixel(grid, r, c, color):
        """Safely add a pixel if the location is valid and is background."""
        if is_valid(r, c) and grid[r][c] == background_color:
            grid[r][c] = color

    # Iterate through all possible top-left corners of 2x2 squares
    for r in range(height - 1):
        for c in range(width - 1):
            # Coordinates of the 2x2 square
            coords = [(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)]
            # Colors in the 2x2 square
            colors = [input_grid[rr][cc] for rr, cc in coords]

            # Count background and non-background pixels
            non_bg_colors = [color for color in colors if color != background_color]
            bg_coords = [coords[i] for i in range(4) if colors[i] == background_color]

            # Check for exactly 3 identical non-background pixels (gray or red) and 1 background pixel
            if len(non_bg_colors) == 3 and len(bg_coords) == 1 and len(set(non_bg_colors)) == 1:
                shape_color = non_bg_colors[0]
                if shape_color not in [gray, red]:
                    continue # Skip if not gray or red

                # Identify MP (Missing Pixel) coordinates
                mr, mc = bg_coords[0]

                # Identify C (Corner) coordinates (diagonally opposite MP)
                cr, cc = -1, -1 # Initialize C coordinates
                if (mr, mc) == (r, c): cr, cc = (r + 1, c + 1)
                elif (mr, mc) == (r + 1, c): cr, cc = (r, c + 1)
                elif (mr, mc) == (r, c + 1): cr, cc = (r + 1, c)
                elif (mr, mc) == (r + 1, c + 1): cr, cc = (r, c)

                # Calculate relative MP position and C parity
                relative_mp = (mr - cr, mc - cc)
                c_parity = (cr % 2, cc % 2) # (0=even, 1=odd)

                # --- Process Gray L-Shapes ---
                if shape_color == gray:
                    if relative_mp[0] == -1: # MP is "above" C: relative_mp is (-1,-1) or (-1,+1)
                        secondary_color = green if c_parity == (1, 1) else yellow # Green if C is odd,odd
                        add_pixel(output_grid, mr - 1, mc, yellow)       # MP+(-1,0)
                        add_pixel(output_grid, mr, mc, yellow)           # MP
                        add_pixel(output_grid, mr, mc + 1, secondary_color) # MP+(0,+1)
                        add_pixel(output_grid, mr + 1, mc + 1, secondary_color) # MP+(+1,+1)
                    
                    elif relative_mp[0] == 1: # MP is "below" C: relative_mp is (+1,-1) or (+1,+1)
                        add_pixel(output_grid, mr - 1, mc - 1, yellow)  # MP+(-1,-1)
                        add_pixel(output_grid, mr, mc - 1, yellow)      # MP+(0,-1)
                        add_pixel(output_grid, mr, mc, yellow)          # MP
                        add_pixel(output_grid, mr + 1, mc, yellow)      # MP+(+1,0)

                # --- Process Red L-Shapes ---
                elif shape_color == red:
                    # Check specific combinations of C_parity and relative_MP based on analysis
                    if c_parity == (1, 1) and relative_mp == (-1, -1): # odd,odd and MP top-left
                        add_pixel(output_grid, cr, cc + 1, green)       # C+(0,+1)
                    
                    elif c_parity == (0, 0) and relative_mp == (-1, +1): # even,even and MP top-right
                        add_pixel(output_grid, cr + 1, cc, green)       # C+(+1,0)
                    
                    elif c_parity == (1, 0) and relative_mp == (+1, -1): # odd,even and MP bottom-left
                        # Add G L-shape opening Bottom-Left, corner C+(-1,+1)
                        add_pixel(output_grid, cr - 1, cc, green)       # C+(-1,0)
                        add_pixel(output_grid, cr - 1, cc + 1, green)   # C+(-1,+1)
                        add_pixel(output_grid, cr, cc + 1, green)       # C+(0,+1)
                        
                    elif c_parity == (0, 1) and relative_mp == (-1, +1): # even,odd and MP top-right
                        # Add G L-shape opening Top-Right, corner C+(+1,-1)
                        add_pixel(output_grid, cr, cc - 1, green)       # C+(0,-1)
                        add_pixel(output_grid, cr + 1, cc - 1, green)   # C+(+1,-1)
                        add_pixel(output_grid, cr + 1, cc, green)       # C+(+1,0)
                    
                    # No action defined for other combinations based on examples

    return output_grid
```