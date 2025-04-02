Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Input Grids:** Contain sparse distributions of non-white pixels (colors 1 through 9) on a white (0) background.
2.  **Output Grids:** Show the original non-white pixels, plus additional filled areas connected to or between some of the original pixels. The background remains white.
3.  **Color Roles:** Different colors seem to behave differently.
    *   Some colors act as "sources" that expand outwards.
    *   Some colors act as static "obstacles" that block expansion.
    *   Some colors might change their expansion behavior based on the presence of other colors in the input.
    *   Yellow (4) seems unique, often filling horizontal segments between pairs.
4.  **Expansion Pattern:** The filled areas suggest an expansion process based on Manhattan distance (cardinal neighbors). Expansion seems to occur simultaneously from all sources. Where expansions from different sources would meet at the same time, the cell remains empty (white). Expansion stops upon hitting any non-white cell (original or newly filled) or the grid boundary.
5.  **Expansion Color Logic:** The color used for filling isn't always the same as the source color.
    *   In train\_1, Magenta (6) expands as Orange (7), and Azure (8) expands as Blue (1). Yellow (4) connects horizontally with Yellow (4).
    *   In train\_2, Azure (8) expands as Blue (1), but Magenta (6) expands as Magenta (6). Blue (1) expands as Blue (1), Yellow (4) expands as Yellow (4).
    *   In train\_3, all source colors (Azure 8, Blue 1, Orange 7, Yellow 4, Red 2) expand using their *own* color. Yellow (4) also performs its horizontal connection.
6.  **Context Dependency:** The specific expansion colors seem dependent on the overall context of the input grid:
    *   Azure (8) expands as Blue (1) *only if* a Magenta (6) source pixel is present in the input grid (seen in train\_1 and train\_2, but not train\_3). Otherwise, Azure (8) expands as Azure (8).
    *   Magenta (6) expands as Orange (7) *only if* an Orange (7) pixel (source or obstacle) is present anywhere in the input grid (seen in train\_1, but not train\_2). Otherwise, Magenta (6) expands as Magenta (6).

**YAML Facts:**


```yaml
Task: Expand or connect colored pixels based on specific rules.

Objects:
  - Type: Pixel
    Properties:
      - Color: Integer (0-9, representing White, Blue, Red, Green, Yellow, Gray, Magenta, Orange, Azure, Maroon)
      - Position: (row, column)
      - Role: Can be Source, Obstacle, Background(White), or Filled.

Relationships:
  - Adjacency: Pixels can be cardinally adjacent (up, down, left, right).
  - Source-Expansion: Certain source colors expand into adjacent white pixels.
  - Source-Obstacle: Expansion stops when encountering any non-white pixel.
  - Source-Source Interaction: Simultaneous expansion; conflicts (meeting at the same step) result in no fill.
  - Horizontal Connection: Yellow (4) pixels can connect horizontally.

Actions/Transformations:
  - Yellow Connection:
    - Identify pairs of Yellow (4) pixels on the same row.
    - If the segment between them consists only of White (0) pixels, fill the segment with Yellow (4).
    - This step seems to occur first, and the filled pixels act as obstacles for subsequent expansion.
  - Determine Expansion Colors:
    - Default: Source color C expands as color C.
    - Exception 1: If any Magenta (6) source exists in the input, Azure (8) sources expand as Blue (1).
    - Exception 2: If any Orange (7) pixel exists in the input, Magenta (6) sources expand as Orange (7).
  - Simultaneous Expansion (BFS):
    - Initialize: Start BFS from all non-Yellow source pixels simultaneously.
    - Propagation: Expand one step (Manhattan distance) into adjacent, originally White (0) cells per iteration.
    - Conflict Resolution: If a White cell is reached by multiple different sources in the same iteration, it remains White (0) and is marked as contested.
    - Termination: Expansion stops at grid boundaries, original non-white pixels, Yellow-filled pixels, and contested cells.
  - Output Generation:
    - Copy the input grid.
    - Apply Yellow connection fills.
    - Apply BFS expansion fills according to the determined expansion colors and conflict resolution.

Input Grid Properties Check:
  - `has_magenta_source`: True if any input pixel == 6.
  - `has_orange_anywhere`: True if any input pixel == 7.

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  **Yellow Connection Phase:**
    *   Repeatedly scan the grid horizontally.
    *   For each row, find all pairs of Yellow (4) pixels.
    *   For each pair, check if all pixels strictly between them in that row are currently White (0) in the output grid.
    *   If they are, fill those intervening White pixels with Yellow (4).
    *   Continue scanning and filling until no more Yellow connections can be made in a full pass.
3.  **Expansion Phase Preparation:**
    *   Identify all non-White, non-Yellow pixels in the original input grid. These are the "source" pixels for the expansion phase.
    *   Check the original input grid for the presence of any Magenta (6) pixels (let's call this `has_magenta_source`).
    *   Check the original input grid for the presence of any Orange (7) pixels (let's call this `has_orange_anywhere`).
    *   Create a mapping `expansion_color_map` for each source color found:
        *   If a source color is Azure (8) AND `has_magenta_source` is true, map it to Blue (1).
        *   Else if a source color is Magenta (6) AND `has_orange_anywhere` is true, map it to Orange (7).
        *   Otherwise, map the source color to itself.
4.  **Simultaneous Expansion Phase (BFS):**
    *   Create a distance grid initialized to infinity, and an owner grid initialized to null.
    *   Create a queue and add the initial state for each source pixel: `(row, col, distance=0, source_pixel_coords)`. Set distance grid to 0 and owner grid to `source_pixel_coords` at these locations.
    *   While the queue is not empty:
        *   Process all elements currently in the queue belonging to the current distance `d`.
        *   For each processed pixel `(r, c)` with owner `S`:
            *   Examine its cardinal neighbors `(nr, nc)`.
            *   If `(nr, nc)` is within grid bounds AND the original input grid at `(nr, nc)` was White (0):
                *   If `distance[nr][nc]` is infinity (not yet reached):
                    *   Set `distance[nr][nc] = d + 1`.
                    *   Set `owner[nr][nc] = S`.
                    *   Add `(nr, nc, d + 1, S)` to a queue/list for the next distance level (`d+1`).
                *   Else if `distance[nr][nc] == d + 1` (reached in the same step) AND `owner[nr][nc]` is not `S` and not "CONTESTED":
                    *   Set `owner[nr][nc] = "CONTESTED"` (mark as conflict).
5.  **Final Output Construction:**
    *   Iterate through the grid cells `(r, c)`.
    *   If `owner[r][c]` is a valid source coordinate `S` (not null, not "CONTESTED") AND the original input grid at `(r, c)` was White (0):
        *   Get the original color `C` of the source pixel `S` from the input grid.
        *   Get the corresponding expansion color `E` from the `expansion_color_map` based on `C`.
        *   Set `output_grid[r][c] = E`.
6.  Return the final output grid.


```python
import numpy as np

# Example visualization of train_1 input (replace with actual grid later)
train_1_input_vis = """
....................
....................
.......M............
....................
....................
...O................
...M...........BA.B.
.....GG.............
............M.......
....................
..G.......G.........
....................
...................B
.....GG.............
..............BB....
....................
....................
.....Y.......Y......
....................
....................
"""

# Conceptual check of rules on train_1
# has_magenta_source = True (M at 2,7; 6,3; 8,13)
# has_orange_anywhere = True (O at 5,3)
# Expansion map: M(6)->O(7), A(8)->B(1), Y(4)->Y(4) (special connect), G(3)->G(3), B(1)->B(1), O(7)->O(7) (non-sources)
# Yellow connect: Row 17, fill 6-11 with Y(4).
# BFS: Start from M(6) and A(8) coords. Use O(7) and B(1) as fill colors respectively. Avoid original non-white, newly filled Y(4), and contested cells.

# Conceptual check of rules on train_2
# has_magenta_source = True (M at 5,11; 5,13; 8,16; 12,11)
# has_orange_anywhere = False
# Expansion map: A(8)->B(1), M(6)->M(6), Y(4)->Y(4), B(1)->B(1), G(3)->G(3)
# Yellow connect: None applicable.
# BFS: Start from A(8), M(6), Y(4), B(1) coords. Use B(1), M(6), Y(4), B(1) as fill colors. Avoid original G(3) and contested cells.

# Conceptual check of rules on train_3
# has_magenta_source = False
# has_orange_anywhere = True (O at 4,4; 4,10; 5,11; 6,11; etc.) - Actually, source O7 at (4,4), (4,10), (5,11), (10,4), (10,6)
# Expansion map: A(8)->A(8), B(1)->B(1), O(7)->O(7), Y(4)->Y(4), R(2)->R(2)
# Yellow connect: Row 10, fill 5 with Y(4).
# BFS: Start from A(8), B(1), O(7), Y(4), R(2) coords. Use respective colors for fill. Avoid newly filled Y(4) and contested cells.

```