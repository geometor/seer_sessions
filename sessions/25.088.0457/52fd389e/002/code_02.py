                 # Check if the coordinate corresponds to an original yellow pixel or an internal pixel
                 original_color = input_grid_np[r,c]
                 if original_color == 4 or (r,c) in internal_coords:
                     output_grid_np[r, c] = 4 # Set to yellow