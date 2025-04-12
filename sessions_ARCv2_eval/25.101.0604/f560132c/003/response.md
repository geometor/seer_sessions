```python
import numpy as np
import math
from collections import deque, Counter

"""
Transforms the input grid by identifying a unique 'noisy' shape (a connected 
component containing multiple colors), extracting the 'noise' pixels (those 
differing from the shape's most frequent 'border' color) into a minimal 
'noise_grid', determining a scaling factor based on the noisy shape's 
bounding box width (Scale = Width - 1), scaling the 'noise_grid' dimensions 
by this factor to get the output size, and then rendering the output grid. 
Each output pixel's color is the maximum color value among the four noise 
grid cells corresponding to the corners surrounding the output pixel's scaled 
location in the noise grid space (treating out-of-bounds lookups as 0).
"""

# --- Helper Functions ---

def _get_val_safe(grid: np.ndarray, r: int, c: int) -> int:
    """
    Safely gets a value from a grid using integer indices, returning 0 for 
    out-of-bounds coordinates.
    """
    H, W = grid.shape
    if 0 <= r < H and 0 <= c < W:
        return int(grid[r, c])
    return 0

def _find_noisy_component_details(grid: np.ndarray):
    """
    Finds the single noisy component, extracts its noise grid, and determines 
    the component width needed for scaling.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        tuple: (noise_grid, H_noise, W_noise, W_comp)
               - noise_grid: NumPy array of the noise pattern.
               - H_noise: Height of the noise grid.
               - W_noise: Width of the noise grid.
               - W_comp: Width of the noisy component's bounding box.
        Returns (None, None, None, None) if no noisy component is found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    noisy_component_found = None

    for r_start in range(rows):
        for c_start in range(cols):
            if grid[r_start, c_start] != 0 and not visited[r_start, c_start]:
                component_cells = {}  # {(r, c): color}
                q = deque([(r_start, c_start)])
                processed_in_component = set([(r_start, c_start)])
                
                start_color = grid[r_start, c_start]
                component_cells[(r_start, c_start)] = start_color
                colors_in_component = {start_color}
                visited[r_start, c_start] = True

                min_r_comp, max_r_comp = r_start, r_start
                min_c_comp, max_c_comp = c_start, c_start

                # BFS to find component extent and colors
                while q:
                    row, col = q.popleft()

                    min_r_comp = min(min_r_comp, row)
                    max_r_comp = max(max_r_comp, row)
                    min_c_comp = min(min_c_comp, col)
                    max_c_comp = max(max_c_comp, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and (nr, nc) not in processed_in_component:
                            
                            visited[nr, nc] = True
                            processed_in_component.add((nr, nc))
                            q.append((nr, nc))

                            cell_color = grid[nr, nc]
                            component_cells[(nr, nc)] = cell_color
                            colors_in_component.add(cell_color)
                
                # Check if this component is noisy
                if len(colors_in_component) > 1:
                    # Found the noisy component (assuming only one exists)
                    noisy_component_found = {
                        'cells': component_cells,
                        'min_r': min_r_comp, 'max_r': max_r_comp,
                        'min_c': min_c_comp, 'max_c': max_c_comp
                    }
                    break # Stop searching once the noisy component is found
            if noisy_component_found:
                break # Stop outer loop as well

    if not noisy_component_found:
        return None, None, None, None # Indicate failure

    # Calculate component width
    W_comp = noisy_component_found['max_c'] - noisy_component_found['min_c'] + 1

    # Determine border color (most frequent, tie-break with max color value)
    color_counts = Counter(noisy_component_found['cells'].values())
    if not color_counts: # Should not happen if noisy_component_found is set
        return None, None, None, None 
    border_color = max(color_counts, key=lambda k: (color_counts[k], k))

    # Extract noise pixels (absolute coordinates)
    noise_pixels_abs = {}
    for (r_n, c_n), color in noisy_component_found['cells'].items():
        if color != border_color:
            noise_pixels_abs[(r_n, c_n)] = color

    if not noise_pixels_abs:
         # This case might occur if multiple colors exist but only one is non-border
         # Or if the most frequent color calculation had unexpected behaviour.
         # Depending on exact problem constraints, might need different handling.
         # For now, treat as failure if no distinct noise pixels found.
        return None, None, None, None

    # Determine noise bounding box
    noise_coords = list(noise_pixels_abs.keys())
    min_r_noise = min(r for r, c in noise_coords)
    max_r_noise = max(r for r, c in noise_coords)
    min_c_noise = min(c for r, c in noise_coords)
    max_c_noise = max(c for r, c in noise_coords)

    H_noise = max_r_noise - min_r_noise + 1
    W_noise = max_c_noise - min_c_noise + 1

    # Create relative noise grid
    noise_grid = np.zeros((H_noise, W_noise), dtype=int)
    for (r_abs, c_abs), color in noise_pixels_abs.items():
        noise_grid[r_abs - min_r_noise, c_abs - min_c_noise] = color

    return noise_grid, H_noise, W_noise, W_comp


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation pipeline to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)

    # Step 1-4: Find noisy component, determine border color, extract noise grid, get component width
    noise_grid, H_noise, W_noise, W_comp = _find_noisy_component_details(input_array)

    if noise_grid is None:
        # Handle case where no noisy component or valid noise pattern was found
        # Based on ARC tasks, often implies returning an empty grid or raising error
        # Returning empty grid for now.
        # raise ValueError("Could not find a valid noisy component or noise pattern.")
        return [] # Or potentially handle based on specific problem context if needed

    # Step 5a: Calculate Scale
    Scale = W_comp - 1
    if Scale <= 0:
        # Scale must be positive. If W_comp is 1, this fails.
        # Again, handle based on assumptions/problem constraints.
        # raise ValueError(f"Invalid calculated scale ({Scale}) from component width {W_comp}.")
        return [] # Return empty for now

    # Step 5b: Calculate Output Size
    H_out = H_noise * Scale
    W_out = W_noise * Scale

    # Step 6: Render Output Grid
    output_grid = np.zeros((H_out, W_out), dtype=int)

    for r_out in range(H_out):
        for c_out in range(W_out):
            # Map output pixel to fractional coordinates in noise grid space
            r_f = r_out / Scale
            c_f = c_out / Scale

            # Identify the four reference points (integer coords) in noise grid
            # Note: using int() conversion after floor/ceil for _get_val_safe
            nr_tl = math.floor(r_f)
            nc_tl = math.floor(c_f)
            nr_tr = math.floor(r_f)
            nc_tr = math.ceil(c_f)
            nr_bl = math.ceil(r_f)
            nc_bl = math.floor(c_f)
            nr_br = math.ceil(r_f)
            nc_br = math.ceil(c_f)

            # Get values safely from noise grid (0 if out-of-bounds)
            val_tl = _get_val_safe(noise_grid, int(nr_tl), int(nc_tl))
            val_tr = _get_val_safe(noise_grid, int(nr_tr), int(nc_tr))
            val_bl = _get_val_safe(noise_grid, int(nr_bl), int(nc_bl))
            val_br = _get_val_safe(noise_grid, int(nr_br), int(nc_br))

            # Assign the maximum value to the output pixel
            output_grid[r_out, c_out] = max(val_tl, val_tr, val_bl, val_br)

    # Step 7: Return Output as list of lists
    return output_grid.tolist()
```