```python
import numpy as np
import collections

"""
Transforms an input grid based on the following rules:

1.  Identify static elements: Horizontal and vertical lines (contiguous segments of 2+ identical non-white pixels) and the white background. These remain unchanged in the output.
2.  Identify agent elements: Single non-white pixels that are not part of any identified line.
3.  For each agent pixel:
    a.  Find all lines in the grid that have the same color as the agent.
    b.  If no same-colored line exists, the agent is removed (becomes white) in the output.
    c.  If same-colored lines exist, find the nearest one based on perpendicular distance.
    d.  Calculate the target position, which is one step away from the nearest line, on the same side as the agent's original position.
    e.  Check the path: Examine all grid cells strictly between the agent's original position and the target position.
    f.  If this path intersects *any* pixel belonging to *any* identified line, the agent is removed (becomes white).
    g.  If the path is clear, the agent is moved to the target position in the output grid. Original agent positions are cleared (set to white) unless overwritten by another moved agent.
4.  The final output grid contains the static lines and the agents in their new positions (or removed).
"""

def _find_lines_and_agents(grid):
    """Identifies lines and agent pixels in the grid."""
    height, width = grid.shape
    lines = []
    line_coords = set()
    
    # Find horizontal lines
    for r in range(height):
        start_col = -1
        current_color = -1
        for c in range(width):
            pixel = grid[r, c]
            if pixel != 0:
                if start_col == -1: # Start of a potential line
                    start_col = c
                    current_color = pixel
                elif pixel != current_color: # End of line (different color)
                    if c - start_col >= 2:
                        lines.append({'color': current_color, 'orientation': 'h', 'row': r, 'start': start_col, 'end': c - 1})
                        for i in range(start_col, c):
                           line_coords.add((r, i))
                    start_col = c # Start new potential line
                    current_color = pixel
            elif start_col != -1: # End of line (white pixel)
                 if c - start_col >= 2:
                     lines.append({'color': current_color, 'orientation': 'h', 'row': r, 'start': start_col, 'end': c - 1})
                     for i in range(start_col, c):
                        line_coords.add((r, i))
                 start_col = -1
                 current_color = -1
        # Check for line ending at the edge
        if start_col != -1 and width - start_col >= 2:
            lines.append({'color': current_color, 'orientation': 'h', 'row': r, 'start': start_col, 'end': width - 1})
            for i in range(start_col, width):
               line_coords.add((r, i))

    # Find vertical lines
    for c in range(width):
        start_row = -1
        current_color = -1
        for r in range(height):
            pixel = grid[r, c]
            if pixel != 0:
                if start_row == -1: # Start of a potential line
                    start_row = r
                    current_color = pixel
                elif pixel != current_color: # End of line (different color)
                    if r - start_row >= 2:
                         lines.append({'color': current_color, 'orientation': 'v', 'col': c, 'start': start_row, 'end': r - 1})
                         for i in range(start_row, r):
                            # Avoid adding coords twice if part of H and V line
                            line_coords.add((i, c)) 
                    start_row = r # Start new potential line
                    current_color = pixel
            elif start_row != -1: # End of line (white pixel)
                 if r - start_row >= 2:
                     lines.append({'color': current_color, 'orientation': 'v', 'col': c, 'start': start_row, 'end': r - 1})
                     for i in range(start_row, r):
                        line_coords.add((i, c))
                 start_row = -1
                 current_color = -1
        # Check for line ending at the edge
        if start_row != -1 and height - start_row >= 2:
             lines.append({'color': current_color, 'orientation': 'v', 'col': c, 'start': start_row, 'end': height - 1})
             for i in range(start_row, height):
                line_coords.add((i, c))

    # Find agents (single non-white pixels not in line_coords)
    agents = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in line_coords:
                agents.append({'color': grid[r, c], 'r': r, 'c': c})

    return lines, agents, line_coords

def _is_path_blocked(start_pos, end_pos, line_coords):
    """Checks if the path between start and end (exclusive) intersects any line coords."""
    r_start, c_start = start_pos
    r_end, c_end = end_pos
    
    # Vertical movement
    if c_start == c_end:
        r_min = min(r_start, r_end)
        r_max = max(r_start, r_end)
        for r in range(r_min + 1, r_max):
            if (r, c_start) in line_coords:
                return True
    # Horizontal movement
    elif r_start == r_end:
        c_min = min(c_start, c_end)
        c_max = max(c_start, c_end)
        for c in range(c_min + 1, c_max):
             if (r_start, c) in line_coords:
                return True
    # Diagonal or other movement (not expected by rules, but check anyway)
    else:
        # This scenario shouldn't occur based on the perpendicular movement rule.
        # If it did, we'd need a line-drawing algorithm (like Bresenham's)
        # to check intermediate points. Assuming only H/V movement.
        pass 
        
    return False


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Moves single pixels towards the nearest line of the same color, stopping one step away,
    unless the path is blocked by any line or no same-colored line exists.
    """
    # Initialize output_grid as a copy of the input
    output_grid = input_grid.copy()
    height, width = output_grid.shape

    # 1. Identify lines, agents, and coordinates belonging to lines
    lines, agents, line_coords = _find_lines_and_agents(input_grid)

    # 2. Temporarily remove agents from the output grid
    for agent in agents:
        output_grid[agent['r'], agent['c']] = 0

    # 3. Process each agent
    for agent in agents:
        agent_color = agent['color']
        agent_r, agent_c = agent['r'], agent['c']

        # a. Find matching lines
        matching_lines = [line for line in lines if line['color'] == agent_color]

        # b. If no matching line, agent stays removed (already set to 0)
        if not matching_lines:
            continue

        # c. Find the nearest matching line
        nearest_line = None
        min_dist = float('inf')

        for line in matching_lines:
            dist = -1
            if line['orientation'] == 'h':
                # Check if agent's column is within the line's horizontal span
                if line['start'] <= agent_c <= line['end']:
                    dist = abs(agent_r - line['row'])
                else: # Need distance to closest endpoint column-wise AND row-wise
                    # This seems overly complex and likely not intended by ARC rules.
                    # Let's stick to perpendicular distance first.
                    # Revisit if examples fail.
                    # Simple perpendicular distance:
                    dist = abs(agent_r - line['row'])

            elif line['orientation'] == 'v':
                 # Check if agent's row is within the line's vertical span
                if line['start'] <= agent_r <= line['end']:
                    dist = abs(agent_c - line['col'])
                else: # As above, stick to perpendicular
                    dist = abs(agent_c - line['col'])
            
            # Update nearest line if this one is closer
            # Simple tie-breaking: prefer horizontal, then lower index if still tied (implicit in iteration order)
            if dist >= 0 and dist < min_dist:
                min_dist = dist
                nearest_line = line
            elif dist == min_dist:
                 # Prioritize horizontal over vertical if distances are equal? Let's try this.
                 if nearest_line and nearest_line['orientation'] == 'v' and line['orientation'] == 'h':
                     nearest_line = line
                 # Otherwise, keep the first one found (implicit)

        # If a nearest line was found (should always happen if matching_lines is not empty)
        if nearest_line:
            # d. Calculate target position
            target_r, target_c = -1, -1
            if nearest_line['orientation'] == 'h':
                target_c = agent_c
                line_row = nearest_line['row']
                if agent_r < line_row:
                    target_r = line_row - 1
                else: # agent_r > line_row (cannot be equal, agent isn't *on* line)
                    target_r = line_row + 1
            elif nearest_line['orientation'] == 'v':
                target_r = agent_r
                line_col = nearest_line['col']
                if agent_c < line_col:
                    target_c = line_col - 1
                else: # agent_c > line_col
                    target_c = line_col + 1

            # Ensure target is within bounds (should be if lines are)
            if 0 <= target_r < height and 0 <= target_c < width:
                # e. Check path for blockage by ANY line
                path_blocked = _is_path_blocked((agent_r, agent_c), (target_r, target_c), line_coords)

                # f/g. Place agent if path is clear
                if not path_blocked:
                    output_grid[target_r, target_c] = agent_color
            # else: target is out of bounds, agent is removed (remains 0)
        # else: agent is removed (remains 0) - this case handled by empty matching_lines check

    # 4. Return the final grid
    return output_grid
```