        # Draw the border
        for r in range(exp_min_r, exp_max_r + 1):
            for c in range(exp_min_c, exp_max_c + 1):
                # Check if the pixel is outside the original bounding box
                is_outside = (r < min_r or r > max_r or c < min_c or c > max_c)
                if is_outside:
                     output_grid_np[r, c] = inner_color