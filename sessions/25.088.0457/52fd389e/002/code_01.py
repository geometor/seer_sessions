    # Pass 2: Ensure original yellow pixels within the bbox are yellow in the output,
    # and preserve the original internal pixels colors if they haven't been overwritten by borders.
    for obj in objects_to_process:
        min_r, min_c, max_r, max_c = obj['bbox']
        internal_coords = obj['internal_coords']

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                 # Check if the current coordinate is within the original bounding box
                 coord = (r, c)
                 original_color = input_grid_np[r, c]

                 # If the pixel was originally yellow, ensure it's yellow in the output
                 if original_color == 4:
                     output_grid_np[r, c] = 4
                 # If the pixel was one of the designated 'internal' pixels for this object,
                 # ensure it retains its original color in the output, *unless* it was already
                 # overwritten by a border in Pass 1.
                 # The current state `output_grid_np[r, c]` reflects Pass 1 changes.
                 # If `output_grid_np[r, c]` is still the same as `original_color`, it wasn't
                 # overwritten by a border. We only need to explicitly handle the case where
                 # the border drawing (Pass 1) might have overwritten an internal pixel, which
                 # shouldn't happen given the border is drawn *outside* the original bbox.
                 # A simpler logic: If it was originally yellow, set to yellow. If it was an internal pixel,
                 # leave it as whatever color it currently is (either original or overwritten by border).
                 # We only need to explicitly set the yellow pixels.
                 # The initial copy `output_grid_np = np.array(input_grid, dtype=int)` handles preserving
                 # internal colors initially. Pass 1 draws borders. Pass 2 just needs to ensure the
                 # original yellow area becomes yellow.

                 # Revised Pass 2 Logic:
                 # Only touch pixels that were originally yellow within the bbox.
                 if original_color == 4:
                     output_grid_np[r, c] = 4