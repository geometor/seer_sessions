# Dilate the object mask to find adjacent pixels
dilated_mask = ndimage.binary_dilation(obj_mask, structure=connectivity_structure)
# Identify pixels that are in the dilated mask but not in the original object mask
neighbor_pixels_mask = dilated_mask & ~obj_mask
# Get the colors of these neighboring pixels from the input grid
neighbor_colors = input_grid[neighbor_pixels_mask]
# Find the unique colors of neighboring objects (excluding background and self)
distinct_neighbor_colors = set(neighbor_colors)
distinct_neighbor_colors.discard(0)
distinct_neighbor_colors.discard(color) # <--- Potential issue here
neighbor_count = len(distinct_neighbor_colors)