# WO-029 — The D1 simulation data, published for vishwaroop

**Status:** passed. Four completed, immutable exports. The split plan was frozen before either set was published. 99 variation attempts ran: 86 succeeded, 12 failed and are kept, and 1 is incomplete.
**Date:** 2026-11-07 · **Author:** claude-code-banshee · **Work order:** WO-029 · **Phase:** D2 (not started); simulation only
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Everything here is **measured** in local SITL on `gz_x500`. There was no hardware and no spending. Nothing was written into vishwaroop.

## 1. The exports (measured)
All four are under `data/exports/`, which is now gitignored, since the bytes are not tracked.

| Export | Kind | Manifest SHA-256 (= `COMPLETE`) | Files |
|---|---|---|---|
| `data/exports/banshee-d1-sim-episodes` | episodes | `d7bc0545852e8a3549790a956782723240faf6f4aa6496ab55ad15367d711fc0` | 3784 |
| `data/exports/banshee-d1-sim-ulogs` | raw ULogs | `9e8c1fb2053f8a47289b4508789c1faad9649632f2a15bec7d97f09ad9d12f18` | 473 |
| `data/exports/banshee-d1-variation-v1-episodes` | episodes | `383dfea07505aa2db716c4c45a03eb31c6014f75bb603ddfd0a58f8096414cfe` | 784 |
| `data/exports/banshee-d1-variation-v1-ulogs` | raw ULogs | `0b76d7b87bb78ab1b5fc94d3ac66af2c0e0389b4b6f0090a72f6b9961af940c0` | 98 |

**Every manifest records:**
- the contract (`ironclad contracts v1`, `schema_version` 1.0.0);
- a SHA-256 for each file;
- the producer and the source commit (`68ec0bc`);
- the rights: "Owner-private. All rights reserved. For use within the owner's projects only.";
- `simulation_only: true`;
- the split plan's path and SHA-256 (`evals/D1-split-plan.json`, `73205f1b…`);
- the transformation (only the `split` block of `episode.json` changes);
- one entry per episode, with its stack, family ID, split, run ID and the SHA-256 of the source episode.

**ULog exports:** each ULog sits under its run ID, and every episode has one. The ULog exports are separate from the episode exports and are read-only.

**Publication protocol:** each export was built in a temporary directory, hashed, verified, renamed into place and verified again. `COMPLETE` was written last, holding the manifest's SHA-256, and then the whole tree was made read-only.

**Independent re-check after publication:**
- every listed hash matches;
- no files are unlisted and none are missing;
- no file is writable;
- every entry's split matches the frozen plan;
- no family appears in two partitions.

## 2. Episodes by stack and split (measured)
| Export | Jazzy train | Jazzy held-out | Humble train | Humble held-out | Total | Succeeded / failed |
|---|---|---|---|---|---|---|
| D1 (`data/derived/d1*`) | 274 | 132 | 45 | 22 | 473 | 413 / 60 |
| Variation set | 76 | 22 | — | — | 98 | 86 / 12 |

**Partition mapping:** held-out is the contract partition `dev`, and train is `train`. Held-out is not `sealed`, because the sealed partition must stay out of agents' reach (DATA_POLICY §5).

## 3. Families per partition (measured)
A family is route × wind × fault family. The assignment logic is in `src/banshee/publish/splits.py`, and the frozen plan is in `evals/D1-split-plan.json`: 43 families, salt `banshee-d1-split-v1`, held-out fraction 0.25, with at least 2 variation families and 2 fault families held out.

| | D1 export | Variation export | Both, distinct |
|---|---|---|---|
| Train | 26 | 7 | 33 |
| Held-out | 9 | 2 | 10 |

One family, `d1-square-v1|calm|nominal`, appears in both exports, and in both it is held out.

**The held-out families are:**
- **2 nominal from the variation set:**
  - `d1-line-v1|wind-2.5|nominal`: 11 variation episodes;
  - `d1-square-v1|calm|nominal`: 82 D1 and 11 variation episodes.
- **8 fault families:**
  - `d1-square-v1|calm|G` (5)
  - `wp-016773cf1d|calm|C` (8)
  - `wp-65dc8ff298|calm|V` (10)
  - `wp-748e2c871c|calm|G` (8)
  - `wp-8c8f13ccc2|calm|E` (5)
  - `wp-9e7b430903|calm|R` (20)
  - `wp-a7a9fc7451|calm|G` (5)
  - `wp-e1ebc8169e|wind-5.4|W` (11)

**Train coverage:** train still holds fault families B, C, E, G, H, K, L, P, PL, R, S, T and V, plus nominal.

**Consequence of the minimum rule:** the rule pulled `d1-square-v1|calm|nominal` into held-out, so all 82 nominal D1 square-route episodes are held out. Train's nominal data comes from the other route and wind cells of the variation set and from the N-01 hover family.

**Split audit:** the contract's split audit passed on each export, with `session_group_id`, `policy_run_group_id` and `scene_group_id` (the family) as hold-out axes. It also passed on both episode exports together (§5).

## 4. The variation set (measured)
**Frozen before running:** routes, winds and seeds were committed in `evals/D1-variation-set.json` and merged in `68ec0bc` before attempt 1.
- **Routes:** `d1-square-v1`, `d1-line-v1` and `d1-climb-v1`.
- **Winds:** calm (`default`), 2.5 m/s (`windy_2p5`) and 5.0 m/s (`windy_5`).
- **Attempts:** 11 per cell, run in round-robin order.

**Seed and world check:** all 99 runs' `px4.log` files show the frozen seed (`ogre2 --seed N`) and the planned Gazebo world.

| Route \ wind | calm | 2.5 m/s | 5.0 m/s |
|---|---|---|---|
| square | 10 ok, 1 failed | 9 ok, 2 failed | 9 ok, 2 failed |
| line | 10 ok, 1 failed | 8 ok, 3 failed | 8 ok, 2 failed, **1 incomplete** |
| climb | 11 ok | 11 ok | 10 ok, 1 failed |

**Incomplete attempts, reported separately:**
- One attempt: index 5, line route, 5.0 m/s wind, run `20261107T070512Z_896c1085`.
- The VM run completed, but the contract validator refused the episode: one of 980 observations (step 677) has `capture_t_ns` = −1794034244281862023. That is roughly the simulation time minus the Unix wall-clock time in ns, so a timestamp from the wrong clock reached the record.
- The run and its ULog are kept in `runs/`. It is in neither export, because the work order publishes completed episodes.
- The cause is **not established**. It is a follow-up for the recorder.

**Why every unsuccessful attempt stopped:**
- All 13 (the 12 failures and the incomplete one) ended with the freshness gate latched to Land.
- The observation ages in their last steps were about 90–230 ms, against the 100 ms bound.
- 2 of the 12 failures had reached all waypoints first.
- This is the same early gate trip as WO-022 and WO-028. **Here it hit 13 of 99 nominal attempts.** Its cause is still not established, and it still blocks the first arm (ET-D3-4).

## 5. Verification
- `make check` passes.
- Each export was verified before `COMPLETE` was written and again after the rename.
- The re-check in §1 was run separately after publication.
- The split audit was run on the 571 episodes of both exports together.
- **Summaries:**
  - per-attempt: `runs/variation-d1-v1/attempts.jsonl`;
  - per run: `ledgers/runs.jsonl`.
- The SITL VMs are stopped.

## 6. Files
`.gitignore` (`data/exports/`), this report, `CHANGES.md`, `ledgers/runs.jsonl` and `ledgers/STATUS.jsonl`. The code, the plan and the frozen evals were merged in PR #34.
