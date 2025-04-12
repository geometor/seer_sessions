import numpy as np
import math
from collections import deque, Counter

"""
Transforms the input grid by:
1. Identifying the unique 'noisy' shape (a connected component containing 
   multiple colors, using 4-directional connectivity).
2. Determining the 'border' color (most frequent color within the noisy shape, 
   using max color value as tie-breaker).
3. Extracting the 'noise' pixels (those differing from the border color) into 
   a minimal bounding box grid ('noise_grid').
4. Calculating a scaling factor based on the noisy shape's bounding box width: 
   Scale = Width - 1.
5. Determining the output grid dimensions by scaling the 'noise_grid' 
   dimensions by the 'Scale' factor.
6. Rendering the output grid: Each output pixel (r_out, c_out) takes the color 
   of the noise grid pixel at (r_out // Scale, c_out // Scale), effectively 
   scaling up each noise pixel into a block.
"""

# --- Helper Functions ---

def _find_noisy_component_details(grid: np.ndarray):
    """
    Finds the single noisy component, extracts its noise grid, and determines 
    the component width needed for scaling.

    A component is a 4-directionally connected group of non-zero cells.
    A component is noisy if it contains more than one distinct color.
    The 'border color' is the most frequent color (max color tie-breaker).
    'Noise pixels' are cells in the noisy component whose color is not the 
    border color.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        tuple: (noise_grid, H_noise, W_noise, W_comp)
               - noise_grid: NumPy array of the noise pattern.
               - H_noise: Height of the noise grid.
               - W_noise: Width of the noise grid.
               - W_comp: Width of the noisy component's bounding box.
        Returns (None, None, None, None) if no noisy component is found or 
        if a valid noise pattern cannot be extracted.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    noisy_component_found = None # Store details of the noisy component when found

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

                    # Update component bounding box
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
                
                # Check if this component is the noisy one
                if len(colors_in_component) > 1:
                    # Found the noisy component (assuming only one exists per task)
                    noisy_component_found = {
                        'cells': component_cells,
                        'min_r': min_r_comp, 'max_r': max_r_comp,
                        'min_c': min_c_comp, 'max_c': max_c_comp
                    }
                    break # Exit inner loop once found
            # If found in inner loop, exit outer loop too
            if noisy_component_found:
                break

    # If no noisy component was identified after checking all cells
    if not noisy_component_found:
        return None, None, None, None 

    # Calculate component width from its bounding box
    W_comp = noisy_component_found['max_c'] - noisy_component_found['min_c'] + 1

    # Determine border color (most frequent, tie-break with max color value)
    color_counts = Counter(noisy_component_found['cells'].values())
    # Check if counter is valid (should be if noisy_component_found is set)
    if not color_counts: 
        return None, None, None, None 
    border_color = max(color_counts, key=lambda k: (color_counts[k], k))

    # Extract noise pixels (those not matching border color) into a dict with absolute coordinates
    noise_pixels_abs = {}
    for (r_n, c_n), color in noisy_component_found['cells'].items():
        if color != border_color:
            noise_pixels_abs[(r_n, c_n)] = color

    # If no noise pixels were found (e.g., if all non-border colors were filtered out somehow)
    if not noise_pixels_abs:
        return None, None, None, None

    # Determine noise bounding box from the absolute coordinates of noise pixels
    noise_coords = list(noise_pixels_abs.keys())
    min_r_noise = min(r for r, c in noise_coords)
    max_r_noise = max(r for r, c in noise_coords)
    min_c_noise = min(c for r, c in noise_coords)
    max_c_noise = max(c for r, c in noise_coords)

    # Calculate noise grid dimensions
    H_noise = max_r_noise - min_r_noise + 1
    W_noise = max_c_noise - min_c_noise + 1

    # Create the relative noise grid (initialized to 0)
    noise_grid = np.zeros((H_noise, W_noise), dtype=int)
    # Populate the noise grid using relative coordinates
    for (r_abs, c_abs), color in noise_pixels_abs.items():
        noise_grid[r_abs - min_r_noise, c_abs - min_c_noise] = color

    # Return the noise grid and its dimensions, plus the component width
    return noise_grid, H_noise, W_noise, W_comp


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation logic to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)

    # Step 1-4: Find noisy component, determine border color, extract noise grid, get component width
    noise_grid, H_noise, W_noise, W_comp = _find_noisy_component_details(input_array)

    # Handle case where no valid noisy component or noise pattern was found
    if noise_grid is None:
        # Return empty list as per common ARC error handling for unapplicable rules
        return [] 

    # Step 5a: Calculate Scale factor
    Scale = W_comp - 1
    
    # Validate scale factor (must be positive)
    if Scale <= 0:
        # If component width is 1 or less, scale is invalid. Return empty.
        return [] 

    # Step 5b: Calculate Output Grid Size
    H_out = H_noise * Scale
    W_out = W_noise * Scale

    # Step 6: Render Output Grid using direct mapping (upscaling)
    output_grid = np.zeros((H_out, W_out), dtype=int)

    # Iterate through each pixel coordinate (r_out, c_out) of the output grid
    for r_out in range(H_out):
        for c_out in range(W_out):
            # Determine the corresponding source pixel coordinates in the noise_grid
            # using integer division (floor division)
            nr = r_out // Scale 
            nc = c_out // Scale
            
            # Assign the color from the source noise pixel to the output pixel
            # Boundary check is implicitly handled because 0 <= r_out < H_out and 0 <= c_out < W_out
            # guarantees 0 <= nr < H_noise and 0 <= nc < W_noise
            output_grid[r_out, c_out] = noise_grid[nr, nc]

    # Step 7: Return the completed output grid as a list of lists
    return output_grid.tolist()
