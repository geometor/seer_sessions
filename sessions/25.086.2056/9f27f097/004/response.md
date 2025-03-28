**Metric Analysis:**

1.  **White Block:** In all examples, there is exactly one solid white rectangular block. Its properties are correctly identified by `get_block_properties`.
2.  **Pattern Block (Intended):** In all examples, the intended pattern block (identified visually from the expected output) has the *exact same dimensions* as the white block. It does *not* contain white pixels. It is *not* a solid block of a single color.
3.  **Dimensions Match:** The dimensions of the white block and the intended pattern block match in all examples.
4.  **Other Non-White Blocks:** The code execution confirms that scanning the grid finds *many* rectangular regions that match the dimensions of the white block and do not contain white. The previous code's logic of picking the *first* one found (often the top-left block of background color) was incorrect.
5.  **Uniqueness:** In each example, the *intended* pattern block appears to be the *only* block of the correct dimensions that contains multiple colors (i.e., is not solid) and does not contain white. Let's re-check the "Other Non-White Blocks" output.
    *   Ex 1: White block 5x5. Intended pattern at (6,1) has colors [1, 4]. The block at (0,0) has [2]. Block at (2,0) has [1, 2, 4]. Block at (5,1) has [1, 2, 4]. Block at (5,5) has [1, 2, 4]. Okay, the uniqueness based on *not being solid* might not hold. What makes the intended pattern block unique?
    *   Could it be the block with the most unique colors?
        *   Ex 1: Pattern(6,1) -> [1, 4] (2 colors). Block(2,0) -> [1, 2, 4] (3 colors). No.
    *   Could it be related to position?
        *   Ex 1: White (0,5), Pattern (6,1).
        *   Ex 2: White (7,4), Pattern (1,1).
        *   Ex 3: White (8,3), Pattern (2,1).
        No obvious positional relationship.
    *   Let's look at the surrounding pixels. Are these blocks perhaps bounded by a specific color?
        *   Ex 1: White block is surrounded by red (2). Pattern block is surrounded by red (2).
        *   Ex 2: White block is surrounded by red (2). Pattern block is surrounded by red (2).
        *   Ex 3: White block is surrounded by blue (1). Pattern block is surrounded by blue (1).
        This seems promising! The white block and the pattern block are both enclosed within a larger area of a single, non-white color (which acts as the background/border color for these objects).

**Revised Hypothesis 2:**
1.  Identify the unique solid white (color 0) rectangular block. Let its dimensions be HxW and its location be (wr, wc).
2.  Find the bounding box of the white block. Check the color of the pixels immediately adjacent (N, S, E, W) to this bounding box. Assume these adjacent pixels share a single, common color (the 'border' color, C_border). C_border must not be white.
3.  Search the *entire* grid for *another* rectangular region of size HxW that:
    *   Is located at (pr, pc), where (pr, pc) is not equal to (wr, wc).
    *   Does *not* contain any white pixels (color 0).
    *   Is also "bordered" by the *same* color C_border found in step 2. (Check pixels adjacent to the HxW region at (pr, pc)).
4.  Assume there is exactly one such "pattern" region.
5.  Copy the contents of this unique pattern region onto the location (wr, wc) in the output grid.

Let's test this revised hypothesis.

*   **Example 1:** White block (0,5, 5x5). Border color is red (2). Search for another 5x5 block bordered by red (2), containing no white (0). The block at (6,1, 5x5) fits this description. It contains colors [1, 4]. It is bordered by red (2).
*   **Example 2:** White block (7,4, 4x4). Border color is red (2). Search for another 4x4 block bordered by red (2), containing no white (0). The block at (1,1, 4x4) fits this description. It contains colors [1, 3]. It is bordered by red (2).
*   **Example 3:** White block (8,3, 4x6). Border color is blue (1). Search for another 4x6 block bordered by blue (1), containing no white (0). The block at (2,1, 4x6) fits this description. It contains colors [2, 3]. It is bordered by blue (1).

This hypothesis seems consistent with all examples. The "border" color acts as a key to link the white block and the pattern block.

---

## General Assessment and Strategy

The previous code failed because it incorrectly identified the "pattern" block. It assumed the pattern block was the first block found matching the white block's dimensions and not containing white pixels. The analysis of all examples reveals a more specific rule:

1.  Both the white block (target) and the pattern block (source) are rectangular and have the *exact same dimensions*.
2.  The white block is solid white (color 0).
3.  The pattern block contains *no* white pixels.
4.  Crucially, both the white block and the pattern block are immediately surrounded by pixels of the *same* single background color (which is not white). This background color serves to identify the correct pattern block among potentially many non-white blocks of the correct size.

The strategy is to:
1.  Find the solid white block and determine its dimensions and location.
2.  Identify the color of the pixels immediately surrounding the white block (assuming it's a single, non-white color).
3.  Iterate through all possible block locations in the grid.
4.  For each location, check if a block of the same dimensions as the white block exists there.
5.  If it exists, check if it contains white pixels.
6.  If it doesn't contain white, check if it is surrounded by the *same* background color identified in step 2.
7.  If all conditions are met, this is the pattern block.
8.  Copy the pattern block's content to the white block's location in the output grid.

## Metrics

Metrics gathered via `tool_code` execution confirm:
*   A single, solid white rectangle exists in each input.
*   A corresponding "pattern" rectangle exists with identical dimensions.
*   This pattern rectangle contains no white pixels.
*   The pattern rectangle is typically multi-colored (not solid).
*   There are often multiple rectangular regions matching the dimensions and non-white criteria, necessitating a more specific selection rule.
*   Visual inspection (and the revised hypothesis) suggests the surrounding background color is the key differentiator.

## Facts YAML


```yaml
task_description: Copy a pattern from a source block onto a target block within a grid.

definitions:
  - &grid_input The input 2D array of integers (colors).
  - &grid_output The output 2D array of integers (colors).
  - &white_block
    type: object
    description: A solid rectangular block composed entirely of white (0) pixels.
    properties:
      color: 0
      shape: rectangle
      solid: true
  - &pattern_block
    type: object
    description: A rectangular block used as the source pattern.
    properties:
      shape: rectangle
      solid: false # Usually contains multiple colors
      contains_white: false
  - &background_color
    type: property
    description: The single color of the pixels immediately adjacent to the outer border of both the white_block and the pattern_block. This color is not white.

grid_elements:
  - <<: *white_block
    location: Unique location within the grid_input.
    role: Target area for the copy operation.
  - <<: *pattern_block
    location: Unique location within the grid_input, different from white_block location.
    role: Source area for the copy operation.
    relationship:
      - type: size_match
        target: *white_block
        details: Has the exact same height and width as the white_block.
      - type: background_match
        target: *white_block
        details: Is surrounded by the same background_color as the white_block.

actions:
  - name: identify_white_block
    description: Locate the unique solid white rectangular block in the grid_input. Determine its bounding box (row, col, height, width).
  - name: identify_background_color
    description: Determine the single color surrounding the identified white_block. Check pixels adjacent to its bounding box.
  - name: identify_pattern_block
    description: >
      Search the grid_input for a rectangular block that:
      1. Has the same height and width as the white_block.
      2. Is not the white_block itself.
      3. Contains no white (0) pixels.
      4. Is surrounded by the same background_color identified previously.
      Assume exactly one such block exists. Determine its bounding box.
  - name: copy_pattern
    description: Create the grid_output by copying the grid_input, then replacing the area defined by the white_block's bounding box with the content of the area defined by the pattern_block's bounding box.

assumptions:
  - There is exactly one solid white rectangular block in the input.
  - There is exactly one pattern block matching the criteria (same dimensions, no white, same background border color) in the input.
  - The pixels immediately surrounding the white block are all of the same, non-white color.
  - The pixels immediately surrounding the pattern block are all of the same color, and this color matches the white block's surrounding color.
```


## Natural Language Program

1.  **Initialize Output:** Create a copy of the input grid, which will become the output grid.
2.  **Find White Block:** Locate the unique, solid, rectangular block consisting entirely of white pixels (color 0) in the input grid. Record its top-left corner coordinates (row `wr`, column `wc`), height `h`, and width `w`.
3.  **Find Border Color:** Identify the color (`C_border`) of the pixels directly adjacent to the outside border of the white block found in step 2. Assume this border consists of a single, uniform color, and that this color is not white.
4.  **Find Pattern Block:** Search the input grid for another rectangular block that meets all the following criteria:
    a.  Its top-left corner is at coordinates (`pr`, `pc`), where (`pr`, `pc`) is different from (`wr`, `wc`).
    b.  Its dimensions are exactly `h` x `w`.
    c.  It does not contain any white pixels (color 0).
    d.  It is immediately surrounded only by pixels of the color `C_border` (identified in step 3).
5.  **Extract Pattern:** Copy the content (the `h` x `w` array of pixels) from the pattern block found in step 4.
6.  **Apply Pattern:** Paste the extracted pattern content into the output grid at the location (`wr`, `wc`), overwriting the original white block.
7.  **Return Output:** The modified grid is the final output.## General Assessment and Strategy

The provided Python code failed because its method for identifying the "pattern" block was too simplistic, relying only on matching dimensions and the absence of white pixels. This led to incorrect blocks (often uniform background-colored areas) being selected.

Analysis of all three examples reveals a more nuanced relationship between the target white block and the source pattern block:
1.  **Target:** A unique, solid white (color 0) rectangle exists.
2.  **Source:** A unique rectangle (the "pattern block") exists with the *exact same dimensions* as the white block.
3.  **Source Content:** The pattern block contains *no* white pixels but typically contains multiple other colors.
4.  **Linking Feature:** Both the white block and the pattern block are immediately surrounded by pixels of the *same* single, non-white background/border color. This shared border color appears to be the key identifier for the correct pattern block.

The strategy requires refining the search for the pattern block to include the border color constraint:
1.  Find the white block and its dimensions.
2.  Determine the color surrounding the white block.
3.  Search for a block with the same dimensions, no white content, *and* the same surrounding border color.
4.  Copy this correctly identified pattern onto the white block's location.

## Metrics

Code execution and analysis confirm the following properties across the examples:
*   **White Block:** Consistently a single, solid (all color 0) rectangle.
*   **Pattern Block:**
    *   Dimensions always match the white block exactly.
    *   Never contains white (color 0) pixels.
    *   Usually contains multiple different colors (is not solid).
*   **Border Color:** Visual inspection and the revised hypothesis strongly suggest both the white block and the intended pattern block share the same single, non-white surrounding color in each example (Red=2 in Ex1/Ex2, Blue=1 in Ex3).
*   **Ambiguity:** Simply searching for non-white blocks of the correct size yields many candidates, highlighting the failure of the original code and the necessity of the border color constraint.

## Facts YAML


```yaml
task_description: Overwrite a specific white rectangular area with a pattern found elsewhere in the grid, identified by matching dimensions and surrounding background color.

definitions:
  - &grid_input The input 2D array of integers (colors).
  - &grid_output The output 2D array of integers (colors).
  - &white_block
    type: object
    description: The target region to be overwritten.
    properties:
      color: 0 # white
      shape: rectangle
      solid: true
      unique: true # Assumed to be the only solid white rectangle.
  - &pattern_block
    type: object
    description: The source region containing the pattern to be copied.
    properties:
      shape: rectangle
      solid: false # Typically contains multiple colors.
      contains_white: false
      unique: true # Assumed to be the only block matching all criteria.
  - &border_color
    type: property
    description: >
      The single color of the pixels immediately adjacent to the outer border
      of both the white_block and the pattern_block. This color is not white.

grid_elements:
  - <<: *white_block
    location: A specific bounding box (row, col, height, width) within grid_input.
    role: Target area for the copy operation.
  - <<: *pattern_block
    location: A specific bounding box (row, col, height, width) within grid_input, different from white_block location.
    role: Source area for the copy operation.
    relationship:
      - type: size_match
        target: *white_block
        details: Has the exact same height and width as the white_block.
      - type: border_match
        target: *white_block
        details: Is surrounded by the same border_color as the white_block.

actions:
  - name: identify_white_block
    description: Locate the unique solid white rectangular block in the grid_input. Determine its bounding box (wr, wc, h, w).
  - name: identify_border_color
    description: >
      Examine the pixels immediately adjacent to the bounding box of the white_block.
      Verify they all share the same single color, C_border. C_border must not be white (0).
  - name: find_pattern_block
    description: >
      Iterate through all possible top-left coordinates (pr, pc) in the grid_input.
      For each, consider the h x w rectangle starting at (pr, pc).
      Select the rectangle that satisfies ALL of the following:
      1. Is not the white_block (i.e., (pr, pc) != (wr, wc)).
      2. Contains no white (0) pixels within its h x w area.
      3. Is fully surrounded by pixels of color C_border (identified in the previous step).
      Assume exactly one such rectangle exists. This is the pattern_block. Record its location (pr, pc).
  - name: perform_copy
    description: >
      Create the grid_output by copying the grid_input.
      Extract the h x w pixel data from the pattern_block at location (pr, pc).
      Overwrite the h x w area in the grid_output starting at location (wr, wc) with the extracted pattern data.

assumptions:
  - There is exactly one solid white rectangular block.
  - The white block is surrounded by pixels of a single, non-white color.
  - There is exactly one other block in the grid that matches the white block's dimensions, contains no white pixels, and is surrounded by the same border color.
  - The border surrounding both blocks is at least one pixel thick where applicable (i.e., the blocks are not touching the grid edges everywhere).
```


## Natural Language Program

1.  **Initialize Output:** Create an exact copy of the input grid. This copy will be modified to become the output grid.
2.  **Find White Target Block:** Scan the input grid to find the unique rectangular block composed entirely of white (0) pixels. Determine its top-left coordinates (`wr`, `wc`), height `h`, and width `w`.
3.  **Determine Border Color:** Identify the color (`C_border`) of the pixels directly adjacent to the perimeter of the white block found in step 2. Confirm this border is composed of a single, uniform color and that `C_border` is not white (0).
4.  **Find Source Pattern Block:** Search the input grid for a rectangular block that meets *all* of the following conditions:
    *   It has height `h` and width `w`.
    *   Its top-left corner (`pr`, `pc`) is *not* the same as the white block's corner (`wr`, `wc`).
    *   It does *not* contain any white (0) pixels.
    *   It is immediately and completely surrounded only by pixels of color `C_border`.
    *   Assume only one such block exists in the grid.
5.  **Copy Pattern:** Extract the `h` x `w` grid segment corresponding to the source pattern block found at (`pr`, `pc`).
6.  **Paste Pattern:** In the output grid (created in step 1), replace the `h` x `w` area starting at (`wr`, `wc`) with the pattern extracted in step 5.
7.  **Return Output:** The modified grid is the result.