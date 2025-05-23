# ... (previous setup) ...
min_r, max_r, min_c, max_c = get_bounding_box(largest_object_coords)
print(f"Slicing rows: {min_r} to {max_r+1}")
print(f"Slicing cols: {min_c} to {max_c+1}")
cropped_grid = [row[min_c : max_c + 1] for row in input_grid[min_r : max_r + 1]]
# ... (rest of comparison) ...