import numpy as np
import math
from collections import deque

"""
Transforms the input grid according to the following process:
1. Identify the unique 'noisy' shape (a connected component containing multiple colors).
   The 'border' color is the most frequent color in the component.
2. Extract the 'noise' pixels (those differing from the shape's border color)
   into a minimal bounding box grid ('noise_grid').
3. Determine the scale factor by calculating the width of the bounding box
   of the entire noisy component found in step 1.
4. Determine the output grid size by scaling the noise_grid dimensions by the scale factor.
5. Render the output grid: For each output pixel (r_out, c_out), map it to fractional
   coordinates (r_f, c_f) in the noise_grid space. Find the maximum color value among
   the four noise grid cells whose coordinates are derived using floor and ceil
   of (r_f, c_f): (floor(r_f), floor(c_f)), (floor(r_f), ceil(c_f)),
   (ceil(r_f), floor(c_f)), (ceil(r_f), ceil(c_f)). Out-of-bounds lookups return 0.
"""


# --- Helper Functions ---

def _get_val_safe(grid: np.ndarray, r: float, c: float) -> int:
    """
    Safely gets a value from a grid using integer indices derived from r, c,
    returning 0 for out-of-bounds. r and c are expected to be results from
    math.floor or math.ceil.
    """
    # Convert float results from floor/ceil to integer indices
    r_idx = int(r)
    c_idx = int(c)
    H, W = grid.shape
    # Check if the integer indices are within the grid bounds
    if 0 <= r_idx < H and 0 <= c_idx < W:
        # Return the value as a standard Python integer
        return int(grid[r_idx, c_idx])
    # Return 0 if indices are out of bounds
    return 0

def _find_noise_grid_and_scale(grid: np.ndarray):
    """
    Finds the single noisy component in the grid, extracts its noise pixels
    into a minimal bounding box grid, and determines the scaling factor based
    on the width of the noisy component's bounding box.

    A component is a 4-directionally connected group of non-zero cells.
    A component is noisy if it contains more than one distinct color.
    The 'border color' is the most frequent color within the noisy component.
    'Noise pixels' are cells in the noisy component whose color is not the border color.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        tuple: (noise_grid, scale) where noise_grid is a NumPy array containing
               the noise pixels relative to their bounding box, and scale is an
               integer calculated as the width of the noisy component's bounding box.
        Returns (None, None) if no noisy component is found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool) # Tracks visited cells globally across component searches

    # Iterate through each cell to find potential starting points for components
    for r_start in range(rows):
        for c_start in range(cols):
            # Start BFS if cell is non-zero and hasn't been visited yet
            if grid[r_start, c_start] != 0 and not visited[r_start, c_start]:
                component_cells = {}  # Stores {(r, c): color} for the current component
                q = deque([(r_start, c_start)]) # Queue for BFS
                processed_in_component = set([(r_start, c_start)]) # Track cells processed in *this* component search

                # Store initial cell info
                start_color = grid[r_start, c_start]
                component_cells[(r_start, c_start)] = start_color
                colors_in_component = {start_color} # Set of unique colors in component
                visited[r_start, c_start] = True # Mark globally visited

                # Initialize component bounding box coordinates
                min_r_comp, max_r_comp = r_start, r_start
                min_c_comp, max_c_comp = c_start, c_start

                # --- Perform BFS to find all connected non-zero cells ---
                while q:
                    row, col = q.popleft()

                    # Update component bounding box as we explore
                    min_r_comp = min(min_r_comp, row)
                    max_r_comp = max(max_r_comp, row)
                    min_c_comp = min(min_c_comp, col)
                    max_c_comp = max(max_c_comp, col)

                    # Explore 4 orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check neighbor validity: within bounds, non-zero, and not already processed for this component
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and (nr, nc) not in processed_in_component:

                            visited[nr, nc] = True # Mark globally visited
                            processed_in_component.add((nr, nc)) # Mark processed for this specific component BFS
                            q.append((nr, nc)) # Add to queue for further exploration

                            # Store neighbor cell info
                            cell_color = grid[nr, nc]
                            component_cells[(nr, nc)] = cell_color
                            colors_in_component.add(cell_color)
                # --- Component fully explored ---

                # Analyze if it's the noisy component (contains more than one color)
                if len(colors_in_component) > 1:
                    # Assumption: Only one such component exists per problem statement.
                    
                    # Safety check: Ensure component_cells is not empty
                    if not component_cells: continue 

                    # --- Identify Border Color ---
                    # Find the most frequent color (border color)
                    color_counts = {}
                    for color in component_cells.values():
                        color_counts[color] = color_counts.get(color, 0) + 1
                    
                    if not color_counts: continue # Safety check

                    # Determine border color (handle ties by taking max count, then max color value for determinism)
                    border_color = max(color_counts, key=lambda k: (color_counts[k], k))

                    # --- Extract Noise Pixels ---
                    # Noise pixels have absolute coordinates initially
                    noise_pixels_abs = {}
                    for (r_n, c_n), color in component_cells.items():
                        if color != border_color:
                            noise_pixels_abs[(r_n, c_n)] = color

                    # Proceed only if noise pixels were actually found
                    if noise_pixels_abs:
                        # --- Determine Scale ---
                        # Hypothesis: Scale is the width of the component's bounding box
                        W_comp = max_c_comp - min_c_comp + 1
                        scale = W_comp # Scaling factor

                        # Basic validation for calculated scale
                        if scale <= 0:
                             raise ValueError(f"Calculated non-positive scale: {scale}")

                        # --- Create the Relative Noise Grid ---
                        noise_coords = list(noise_pixels_abs.keys())
                        # Find bounding box of noise pixels
                        min_r_noise = min(r for r, c in noise_coords)
                        max_r_noise = max(r for r, c in noise_coords)
                        min_c_noise = min(c for r, c in noise_coords)
                        max_c_noise = max(c for r, c in noise_coords)
                        
                        # Calculate noise grid dimensions
                        H_noise = max_r_noise - min_r_noise + 1
                        W_noise = max_c_noise - min_c_noise + 1
                        
                        # Basic validation for noise grid dimensions
                        if H_noise <= 0 or W_noise <= 0:
                            raise ValueError(f"Calculated non-positive noise grid dimensions: H={H_noise}, W={W_noise}")

                        # Initialize relative noise grid
                        noise_grid_rel = np.zeros((H_noise, W_noise), dtype=int)
                        # Populate relative noise grid
                        for (r_abs, c_abs), color in noise_pixels_abs.items():
                            # Map absolute noise coordinates to relative coordinates within the noise grid
                            noise_grid_rel[r_abs - min_r_noise, c_abs - min_c_noise] = color

                        # Return the extracted noise grid and the calculated scale factor
                        return noise_grid_rel, scale

    # If the loops complete without finding and returning a noisy component
    return None, None


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation pipeline: find noisy component, extract noise grid,
    determine scale from component width, upscale noise grid using max-of-4-neighbors rule.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.

    Raises:
        ValueError: If no noisy component is found, or if calculated scale or
                    noise grid dimensions are invalid.
    """
    input_array = np.array(input_grid, dtype=int)

    # Step 1, 2, 3: Find the noise grid and the scaling factor
    noise_grid, scale = _find_noise_grid_and_scale(input_array)

    # Validate results from the helper function
    if noise_grid is None:
        raise ValueError("No noisy component found in the input grid.")
    # Scale is already validated in the helper, but check again just in case
    if scale is None or scale <= 0:
        raise ValueError(f"Invalid scale determined: {scale}")
    # Ensure noise grid is not empty
    if noise_grid.size == 0:
         raise ValueError("Empty noise grid extracted.")

    H_noise, W_noise = noise_grid.shape

    # Step 4: Determine Output Grid Size based on noise grid dimensions and scale
    H_out = H_noise * scale
    W_out = W_noise * scale

    # Step 5: Render the Output Grid
    output_grid = np.zeros((H_out, W_out), dtype=int)

    # Iterate through each pixel coordinate (r_out, c_out) of the output grid
    for r_out in range(H_out):
        for c_out in range(W_out):
            # Map output pixel coordinates to fractional coordinates (r_f, c_f) in the noise_grid space
            # These represent the top-left corner of the corresponding area in the noise grid
            r_f = r_out / scale
            c_f = c_out / scale

            # Identify the four reference points in the noise grid using floor/ceil of the fractional coordinates
            # These correspond to the grid points surrounding the mapped location (r_f, c_f)
            nr_tl = math.floor(r_f) # Top-left row index
            nc_tl = math.floor(c_f) # Top-left col index
            nr_tr = math.floor(r_f) # Top-right row index (same as tl)
            nc_tr = math.ceil(c_f)  # Top-right col index
            nr_bl = math.ceil(r_f)  # Bottom-left row index
            nc_bl = math.floor(c_f) # Bottom-left col index (same as tl)
            nr_br = math.ceil(r_f)  # Bottom-right row index (same as bl)
            nc_br = math.ceil(c_f)  # Bottom-right col index (same as tr)

            # Get values from the noise grid for these four reference points
            # _get_val_safe handles out-of-bounds checks by returning 0
            val_tl = _get_val_safe(noise_grid, nr_tl, nc_tl)
            val_tr = _get_val_safe(noise_grid, nr_tr, nc_tr)
            val_bl = _get_val_safe(noise_grid, nr_bl, nc_bl)
            val_br = _get_val_safe(noise_grid, nr_br, nc_br)

            # Assign the maximum of these four values to the current output grid pixel
            output_grid[r_out, c_out] = max(val_tl, val_tr, val_bl, val_br)

    # Convert the final NumPy array output grid back to a list of lists for the required return format
    return output_grid.tolist()