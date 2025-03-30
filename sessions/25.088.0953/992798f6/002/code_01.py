    while True:
        points.append((r0, c0))
        if r0 == r1 and c0 == c1: break
        e2 = 2 * err
        if e2 > -dc: # Condition to step in r direction
            err -= dc
            r0 += sr
        if e2 < dr:  # Condition to step in c direction
            err += dr
            c0 += sc