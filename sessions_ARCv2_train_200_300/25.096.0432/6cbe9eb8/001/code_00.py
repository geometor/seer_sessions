import copy

"""
Identifies all rectangular regions within the input grid that are enclosed by a solid border of a single, uniform digit. 
Calculates the area of each identified rectangle. Selects the rectangle with the largest area. Extracts and returns 
the subgrid corresponding to this largest rectangle, including its border.
"""

def _is_valid(r, c, R, C):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < R and 0 <= c < C

def _check_border(input_grid, r1, c1, r2, c2, border_digit):
    """Check if the border of the rectangle defined by (r1, c1) and (r2, c2) is solid and matches border_digit."""
    R = len(input_grid)
    C = len(input_grid[0])

    # Check top border
    for c in range(c1, c2 + 1):
        if not _is_valid(r1, c, R, C) or input_grid[r1][c] != border_digit:
            return False
            
    # Check bottom border
    for c in range(c1, c2 + 1):
        if not _is_valid(r2, c, R, C) or input_grid[r2][c] != border_digit:
            return False
            
    # Check left border (excluding corners)
    for r in range(r1 + 1, r2):
        if not _is_valid(r, c1, R, C) or input_grid[r][c1] != border_digit:
            return False
            
    # Check right border (excluding corners)
    for r in range(r1 + 1, r2):
        if not _is_valid(r, c2, R, C) or input_grid[r][c2] != border_digit:
            return False
            
    return True

def _extract_subgrid(input_grid, r1, c1, r2, c2):
    """Extracts the subgrid defined by the rectangle corners."""
    subgrid = []
    for r in range(r1, r2 + 1):
        subgrid.append(input_grid[r][c1 : c2 + 1])
    return subgrid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Finds the largest rectangle defined by a solid border of a single digit
    within the input grid and returns that rectangle as a subgrid.
    """
    R = len(input_grid)
    if R == 0:
        return []
    C = len(input_grid[0])
    if C == 0:
        return []

    found_rectangles = []

    # 1. Iterate through each cell as a potential top-left corner (r1, c1).
    for r1 in range(R):
        for c1 in range(C):
            border_digit = input_grid[r1][c1]
            
            # 2. Iterate through each cell as a potential bottom-right corner (r2, c2).
            #    Start from r1, c1 to ensure width and height >= 1.
            for r2 in range(r1, R):
                for c2 in range(c1, C):
                    # Basic check: bottom-right corner must match border digit
                    if input_grid[r2][c2] != border_digit:
                        continue
                        
                    # 3. Check if the rectangle defined by (r1, c1) and (r2, c2) has a valid solid border.
                    if _check_border(input_grid, r1, c1, r2, c2, border_digit):
                        # 4. If valid, calculate area and store rectangle info.
                        height = r2 - r1 + 1
                        width = c2 - c1 + 1
                        area = height * width
                        found_rectangles.append({
                            "r1": r1, "c1": c1, 
                            "r2": r2, "c2": c2, 
                            "area": area
                        })

    # 5. Identify the rectangle with the largest area.
    if not found_rectangles:
        return [] # Or handle error appropriately if a rectangle is always expected

    largest_rectangle = max(found_rectangles, key=lambda x: x["area"])

    # 6. Extract the subgrid corresponding to the largest rectangle.
    output_grid = _extract_subgrid(
        input_grid,
        largest_rectangle["r1"], largest_rectangle["c1"],
        largest_rectangle["r2"], largest_rectangle["c2"]
    )

    # 7. Return the extracted subgrid.
    return output_grid