def bresenham_line(r0, c0, r1, c1):
    points = []
    dr = abs(r1 - r0)
    dc = abs(c1 - c0)
    sr = 1 if r0 < r1 else -1
    sc = 1 if c0 < c1 else -1
    err = dr - dc # Initial error term

    while True:
        points.append((r0, c0))
        if r0 == r1 and c0 == c1:
            break
        e2 = 2 * err # Error doubled
        # Check for vertical step
        if e2 > -dc: # Condition: 2*(dr-dc) > -dc => 2*dr - 2*dc > -dc => 2*dr > dc
            err -= dc # Adjust error by -dc
            r0 += sr # Step vertically
        # Check for horizontal step (can happen in same iteration -> diagonal)
        if e2 < dr: # Condition: 2*(dr-dc) < dr => 2*dr - 2*dc < dr => dr < 2*dc
            err += dr # Adjust error by +dr
            c0 += sc # Step horizontally
    return points