import numpy as np

def get_contiguous_pixels(grid, start_pixel, color):
    """
    Finds all pixels contiguous to a starting pixel of a given color using 8-neighbor adjacency.

    Args:
        grid: The 2D numpy array.
        start_pixel: (row, col) tuple.
        color: The color value to match.

    Returns:
        A set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    to_visit = {start_pixel}

    while to_visit:
        current_pixel = to_visit.pop()
        visited.add(current_pixel)

        row, col = current_pixel
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < rows and 0 <= new_col < cols:
                    if (new_row, new_col) not in visited and grid[new_row, new_col] == color:
                        to_visit.add((new_row, new_col))
    return visited

def is_closed_region(grid, green_pixels):
    """
    Checks if a set of green pixels forms a closed region.
    """
    rows, cols = grid.shape
    for r, c in green_pixels:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nr, nc = r + i, c + j
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr, nc] != 3: # Check for non-green neighbors
                        continue
                else: return False #if is out of bounds, region is not closed
    return True

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input-output example pair.
    """
    rows, cols = input_grid.shape
    green_pixels = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 3:
                green_pixels.add((r, c))

    distinct_regions = []
    visited_pixels = set()
    for pixel in green_pixels:
        if pixel not in visited_pixels:
            region = get_contiguous_pixels(input_grid, pixel, 3)
            distinct_regions.append(region)
            visited_pixels.update(region)

    num_regions = len(distinct_regions)
    closed_regions = 0
    correctly_filled = True

    for region in distinct_regions:
        if is_closed_region(input_grid, region):
            closed_regions += 1
            # Check if the interior is filled with yellow in the output
            min_row = min(r for r, _ in region)
            max_row = max(r for r, _ in region)
            min_col = min(c for _, c in region)
            max_col = max(c for _, c in region)
            for r in range(min_row + 1, max_row):
                for c in range(min_col + 1, max_col):
                    if (r,c) in region:
                        is_surrounded = True
                        for i in range(-1, 2):
                            for j in range(-1,2):
                                if i == 0 and j == 0: continue
                                nr,nc = r+i, c+j
                                if (nr, nc) not in region:
                                    is_surrounded = False
                                    break
                            if not is_surrounded: break
                        if is_surrounded:
                            if output_grid[r,c] != 4:
                                correctly_filled = False
                                break
                if not correctly_filled: break


        else:
          #if is not closed, check if it has been filled
          for r, c in region:
            if output_grid[r,c] == 4:
              correctly_filled = False
              break

    return {
        "num_green_regions": num_regions,
        "num_closed_regions": closed_regions,
        "correctly_filled": correctly_filled,
    }

def main():
    # Example grids (Replace with your actual grid data)
    input_grids = [
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                  [0, 0, 0, 0, 3, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 3, 3, 3, 3, 3, 0, 0],
                  [0, 0, 0, 3, 3, 3, 3, 3, 0, 0],
                  [0, 0, 0, 3, 3, 3, 3, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 3, 0, 3, 0, 0, 0],
                  [0, 0, 3, 0, 0, 0, 3, 0, 0],
                  [0, 3, 0, 0, 0, 0, 0, 3, 0],
                  [0, 0, 3, 0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 3, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]])

    ]
    output_grids = [
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                  [0, 0, 0, 0, 3, 4, 3, 0, 0, 0],
                  [0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 3, 3, 3, 3, 3, 0, 0],
                  [0, 0, 0, 3, 3, 3, 3, 3, 0, 0],
                  [0, 0, 0, 3, 3, 3, 3, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 3, 0, 3, 0, 0, 0],
                  [0, 0, 3, 0, 0, 0, 3, 0, 0],
                  [0, 3, 0, 0, 0, 0, 0, 3, 0],
                  [0, 0, 3, 0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 3, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    ]

    for i, (input_grid, output_grid) in enumerate(zip(input_grids, output_grids)):
        results = analyze_example(input_grid, output_grid)
        print(f"Example {i+1}:")
        print(f"  Number of green regions: {results['num_green_regions']}")
        print(f"  Number of closed green regions: {results['num_closed_regions']}")
        print(f"  Correctly filled: {results['correctly_filled']}")
        print("-" * 20)

if __name__ == "__main__":
    main()