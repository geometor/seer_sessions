                 # Check if the coordinate corresponds to an original yellow pixel
                 original_color = input_grid_np[r,c]
                 if original_color == 4:
                     output_grid_np[r, c] = 4 # Set ONLY original yellow pixels to yellow