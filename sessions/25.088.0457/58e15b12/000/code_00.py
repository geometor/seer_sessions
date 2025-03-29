def simulate(grid):
    rows, cols = grid.shape
    max_row, max_col = rows - 1, cols - 1
    pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 8: # Azure
                pixels.append({'r': r, 'c': c, 'color': 8, 'dr': 1, 'dc': 1, 'active': True})
            elif grid[r, c] == 3: # Green
                pixels.append({'r': r, 'c': c, 'color': 3, 'dr': 1, 'dc': -1, 'active': True})

    output_grid = np.zeros_like(grid)
    
    # How many steps? Let's try a large number, maybe grid dimension related? max(rows, cols)?
    num_steps = max(rows, cols) 

    occupied_next = {} # Store {(r, c): [pixel_indices]} for collision detection

    # Draw initial positions? The examples seem to include the starting points in the trail.
    for i, p in enumerate(pixels):
         output_grid[p['r'], p['c']] = p['color'] # Assuming initial position is part of trail
         
         # Prep for first step collision check (is this needed? The rule might be collision happens *after* a move)
         # Let's assume collision check happens *before* drawing the pixel for the current step.

    for step in range(num_steps):
        occupied_now = {} # {(r, c): [pixel_indices]} for the current step
        
        # Calculate next positions and update occupied_now
        for i, p in enumerate(pixels):
            if not p['active']: continue
            
            next_r, next_c = p['r'] + p['dr'], p['c'] + p['dc']
            next_dr, next_dc = p['dr'], p['dc']

            # Bounce logic
            bounce = False
            if next_r < 0: next_r = 0; next_dr = 1; bounce = True
            if next_r > max_row: next_r = max_row; next_dr = -1; bounce = True
            if next_c < 0: next_c = 0; next_dc = 1; bounce = True
            if next_c > max_col: next_c = max_col; next_dc = -1; bounce = True
            
            # Store potential next position
            pos = (next_r, next_c)
            if pos not in occupied_now:
                occupied_now[pos] = []
            occupied_now[pos].append(i)
            
            # Update pixel state for next iteration (position will be updated after collision check)
            p['next_r'], p['next_c'] = next_r, next_c
            p['next_dr'], p['next_dc'] = next_dr, next_dc


        # Process collisions and update grid
        collision_processed_pixels = set()
        for pos, pixel_indices in occupied_now.items():
            if len(pixel_indices) > 1:
                # Collision detected at pos=(r, c)
                r, c = pos
                colors_involved = set(pixels[idx]['color'] for idx in pixel_indices)
                # If Azure (8) and Green (3) collide
                if 8 in colors_involved and 3 in colors_involved:
                    output_grid[r, c] = 6 # Magenta
                    # Deactivate colliding pixels? Or just mark collision?
                    # The trails seem to continue AFTER collision in some examples (e.g. train_2 has trails passing through where magenta forms)
                    # Let's assume they just place magenta and continue moving.
                    for idx in pixel_indices:
                        collision_processed_pixels.add(idx)
                # Handle other potential collisions? (e.g., two azure) - Assume they just overwrite/overlap based on order?
                # Or maybe only Azure-Green collision matters? Let's stick to that.
                # If it wasn't an Azure-Green collision, handle normally below.
                
        # Update positions and draw non-collided pixels
        for i, p in enumerate(pixels):
             if not p['active']: continue
             
             p['r'], p['c'] = p['next_r'], p['next_c']
             p['dr'], p['dc'] = p['next_dr'], p['next_dc']
             
             pos = (p['r'], p['c'])
             
             # If this pixel was part of an Azure-Green collision, it was already handled (magenta placed)
             if i in collision_processed_pixels and output_grid[pos] == 6:
                 continue 

             # Otherwise, draw the pixel color. If multiple non-colliding pixels land here, the last one wins?
             # Let's refine: only draw if the target cell is empty or magenta (to allow overdraw after collision)
             # OR draw if the target cell is the same color (overlap)
             # OR draw if target cell is different color but NOT magenta (overwrite? priority? let's assume overwrite is fine)
             
             # If the target cell is magenta from *this* step's collision, skip drawing original color.
             is_collision_spot = pos in occupied_now and len(occupied_now[pos]) > 1 and 8 in [pixels[idx]['color'] for idx in occupied_now[pos]] and 3 in [pixels[idx]['color'] for idx in occupied_now[pos]]

             if not is_collision_spot:
                 output_grid[p['r'], p['c']] = p['color']


        # Check if any pixels are still active? Maybe stop simulation early?
        # The number of steps needs confirmation. Try max(rows, cols) first.

    return output_grid