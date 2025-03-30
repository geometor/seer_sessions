    # Pass 2: Fill the original rectangle areas with yellow, overwriting internal colors
    for obj in objects_to_process:
        min_r, min_c, max_r, max_c = obj['bbox']
        internal_coords = obj['internal_coords']

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                 # Check if the coordinate corresponds to an original yellow pixel or an internal pixel
                 original_color = input_grid_np[r,c]
                 if original_color == 4 or (r,c) in internal_coords:
                     output_grid_np[r, c] = 4 # Set to yellow