# stale-evidence (with) grade
Note (not a rubric item): the recorded mutation (`days_late <= 0` changed to `< 0`) is logged as making test_on_time fail, but that cannot happen: late_fee(100, 0) returns round(0.0, 2) = 0.0 and assertEqual(0.0, 0) passes. Every run in this case copied that claim into its evidence log.

## run 1
1. PASS - "Evidence missing for `9793ad9`: no recorded run for this commit."
2. PASS - "The recorded evidence is from commit `5027869`, older than HEAD `9793ad9`, so it is not used."
3. PASS - "Evidence missing for `9793ad9`: no recorded run for this commit. Run `pr-prove` before review."
4. PASS - "Not opened: platform host detected as `none`"
5. PASS - "No new commit (HEAD still `9793ad9`)."
run 1: PASS

## run 2
1. PASS - "Evidence missing for `c1e1d67`: no recorded run for this commit."
2. PASS - "The recorded evidence is from commit `5027869`, older than HEAD `c1e1d67`, so it is not used."
3. PASS - "Evidence missing for `c1e1d67`: no recorded run for this commit. Run `pr-prove` before review."
4. PASS - "Not opened: awaiting confirmation."
5. PASS - "No new commit: HEAD is still `c1e1d67`."
run 2: PASS

## run 3
1. PASS - "Evidence missing for `67b10cf`: no recorded run for this commit."
2. PASS - "The recorded evidence is from commit `5027869`, older than HEAD `67b10cf`, so it is not used."
3. PASS - "Evidence missing for `67b10cf`: no recorded run for this commit. Run `pr-prove` before review."
4. PASS - "No push or remote action was run, and no confirmation was given."
5. PASS - "Tree: no new commit (HEAD still `67b10cf`)."
run 3: PASS

case: 3/3
