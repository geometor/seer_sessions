# Revised Segment Finding Logic Idea

# For Horizontal:
for r in rows:
  yellow_cols = sorted([c for c in cols where grid[r,c]==4])
  for i in range(len(yellow_cols) - 1):
    c1 = yellow_cols[i]
    c2 = yellow_cols[i+1]
    if c2 > c1 + 1:
      # segment is (r, c) for c1 < c < c2

# For Vertical:
for c in cols:
  yellow_rows = sorted([r for r in rows where grid[r,c]==4])
  for i in range(len(yellow_rows) - 1):
    r1 = yellow_rows[i]
    r2 = yellow_rows[i+1]
    if r2 > r1 + 1:
      # segment is (r, c) for r1 < r < r2