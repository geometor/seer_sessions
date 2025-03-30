# Adapted from Wikipedia Bresenham's Line Algorithm pseudocode
def bresenham_wikipedia(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0) # Note the negative sign
    sy = 1 if y0 < y1 else -1
    err = dx + dy # error value e_xy

    while True:
        points.append((x0, y0)) # Use (row, col) -> (y, x) convention if needed
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy: # e_xy+e_x >= 0
            err += dy
            x0 += sx
        if e2 <= dx: # e_xy+e_y <= 0
            err += dx
            y0 += sy
    return points