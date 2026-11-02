# WO-028 | Repeat the two cases that differed on Humble, and say whether the difference is noise
**Phase:** D2 (accepted before D2 starts, by the owner's decision of 2026-11-02)
**Exit tests advanced:** none
**Size:** S
**Prerequisites:** WO-025 accepted.
**Authorization:** the owner's decision of 2026-11-02. Simulation only.
**Files:** `reports/WO-028-humble-differences.md`, `ledgers/runs.jsonl`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
R-06 (Altitude-mode drift) and N-01 (the 5 m climb) differed between Jazzy and Humble in WO-025. Run each 5 times on each stack and state whether the difference is noise.

## Scope
`evals/D1-fault-matrix.json` cases R-06 and N-01, unchanged, 5 runs each on `banshee-sitl` and `banshee-sitl-humble`, one stack at a time. With WO-025's run, Humble has 6 of each; the Jazzy record adds one more.

## Out of scope
Other cases. Changing either case.

## Verification
```bash
make check
```

## Stop conditions
A difference outside the spread of either stack's runs is reported as a difference, not as noise.

## Report
`reports/WO-028-humble-differences.md`
