```python
import numpy as np
from scipy.spatial.distance import cdist
from skimage.measure import label, regionprops

"""
Identify non-white (0), non-magenta (6) "marker" pixels and their locations/colors.
Identify contiguous shapes made of magenta (6) pixels ("template shapes").
Associate each marker pixel with the spatially closest template shape (minimum distance from marker to any pixel of the shape).
For each marker-template pair:
  Extract the template shape within its minimal bounding box.
  Create a new grid of the bounding box size.
  Fill this new grid: where the template shape had magenta (6), place the marker's color; otherwise, place white (0).
Determine arrangement:
  Calculate the row and column range spanned by marker pixels.
  If column range > row range, arrange horizontally, sorted by marker column.
  Otherwise, arrange vertically, sorted by marker row.
Combine the colored shapes according to the determined arrangement and sorting order to create the final output grid.
"""

def find_marker_pixels(grid):
    """Finds pixels that are not white (0) or magenta (6)."""
    markers = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != 0 and color != 6:
                markers.append({'pos': (r, c), 'color': color})
    return markers

def find_shapes(grid, color):
    """Finds contiguous shapes of a specific color."""
    binary_grid = (grid == color).astype(int)
    labeled_grid, num_labels = label(binary_grid, connectivity=1, background=0, return_num=True) # Use connectivity=1 for 4-way adjacency
    
    shapes = []
    if num_labels > 0:
        regions = regionprops(labeled_grid)
        for region in regions:
            coords = region.coords # Gives list of (row, col) tuples
            # Convert coords to list of tuples for consistency
            coords_list = [tuple(coord) for coord in coords]
            shapes.append({'coords': coords_list, 'label': region.label})
            
    # Filter out potential empty shapes if any issue with regionprops
    shapes = [s for s in shapes if s['coords']] 
    return shapes


def get_bounding_box(coords):
    """Calculates the minimum bounding box for a set of coordinates."""
    if not coords:
        return None, None, None, None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return min_r, min_c, height, width

def distance_marker_to_shape(marker_pos, shape_coords):
    """Calculates the minimum Manhattan distance from a marker point to any pixel in a shape."""
    marker_np = np.array([marker_pos])
    shape_np = np.array(shape_coords)
    # Use cdist with 'cityblock' for Manhattan distance
    distances = cdist(marker_np, shape_np, metric='cityblock')
    return np.min(distances)

def extract_and_recolor(grid, shape_coords, marker_color):
    """Extracts shape within bounding box and recolors magenta to marker color."""
    if not shape_coords:
        return None
        
    min_r, min_c, height, width = get_bounding_box(shape_coords)
    
    # Create the output subgrid, initialized to white (0)
    subgrid = np.zeros((height, width), dtype=np.uint8)
    
    # Convert shape_coords to a set for faster lookup
    shape_coords_set = set(shape_coords)

    # Iterate through the bounding box in the original grid coordinates
    for r in range(min_r, min_r + height):
        for c in range(min_c, min_c + width):
            # Check if the current coordinate belongs to the shape
            if (r, c) in shape_coords_set:
                 # Check if the original pixel was magenta (redundant if shape_coords only contains magenta pixels)
                 # if grid[r, c] == 6: # This check might be unnecessary if find_shapes is correct
                 subgrid[r - min_r, c - min_c] = marker_color
                 # Else case is handled by initialization to 0 (white)

    return subgrid

def combine_grids(grids, orientation):
    """Combines multiple grids horizontally or vertically, padding with 0s."""
    if not grids:
        return np.array([[]], dtype=np.uint8) # Return empty if no grids

    if orientation == 'horizontal':
        max_height = max(g.shape[0] for g in grids)
        padded_grids = []
        for g in grids:
            pad_height = max_height - g.shape[0]
            # Pad at the bottom
            padded_g = np.pad(g, ((0, pad_height), (0, 0)), mode='constant', constant_values=0)
            padded_grids.append(padded_g)
        return np.hstack(padded_grids)
    else: # vertical
        max_width = max(g.shape[1] for g in grids)
        padded_grids = []
        for g in grids:
            pad_width = max_width - g.shape[1]
            # Pad on the right
            padded_g = np.pad(g, ((0, 0), (0, pad_width)), mode='constant', constant_values=0)
            padded_grids.append(padded_g)
        return np.vstack(padded_grids)

def transform(input_grid):
    """
    Transforms the input grid by finding marker pixels and magenta template shapes,
    associating them by proximity, extracting and recoloring the shapes based on markers,
    and arranging the resulting shapes based on marker positions.
    """
    input_grid_np = np.array(input_grid, dtype=np.uint8)

    # 1. Find marker pixels
    markers = find_marker_pixels(input_grid_np)
    if not markers:
        # Handle case with no markers if necessary, maybe return empty or input?
        # Assuming task guarantees markers.
        return np.array([[]], dtype=np.uint8)


    # 2. Find template shapes (magenta color = 6)
    template_shapes = find_shapes(input_grid_np, 6)
    if not template_shapes:
         # Handle case with no template shapes if necessary.
        return np.array([[]], dtype=np.uint8)

    # 3. Associate each marker with the closest template shape
    associations = []
    used_shape_labels = set() # Keep track of shapes already assigned

    # Calculate all distances first to handle potential multiple markers closest to the same shape
    marker_shape_distances = []
    for i, marker in enumerate(markers):
        for j, shape in enumerate(template_shapes):
            dist = distance_marker_to_shape(marker['pos'], shape['coords'])
            marker_shape_distances.append({'marker_idx': i, 'shape_idx': j, 'dist': dist})
            
    # Sort distances to prioritize closest pairs
    marker_shape_distances.sort(key=lambda x: x['dist'])

    marker_assigned = [False] * len(markers)
    shape_assigned = [False] * len(template_shapes)
    
    processed_pairs = []

    for M_S_dist in marker_shape_distances:
        marker_idx = M_S_dist['marker_idx']
        shape_idx = M_S_dist['shape_idx']
        
        # If this marker and shape haven't been assigned yet, make the assignment
        if not marker_assigned[marker_idx] and not shape_assigned[shape_idx]:
            marker = markers[marker_idx]
            shape = template_shapes[shape_idx]
            processed_pairs.append({
                'marker': marker,
                'shape_coords': shape['coords']
            })
            marker_assigned[marker_idx] = True
            shape_assigned[shape_idx] = True
            
        # Stop if all markers have been assigned
        if all(marker_assigned):
            break

    # Ensure we found an association for every marker
    if len(processed_pairs) != len(markers):
        # This might indicate an issue with the association logic or input data mismatch
        print(f"Warning: Could not associate all {len(markers)} markers. Found {len(processed_pairs)} associations.")
        # Depending on requirements, could raise an error or return empty/partial grid
        # Let's proceed with the associations found for now.

    # 4. Process each pair: Extract and recolor
    output_shapes_data = []
    for pair in processed_pairs:
        marker = pair['marker']
        shape_coords = pair['shape_coords']
        recolored_shape = extract_and_recolor(input_grid_np, shape_coords, marker['color'])
        if recolored_shape is not None:
            output_shapes_data.append({
                'shape': recolored_shape,
                'marker_pos': marker['pos']
            })

    if not output_shapes_data:
         return np.array([[]], dtype=np.uint8)

    # 5. Determine arrangement strategy
    marker_rows = [data['marker_pos'][0] for data in output_shapes_data]
    marker_cols = [data['marker_pos'][1] for data in output_shapes_data]

    row_range = max(marker_rows) - min(marker_rows) if len(marker_rows) > 1 else 0
    col_range = max(marker_cols) - min(marker_cols) if len(marker_cols) > 1 else 0

    if col_range > row_range:
        orientation = 'horizontal'
        # Sort by marker column index
        output_shapes_data.sort(key=lambda x: x['marker_pos'][1])
    else:
        orientation = 'vertical'
        # Sort by marker row index
        output_shapes_data.sort(key=lambda x: x['marker_pos'][0])

    # 6. Assemble the output grid
    final_shapes = [data['shape'] for data in output_shapes_data]
    output_grid = combine_grids(final_shapes, orientation)

    # 7. Return the result
    return output_grid.tolist() # Convert back to list of lists if required by ARC env
```