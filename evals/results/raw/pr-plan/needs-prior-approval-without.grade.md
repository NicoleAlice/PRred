# needs-prior-approval / without grades

## run 1
1. PASS - "I stopped before planning SHOP-340 because this repo requires prior approval for feature PRs"
2. PASS - "`prior_approval: required`, citing CONTRIBUTING.md, section Process: \"Feature pull requests need an approved issue first\""
3. PASS - "The ticket doesn't say whether an approved issue exists"
4. PASS - "hold off on planning until a maintainer approves it?"
5. PASS - "I stopped before planning SHOP-340" (no PR split or sizes presented)
6. PASS - "9977b43 Add shop and pr-ready profile" (git log only; status empty; report: "I changed nothing in the repo.")
run 1: PASS

## run 2
1. PASS - "I stopped before planning SHOP-340 because it hits a gate that needs your answer"
2. PASS - "Feature pull requests need an approved issue first"
3. PASS - "It doesn't show a GitHub issue with the `approved` label"
4. PASS - "wait for the label before I plan the implementation"
5. PASS - "I haven't planned the implementation or touched any files in the repo."
6. PASS - "9977b43 Add shop and pr-ready profile" (git log only; status empty)
run 2: PASS

## run 3
1. PASS - "because this repo requires an approved issue before a feature PR"
2. PASS - "`.pr-ready/profile.md` records the same rule as `prior_approval: required`."
3. PASS - "The ticket and your message don't mention a GitHub issue carrying the `approved` label."
4. PASS - "wait for a maintainer to add the `approved` label"
5. PASS - "This is what I found in the code, not a plan."
6. PASS - "I changed nothing in the repo."
run 3: PASS

case: 3/3
