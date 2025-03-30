# 5. & 6. Iterate through the Stamps Area bounding box and transfer patterns
for r in range(min_r_stamp, max_r_stamp + 1):
    for c in range(min_c_stamp, max_c_stamp + 1):
        # Check if the pixel is within the original grid bounds
        if 0 <= r < rows and 0 <= c < cols:
             input_color = grid[r, c]
             # Check if it's a non-white pixel AND truly part of the stamps (not canvas)
             is_stamp_pixel = (
                 input_color != 0 and
                 not (canvas_r <= r < canvas_r + canvas_h and canvas_c <= c < canvas_c + canvas_w)
             )

             if is_stamp_pixel:
                # Calculate relative position within the stamp bounding box
                rel_r = r - min_r_stamp # <<<<<<< RELATIVE TO STAMP BOX TOP-LEFT
                rel_c = c - min_c_stamp # <<<<<<< RELATIVE TO STAMP BOX TOP-LEFT

                # Check if relative position is within the output grid bounds
                if 0 <= rel_r < output_grid.shape[0] and 0 <= rel_c < output_grid.shape[1]:
                    # Set the output pixel to azure (8)
                    output_grid[rel_r, rel_c] = 8 # <<<<<<<<< PLACED AT (rel_r, rel_c) IN OUTPUT