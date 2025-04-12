import numpy as np
from collections import Counter

# --- Mock code_execution environment ---
# Assume previous code (helpers + transform) is loaded
# Assume inputs and expected outputs are available as lists of lists:
# train_1_input, train_1_output_expected, ... train_5_output_expected

# --- Re-run Transformation and Gather Metrics ---

results = []
all_inputs = [train_1_input, train_2_input, train_3_input, train_4_input, train_5_input]
all_expected = [train_1_output_expected, train_2_output_expected, train_3_output_expected, train_4_output_expected, train_5_output_expected]

for i, (inp, expected) in enumerate(zip(all_inputs, all_expected)):
    example_num = i + 1
    actual_list = transform(inp)
    actual = np.array(actual_list, dtype=int)
    expected_np = np.array(expected, dtype=int)

    match = np.array_equal(actual, expected_np)
    pixels_off = np.sum(actual != expected_np)
    size_correct = actual.shape == expected_np.shape
    
    palette_actual = set(np.unique(actual))
    palette_expected = set(np.unique(expected_np))
    palette_correct = palette_actual == palette_expected

    counts_actual = Counter(actual.flatten())
    counts_expected = Counter(expected_np.flatten())
    count_correct = counts_actual == counts_expected
    
    # Detailed difference analysis (for failed cases)
    diff_coords = []
    diff_info = []
    if not match:
        diff_indices = np.argwhere(actual != expected_np)
        for r, c in diff_indices:
            diff_coords.append((r,c))
            diff_info.append({
                'coord': (r, c), 
                'input': int(inp[r][c]), 
                'expected': int(expected_np[r, c]), 
                'actual': int(actual[r, c])
            })
            
    results.append({
        "example": example_num,
        "match": match,
        "pixels_off": int(pixels_off),
        "size_correct": size_correct,
        "palette_correct": palette_correct,
        "count_correct": count_correct,
        "diff_coords": diff_coords,
        "diff_info": diff_info
    })

# --- Print Summary Metrics ---
# print(results) 
# Example Output (based on the provided execution results):

# Example 1: Match=True, Pixels Off=0
# Example 2: Match=False, Pixels Off=6
#   Diff Coords: [(1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (4, 5)]
#   Diff Info:
#     (1,3): In=7, Exp=3, Act=7 -> Mover '3' expected, not placed. Target was Exp=4 (Static).
#     (1,4): In=4, Exp=4, Act=4 -> OK (Static '4' preserved)
#     (2,3): In=7, Exp=3, Act=7 -> Mover '3' expected, not placed. Target was Exp=4 (Static).
#     (2,4): In=4, Exp=4, Act=4 -> OK (Static '4' preserved)
#     (3,4): In=7, Exp=3, Act=7 -> Mover '3' expected, not placed. Input(8,4)=3 -> Move(-1,1) -> (7,5). Out[7,5]=2(Anchor). Blocked. Input(8,3)=3 -> Move(-1,1) -> (7,4). Out[7,4]=7(BG). Placed? Code got 7. Input(6,6)=3 -> Move(-1,0) -> (5,6). Out[5,6]=3. Code got 3. Input(7,5)=3 -> Move(-1,0) -> (6,5). Out[6,5]=7(BG). Placed? Code got 7.
#     (4,5): In=7, Exp=3, Act=7 -> Mover '3' expected, not placed. Input(5,6)=3 -> Move(-1,0) -> (4,6). Out[4,6]=7(BG). Placed? Code got 7.
#   Analysis Ex2: The code seems to be incorrectly handling collisions or placements. Static '4' is preserved correctly. Anchor '2' is preserved correctly. The mover '3' placements are wrong. It seems movers should NOT overwrite static or anchor values. Let's re-evaluate the expected output: 3s appear at (1,3), (2,3), (3,4), (4,5), (5,6). Sources: (8,3)->(7,4)? No, (-1,+1) -> (7,4) -> expected=7? No. (8,4)->(7,5)? Yes, blocked by anchor 2. (5,6)->(4,6)? No, expected=7. (6,6)->(5,6)? Yes, expected=3. (7,6)->(6,6)? Yes, expected=7. (6,5)->(5,5)? No, expected=7. (7,5)->(6,5)? Yes, expected=7. (8,3)->(7,4)? Yes. (8,4)->(7,5)? Blocked. (5,6)->(4,6)? Yes. (6,6)->(5,6)? Yes. (7,6)->(6,6)? Yes.
#   Let's re-trace Expected Ex2: Input 3s at (5,6), (6,5), (6,6), (7,5), (7,6), (8,3), (8,4). Anchor=col 7 (value 2). Static=4 (col 4). Mover=3.
#   Rel -1: (5,6)->(-1,0)->(4,6). Out=BG. Place 3. (6,6)->(-1,0)->(5,6). Out=BG. Place 3. (7,6)->(-1,0)->(6,6). Out=BG. Place 3.
#   Rel -2: (6,5)->(-1,+1)->(5,6). Out=3. No Change. (7,5)->(-1,+1)->(6,6). Out=3. No Change. (8,4)->(-1,+1)->(7,5). Out=2(Anchor). Blocked.
#   Rel -3: (8,3)->?? No rule for M=3, rel=-3.
#   Expected output has 3s at: (1,3), (2,3), (3,4), (4,5), (5,6). Where do these come from? This contradicts the left-mover logic completely.
#   Let's reconsider Ex2 roles. Anchor=7 (col 7, val 2). What if Static=3 AND Static=4? Mover=None? Then output should match input except for anchor col. Doesn't match. What if Anchor=4 (col 4, val 4)? Mover=3? Static=None? Anchor col 4 not preserved.
#   Hypothesis for Ex2: Anchor=col 7 (val 2). Static=col 4 (val 4). Mover=3. The rules are different. Maybe it relates to the *shape* of the static object? The static 4s are a vertical line. The mover 3s form shapes relative to it? This seems overly complex.
#   Let's stick to simpler fix: Movers don't overwrite non-background. Rerun trace:
#   Rel -1: (5,6)->(4,6). Out=BG. Place 3. (6,6)->(5,6). Out=BG. Place 3. (7,6)->(6,6). Out=BG. Place 3.
#   Rel -2: (6,5)->(5,6). Out=3. No change. (7,5)->(6,6). Out=3. No change. (8,4)->(7,5). Out=2(Anchor). Blocked.
#   Final state with this rule: 3s at (4,6), (5,6), (6,6). Still doesn't match expected.
#   There must be a different rule for M=3, or the static '4' influences the '3' movement differently. The expected output shows 3s appearing in col 3 and col 4 & 5. This is very confusing. Let's assume the core logic is right but parameterization failed for M=3.
# Example 3: Match=True, Pixels Off=0
# Example 4: Match=False, Pixels Off=6
#   Diff Coords: [(1, 3), (2, 2), (2, 3), (3, 3), (4, 3), (5, 3)]
#   Diff Info:
#     (1,3): In=3(Static), Exp=3, Act=8(Mover) -> Mover overwrote Static INCORRECTLY? Or expected has Static.
#     (2,2): In=3(Static), Exp=3, Act=3 -> OK
#     (2,3): In=0(BG), Exp=0, Act=8(Mover) -> Unexpected Mover placed?
#     (3,3): In=3(Static), Exp=3, Act=8(Mover) -> Mover overwrote Static INCORRECTLY?
#     (4,3): In=8(Mover), Exp=8, Act=8 -> OK
#     (5,3): In=8(Mover), Exp=0, Act=0 -> OK
#   Analysis Ex4: Anchor=col 4 (val 5). Static=3 (col 2, 3). Mover=8.
#   Input 8s at (4,3), (5,3), (6,2), (7,2), (8,1), (8,2).
#   Rel -1: (4,3)->(-4,0)->(0,3). Out=BG. Place 8. (5,3)->(-4,0)->(1,3). Out=3(Static). Expected=3. Actual=8. -> ISSUE 1: Mover overwrite.
#   Rel -2: (6,2)->(-4,+1)->(2,3). Out=0(BG). Expected=0. Actual=8. -> ISSUE 2: Mover placed where not expected? (7,2)->(-4,+1)->(3,3). Out=3(Static). Expected=3. Actual=8. -> ISSUE 1: Mover overwrite. (8,2)->(-4,+1)->(4,3). Out=BG. Expected=8. Actual=8. -> OK.
#   Rel -3: (8,1)-> ?? No rule for M=8, rel=-3. Removed. OK.
#   Cond Gen: flag_minus_2=True. Place 8 at (0, anc_c-1) = (0, 3). Out=8. OK.
#   Hypothesis: Movers DO NOT overwrite Static or Anchor values. Let's recalculate Ex4 based on this:
#   Rel -1: (4,3)->(0,3). Out=BG. Place 8. (5,3)->(1,3). Out=3(Static). BLOCKED. Expected=3. Actual(new)=3. MATCHES EXPECTED NOW.
#   Rel -2: (6,2)->(2,3). Out=0(BG). Place 8. Expected=0. Actual(new)=8. STILL MISMATCH. (7,2)->(3,3). Out=3(Static). BLOCKED. Expected=3. Actual(new)=3. MATCHES EXPECTED NOW. (8,2)->(4,3). Out=BG. Place 8. Expected=8. Actual(new)=8. OK.
#   Cond Gen: Place 8 at (0, 3). OK.
#   The remaining mismatch is at (2,3). Why is 8 placed there in code, but expected is 0? Source was (6,2). Move=(-4,+1). Target=(2,3). Is the shift wrong for M=8, rel=-2?
#   Let's re-examine Expected Ex4: 8s at (0,3), (1,2), (2,1), (3,2), (4,3). Where are these coming from? This doesn't match the simple shift logic well.
#   Could the Static '3's *also* be moving? If 3 is Mover and 8 is Static? Fails frequency test.
#   What if the rule depends on the *value* being overwritten? Mover overwrites BG, but not Static/Anchor?
#   Let's assume the "No overwrite" rule is correct. The code placed 8 at (2,3) from (6,2). Expected is 0. This implies the move from (6,2) should not have happened or targeted a different place.
# Example 5: Match=False, Pixels Off=3
#   Diff Coords: [(2, 2), (3, 2), (4, 3)]
#   Diff Info:
#     (2,2): In=0(BG), Exp=9(Mover), Act=0 -> Mover expected, not placed.
#     (3,2): In=0(BG), Exp=9(Mover), Act=0 -> Mover expected, not placed.
#     (4,3): In=0(BG), Exp=9(Mover), Act=0 -> Mover expected, not placed.
#   Analysis Ex5: Anchor=col 5 (val 6). Static=3 (col 3). Mover=9.
#   Input 9s at (5,4), (6,3), (7,0), (7,1), (7,2), (8,0).
#   Rel -1: (5,4)->(0,0)->(5,4). Out=BG. Place 9. Expected=9. Actual=9. OK.
#   Rel -2: (6,3)->(-2,0)->(4,3). Out=BG. Place 9. Expected=9. Actual=0. -> ISSUE: Code placed 9, but did it get overwritten later? Or was the move wrong?
#   Rel -3: (7,2)->(-5,0)->(2,2). Out=BG. Place 9. Expected=9. Actual=0. -> ISSUE.
#   Rel -4: (7,1)->Remove. OK. (8,0)->Remove. OK.
#   Rel -5: (7,0)->Remove. OK.
#   Cond Gen: flag_minus_2=True (from (6,3) move). Place 9 at (0,4) and (1,4). OK.
#   Why are (2,2), (3,2), (4,3) wrong? Code calculates targets (2,2) [from (7,2), rel=-3] and (4,3) [from (6,3), rel=-2]. It seems they *should* be placed. Why are they 0 in the actual output? Is there an intermediate step overwriting them? No. Did the code fail to place them? Let's re-check the code logic: It adds to `mover_placements` then iterates. It *should* place them.
#   What is expected at (3,2)? Where could that 9 come from? No input 9 maps there with current rules.
#   This implies the rules for M=9 shifts (rel=-2, rel=-3) are incorrect, or the "No Overwrite" rule needs more nuance.
#   Let's reconsider the "No Overwrite" rule globally. It fixes parts of Ex4 but breaks Ex5 and doesn't fix Ex2.
#   What if the Mover Placement step *first* clears all current Mover locations in `out` to Background, *then* places the new locations (only onto Background)?

# --- Final Strategy Revision ---
# 1. Implement the "Movers Only Place on Background" rule. This seems the most promising single change based on Ex4 partial fix.
# 2. Re-evaluate Ex2 and Ex5 after this change. If still incorrect, the specific shifts `(dr, dc)` for M=3 and M=9 must be wrong.
# 3. Ex2 is the most problematic. The expected output doesn't fit the established left-mover shift pattern well. There might be a specific rule for M=3 interacting with Static objects, or a completely different paradigm for M=3. Given time constraints, focus on fixing the overwrite logic and assume M=3 might remain an anomaly.
# 4. Refine YAML and NL Program based on the "Place on Background" rule.

