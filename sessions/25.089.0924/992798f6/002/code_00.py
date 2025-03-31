def get_line_coords_bresenham(r1, c1, r2, c2):
    coords = []
    dr = r2 - r1
    dc = c2 - c1
    sr = 1 if dr > 0 else -1
    sc = 1 if dc > 0 else -1
    dr = abs(dr)
    dc = abs(dc)
    
    r, c = r1, c1 # Start point

    if dc > dr: # Slope < 1 (more horizontal)
        err = 2 * dr - dc
        for _ in range(dc): # Need dc steps to reach target column
            c += sc # Move horizontally
            if err >= 0: # Threshold to move vertically
                r += sr
                err -= 2 * dc
            err += 2 * dr
            coords.append((r, c)) # Add the point *after* the move
    else: # Slope >= 1 (more vertical)
        err = 2 * dc - dr
        for _ in range(dr): # Need dr steps to reach target row
            r += sr # Move vertically
            if err >= 0: # Threshold to move horizontally
                c += sc
                err -= 2 * dr
            err += 2 * dc
            coords.append((r, c)) # Add the point *after* the move
            
    # The loop generates points *between* start and end.
    # Check if the last point generated is indeed the end point's neighbor
    # This implementation generates points starting from the neighbor of (r1, c1)
    # up to and including (r2, c2).
    
    # Let's rethink. The previous manual trace generated points *including* start and end.
    # Let's align the implementation with that trace.

    coords_trace = [] # Store points including start and end
    
    r_curr, c_curr = r1, c1
    coords_trace.append((r_curr, c_curr)) # Add start point
    
    if dc > dr: # Slope < 1
        err = 2 * dr - dc
        while c_curr != c2:
            c_curr += sc
            if err >= 0:
                r_curr += sr
                err -= 2 * dc
            err += 2 * dr
            coords_trace.append((r_curr, c_curr))
    else: # Slope >= 1
        err = 2 * dc - dr
        while r_curr != r2:
            r_curr += sr
            if err >= 0:
                c_curr += sc
                err -= 2 * dr
            err += 2 * dc
            coords_trace.append((r_curr, c_curr))
            
    return coords_trace # Return full list including start and end