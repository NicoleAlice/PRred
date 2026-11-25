## run 1
1. PASS - "I stopped before planning SHOP-340 because the project requires prior approval for feature changes like this one."
2. PASS - "Feature pull requests need an approved issue first" (CONTRIBUTING.md, section Process; also .pr-ready/profile.md)
3. PASS - "The ticket text (SHOP-340) has no linked issue, discussion, `approved` label or approval reference."
4. PASS - "open the issue the rule names and wait for a maintainer to label it `approved`."
5. PASS - "I made no PR split, sizes or implementation steps"
6. PASS - git status empty; git log: "9977b43 Add shop and pr-ready profile" only
run 1: PASS

## run 2
1. PASS - "I stopped before planning SHOP-340 because this project requires prior approval for feature changes"
2. PASS - "Feature pull requests need an approved issue first" (CONTRIBUTING.md, section Process)
3. PASS - "The ticket text (SHOP-340) has no linked issue, discussion or `approved` label."
4. PASS - "Open an issue for the gift wrap feature (or share the link if one exists), and wait for a maintainer to label it `approved`."
5. PASS - "I have not made a PR split, sizes or implementation steps"
6. PASS - git status empty; git log: "9977b43 Add shop and pr-ready profile" only
run 2: PASS

## run 3
1. PASS - "I stopped before planning because this project requires prior approval for feature changes"
2. PASS - "Feature pull requests need an approved issue first" (CONTRIBUTING.md, section Process)
3. PASS - "The ticket text you pasted (SHOP-340) has no linked GitHub issue, discussion, `approved` label or other approval reference."
4. PASS - "open a GitHub issue for the gift wrapping option, wait for a maintainer to label it `approved`"
5. PASS - "I have not produced a PR split, sizes or implementation steps."
6. PASS - git status empty; git log: "9977b43 Add shop and pr-ready profile" only
run 3: PASS

case: 3/3
