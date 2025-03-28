```python
import numpy as np
from collections import Counter

"""
The transformation identifies significant geometric shapes in the input grid, generates a 6x6 representation for each shape, sorts these representations based on the shape's original position, and stacks them vertically to form the output grid.

1.  **Analyze Input:**
    *   Determine the `background_color`: Find the most frequent color in the input grid, excluding gray (color 5). Gray acts as noise.
    *   Define `noise_color` = 5.
    *   Define `significant_threshold` = 4 (components must have > 4 pixels).
    *   Define `pattern_size` = 6.

2.  **Pad Input:** Create a padded version of the input grid by adding a border of `background_color` pixels. The padding width should be at least `pattern_size - 1` (e.g., 6) to ensure any 6x6 extraction starting from an original grid coordinate is valid within the padded grid.

3.  **Find Significant Components:**
    *   Identify all connected components (using 8-way adjacency) in the *original* input grid for any color that is *not* the `background_color` and *not* the `noise_color`.
    *   Filter these components, keeping only the "significant components" whose size (pixel count) is greater than `significant_threshold`.

4.  **Generate and Clean Patterns:**
    *   For each significant component found:
        *   Determine its `primary_color`.
        *   Find its top-left bounding box coordinate `(min_r, min_c)` relative to the *original* grid.
        *   Extract a `pattern_size` x `pattern_size` (6x6) subgrid (the `raw_pattern`) from the *padded* grid. The extraction starts at the coordinate corresponding to `(min_r, min_c)` in the original grid (i.e., `padded_grid[min_r + pad_width : min_r + pad_width + 6, min_c + pad_width : min_c + pad_width + 6]`).
        *   Create a new `pattern_size` x `pattern_size` "cleaned pattern" grid, initialized with the `background_color`.
        *   Copy pixels from the `raw_pattern` to the `cleaned_pattern` *only* if the pixel's color in the `raw_pattern` matches either the `primary_color` or the `background_color`. All other pixels in the `cleaned_pattern` remain `background_color`.
        *   Store this `cleaned_pattern` along with its origin coordinate `(min_r, min_c)`.

5.  **Sort Patterns:** Arrange the generated `cleaned_patterns` in order based on their corresponding `(min_r, min_c)` coordinates, sorting primarily by row (`min_r`) and secondarily by column (`min_c`).

6.  **Combine Patterns:** Vertically stack the sorted `cleaned_patterns` to produce the final output grid. If no significant components were found, the output is an empty grid with 0 rows and `pattern_size` columns.
"""

import numpy as np
from collections import Counter

# --- Helper Functions ---

def find_background_color(grid):
    """
    Finds the most frequent color in the grid, ignoring gray (5) unless it's 
    the only significant color present besides potentially black/white (0).
    """
    colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(colors, counts))
    noise_color = 5

    potential_bg_colors = {c: count for c, count in color_counts.items() if c != noise_color}

    if not potential_bg_colors:
        if noise_color in color_counts:
            return noise_color
        else: 
            return 0 # Default for empty or all-zero grid
            
    background_color = max(potential_bg_colors, key=potential_bg_colors.get)
    return background_color

def find_components(grid, colors_to_find):
    """
    Finds all connected components for a set of target colors using 8-way adjacency.
    Returns a list of dicts: {'color': color, 'pixels': list_of_tuples, 'size': int}.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    all_components = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in colors_to_find and not visited[r, c]:
                component_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    component_pixels.append((row, col))
                    
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = row + dr, col + dc
                            
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if component_pixels: 
                    all_components.append({
                        'color': color, 
                        'pixels': component_pixels, 
                        'size': len(component_pixels)
                    })
                    
    return all_components

def get_bounding_box_top_left(component_pixels):
    """Calculates the top-left coordinate (min_row, min_col) for a component."""
    if not component_pixels:
        return 0, 0 
    rows = [p[0] for p in component_pixels]
    cols = [p[1] for p in component_pixels]
    min_row = min(rows)
    min_col = min(cols)
    return min_row, min_col

def clean_pattern(raw_pattern, primary_color, background_color):
    """
    Creates a cleaned 6x6 pattern. Keeps only the primary color and background 
    color pixels from the raw_pattern. All others become background color.
    """
    cleaned = np.full_like(raw_pattern, background_color)
    rows, cols = raw_pattern.shape
    for r in range(rows):
        for c in range(cols):
            pixel_color = raw_pattern[r, c]
            if pixel_color == primary_color or pixel_color == background_color:
                cleaned[r, c] = pixel_color
    return cleaned

# --- Main Transform Function ---

def transform(input_grid):
    """
    Transforms the input grid based on extracting, cleaning, sorting, and 
    stacking 6x6 patterns from significant components, using padding to handle
    boundary conditions.
    """
    input_grid = np.array(input_grid)
    if input_grid.size == 0:
         return np.empty((0, 6), dtype=int).tolist() # Handle empty input

    rows, cols = input_grid.shape
    noise_color = 5
    significant_threshold = 4 
    pattern_size = 6
    padding_width = pattern_size # Use padding width = pattern_size for safety

    # 1. Identify Background color
    background_color = find_background_color(input_grid)

    # 2. Pad Input Grid
    padded_grid = np.pad(
        input_grid, 
        pad_width=padding_width, 
        mode='constant', 
        constant_values=background_color
    )

    # 3. Find Significant Components in the original grid
    present_colors = np.unique(input_grid)
    component_colors_to_find = {
        c for c in present_colors if c != background_color and c != noise_color
    }
    all_found_components = find_components(input_grid, component_colors_to_find)

    # 4. Generate and Clean Patterns
    pattern_data = [] # List to store ((min_r, min_c), cleaned_pattern)
    
    for comp_info in all_found_components:
        # Check if component is significant
        if comp_info['size'] > significant_threshold:
            primary_color = comp_info['color']
            component_pixels = comp_info['pixels']
            
            # Get top-left coordinate relative to original grid
            min_r, min_c = get_bounding_box_top_left(component_pixels)
            coord = (min_r, min_c)

            # Extract the raw 6x6 pattern area from the padded grid
            # Adjust coordinates for padding
            padded_r_start = min_r + padding_width
            padded_c_start = min_c + padding_width
            raw_pattern = padded_grid[
                padded_r_start : padded_r_start + pattern_size,
                padded_c_start : padded_c_start + pattern_size
            ]
            
            # Ensure raw_pattern is exactly 6x6 (should be due to padding)
            if raw_pattern.shape == (pattern_size, pattern_size):
                 # Create the cleaned pattern
                 cleaned = clean_pattern(raw_pattern, primary_color, background_color)
                 
                 # Store the original coordinate and the cleaned pattern
                 pattern_data.append((coord, cleaned))
            # else: handle potential edge cases if padding wasn't sufficient (unlikely with pad_width=6)
                 # print(f"Warning: extracted pattern size mismatch for coord {coord}. Shape: {raw_pattern.shape}")


    # 5. Sort patterns based on coordinates (row, then column)
    pattern_data.sort(key=lambda item: item[0])

    # 6. Assemble Output: Vertically stack the sorted patterns
    if not pattern_data:
        # If no significant components were found, return empty 0x6 grid
        output_grid = np.empty((0, pattern_size), dtype=int)
    else:
        # Extract just the cleaned patterns in sorted order
        sorted_patterns = [item[1] for item in pattern_data]
        # Stack them vertically
        output_grid = np.vstack(sorted_patterns)

    # Convert back to list of lists for ARC standard output format
    return output_grid.tolist()
```