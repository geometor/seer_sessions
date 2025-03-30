```python
import numpy as np
from collections import Counter
from skimage.measure import label

"""
Transformation Rule:

1. Identify the background color (most frequent color, often bordering the grid).
2. Find all distinct contiguous objects that are not the background color.
3. Differentiate objects into:
    a. 'Main Regions': Large objects, predominantly composed of a single 'main_color'.
    b. 'Noise Shapes': Small, potentially multi-colored objects, separate from main regions.
4. Identify the 'marker_color': A color found both as isolated single pixels within main regions *and* as part of at least one noise shape.
5. Identify the 'target_color': The color found orthogonally adjacent to the 'marker_color' within the noise shape.
6. Identify the 'main_color': The dominant color of the main regions containing the isolated marker_color pixels.
7. Find the locations (row, column) of all marker_color pixels situated within the identified main regions.
8. Collect the unique row indices and column indices from these marker pixel locations.
9. Create an output grid, initially a copy of the input grid.
10. Iterate through the grid. For any pixel (r, c) where the input color is the 'main_color', if its row 'r' is in the collected marker rows OR its column 'c' is in the collected marker columns, change the color of that pixel in the output grid to the 'target_color'.
11. Identify all pixel coordinates belonging to the noise shape(s).
12. Replace the pixels corresponding to the noise shape(s) in the output grid with the background color.
13. Return the modified output grid.
"""

# Helper functions
def find_objects(grid, ignore_color=-1):
    """
    Finds connected components (objects) in the grid.
    Optionally ignores a specific color (e.g., background).
    Returns a labeled grid and a list of object properties.
    """
    mask = grid != ignore_color if ignore_color != -1 else np.ones_like(grid, dtype=bool)
    labeled_grid, num_labels = label(mask, connectivity=1, background=0, return_num=True) # Use connectivity=1 for orthogonal

    objects = []
    for i in range(1, num_labels + 1):
        coords = np.argwhere(labeled_grid == i)
        if coords.size > 0:
            colors = grid[coords[:, 0], coords[:, 1]]
            unique_colors, counts = np.unique(colors, return_counts=True)
            objects.append({
                'id': i,
                'coords': coords,
                'colors': dict(zip(unique_colors, counts)),
                'size': len(coords),
                'bounding_box': (coords.min(axis=0), coords.max(axis=0))
            })
    return labeled_grid, objects

def get_neighbors(grid, r, c, connectivity=1):
    """Gets neighbor coordinates and colors."""
    neighbors = []
    rows, cols = grid.shape
    coords = []
    # Orthogonal neighbors (connectivity=1)
    if r > 0: coords.append((r - 1, c))
    if r < rows - 1: coords.append((r + 1, c))
    if c > 0: coords.append((r, c - 1))
    if c < cols - 1: coords.append((r, c + 1))
    # Diagonal neighbors (connectivity=2)
    if connectivity == 2:
        if r > 0 and c > 0: coords.append((r - 1, c - 1))
        if r > 0 and c < cols - 1: coords.append((r - 1, c + 1))
        if r < rows - 1 and c > 0: coords.append((r + 1, c - 1))
        if r < rows - 1 and c < cols - 1: coords.append((r + 1, c + 1))

    for nr, nc in coords:
        neighbors.append({'coord': (nr, nc), 'color': grid[nr, nc]})
    return neighbors

def get_most_frequent_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # Handle cases where the background might not be the absolute most frequent
    # if multiple large areas exist. Check corners/borders if needed, but
    # simple frequency often works for ARC.
    if not counts:
        return 0 # Default if grid is empty
    return counts.most_common(1)[0][0]

def transform(input_grid):
    """
    Applies the transformation rule based on marker pixels within main regions
    and color relationships derived from separate noise shapes.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 1. Identify background color
    background_color = get_most_frequent_color(grid)

    # 2. Find all non-background objects
    labeled_grid, objects = find_objects(grid, ignore_color=background_color)

    if not objects:
        return output_grid # No objects to process

    # 3. Differentiate Main Regions and Noise Shapes
    # Heuristic: Main regions are significantly larger than noise shapes.
    # We might need a more robust way, but size difference is often key in ARC.
    sizes = [obj['size'] for obj in objects]
    if not sizes:
        return output_grid

    # Use a threshold - e.g., objects smaller than 1/10th of the largest might be noise
    # Or simply assume the smallest few are noise if there's a clear size gap.
    # Let's sort by size and try to find a marker/target relationship in the smaller ones.
    objects.sort(key=lambda x: x['size'])

    potential_noise_shapes = []
    potential_main_regions = []
    # Simple split: smallest objects are potential noise, largest are potential main
    # This might need adjustment based on task specifics. Assume at least one noise, one main.
    # A better approach might involve checking color complexity too.
    size_threshold = np.mean(sizes) # A possible heuristic
    if len(objects) > 1:
         for obj in objects:
             # Noise shapes are small, main regions large. Use size comparison.
             # Also check if object contains multiple colors, often true for noise
             is_complex = len(obj['colors']) > 1
             # A more robust check might be needed, maybe comparing against largest object size
             if obj['size'] < size_threshold / 2 and is_complex : # Arbitrary threshold factor
                 potential_noise_shapes.append(obj)
             else:
                 potential_main_regions.append(obj)
    else: # Only one object found besides background
        potential_main_regions = objects # Treat it as the main region

    if not potential_main_regions: # If all objects classified as noise, maybe the threshold was wrong
         potential_main_regions = objects # Revert
         potential_noise_shapes = [] # Assume no noise shape if logic fails

    # 4, 5, 6. Identify marker, target, and main colors
    marker_color = -1
    target_color = -1
    main_color = -1
    noise_shape_coords = []
    marker_pixel_locations = [] # Store (r, c) tuples

    # Find potential marker pixels (isolated pixels within potential main regions)
    potential_markers = {} # {color: [(r, c), ...]}
    for region in potential_main_regions:
        region_coords_set = set(tuple(c) for c in region['coords'])
        # Find the dominant color in this region
        dominant_color_in_region = max(region['colors'], key=region['colors'].get)

        for r, c in region['coords']:
            pixel_color = grid[r, c]
            if pixel_color != dominant_color_in_region:
                 # Check if it's truly isolated within this region's dominant color
                 is_isolated = True
                 neighbor_colors = []
                 for neighbor in get_neighbors(grid, r, c, connectivity=1):
                     nc_r, nc_c = neighbor['coord']
                     n_color = neighbor['color']
                     neighbor_colors.append(n_color)
                     # Check if neighbor is part of the *same* large region
                     # This is tricky without re-labeling or complex checks.
                     # Simplification: Check if neighbours are mostly the dominant color
                 if all(nc == dominant_color_in_region or nc == pixel_color for nc in neighbor_colors) and any(nc == dominant_color_in_region for nc in neighbor_colors) :
                      if pixel_color not in potential_markers:
                          potential_markers[pixel_color] = []
                      potential_markers[pixel_color].append(((r, c), dominant_color_in_region))


    # Now check potential noise shapes for marker/target pairs
    found_match = False
    for noise_shape in potential_noise_shapes:
        noise_colors = set(noise_shape['colors'].keys())
        for pm_color, locations_and_main in potential_markers.items():
            if pm_color in noise_colors:
                # Found potential marker color. Look for adjacent target color in noise shape.
                for r_noise, c_noise in noise_shape['coords']:
                    if grid[r_noise, c_noise] == pm_color:
                        for neighbor in get_neighbors(grid, r_noise, c_noise, connectivity=1):
                            n_color = neighbor['color']
                            # Ensure neighbor is part of the same noise object
                            n_coord = neighbor['coord']
                            is_neighbor_in_noise = False
                            for c in noise_shape['coords']:
                                if tuple(c) == n_coord:
                                    is_neighbor_in_noise = True
                                    break
                            
                            if is_neighbor_in_noise and n_color != pm_color and n_color != background_color:
                                # Found potential target color adjacent to marker in noise
                                marker_color = pm_color
                                target_color = n_color
                                # Assume the main color associated with the first found marker location
                                main_color = locations_and_main[0][1]
                                marker_pixel_locations = [loc[0] for loc in locations_and_main] # Get just the (r, c) tuples
                                noise_shape_coords = noise_shape['coords']
                                found_match = True
                                break # Found target color
                    if found_match: break
            if found_match: break
        if found_match: break

    # If no match found via noise shape, the logic might be different or failed.
    # Fallback or error handling could be added here. For now, proceed if found.
    if not found_match:
        # Maybe there's no noise shape, or the identification failed.
        # Try a simpler rule if only markers and main regions are found?
        # For this problem, the noise shape seems essential.
        print("Warning: Could not reliably identify marker/target/main colors using noise shape.")
        # Attempt to guess based on most frequent non-background in main regions and isolated pixels
        if potential_markers and potential_main_regions:
             marker_color = list(potential_markers.keys())[0] # Guess first potential marker
             main_color = potential_markers[marker_color][0][1] # Associated main color
             marker_pixel_locations = [loc[0] for loc in potential_markers[marker_color]]
             # Cannot determine target color without noise shape reliably
             print("Cannot determine target color. Returning intermediate state.")
             # Might return output_grid without painting step or raise error
             return output_grid # Or handle differently


    # 7. Collect marker rows and columns
    marker_rows = set()
    marker_cols = set()
    for r, c in marker_pixel_locations:
        marker_rows.add(r)
        marker_cols.add(c)

    # 8. Apply transformation (Paint rows/columns)
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is in a marked row or column AND is the main color
            if (r in marker_rows or c in marker_cols) and grid[r, c] == main_color:
                output_grid[r, c] = target_color

    # 9. Remove Noise Shape
    if len(noise_shape_coords) > 0:
        for r, c in noise_shape_coords:
            output_grid[r, c] = background_color

    # Note: The original marker pixels should remain unchanged if the painting
    # logic correctly only targets 'main_color' pixels. Double check needed if
    # marker_color == main_color, but examples suggest they are different.

    return output_grid.tolist() # Convert back to list of lists if needed

```