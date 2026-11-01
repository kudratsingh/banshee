# WO-002 — D1 SITL: pinned launch, offboard velocity mission, independent outcome, contract export

**Status:** in progress. No exit test has run. Later results are appended below, dated.
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-002 · **Phase:** D1 · **Protocol version:** `evals/D1-exit-tests.json`, sha256 `1f4900194371c9124b3aa0e6ef29c438d947fe931fc513baba698948ae758180` when frozen
**Program link:** PROGRAM §5.1, §6 → banshee D1

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## Incident, 2026-10-31: setup filled the owner's disk
**Impact.** The Mac's disk filled, and the Mac then quit unexpectedly at about 21:45 PDT. The link between the two is likely but not proven: no shutdown cause was found in the system log. All four repositories are intact and the Mac has about 90 GB free (owner's check). The other agents' work was not affected (owner). This repository's ledgers parse and `git fsck` is clean (measured). Setup logs and scratch files were lost in the reboot's `/private/tmp` cleanup, including the two logs that were the direct evidence of this incident. The full account, with paths, is in `ledgers/corrections.jsonl`. No run record was lost, because no run had happened.

**Cause.** The fault was the agent's.
- `provision.sh` ran `DONT_RUN=1 make px4_sitl gz_x500`, expecting a build. PX4 appears to have started anyway. With no terminal, its `pxh>` prompt repeated without end. The cause of the prompt loop is read from what the log showed before the crash; the log itself is gone.
- The agent sent that output to a log file on the Mac, with no size cap and no time limit, which `AGENTS.md §8.8` requires. The log reached at least 34,249,662,532 bytes (measured, shortly before the disk filled).
- A status check shortly before saw the repeating prompt at the end of the log, and did not look at its size.

**Fix.**
| Bound | Where | Evidence |
|---|---|---|
| Build only: `make px4_sitl_default` | `provision.sh` | the build completed in the partial rerun, and PX4 did not start (measured) |
| 200 MB log cap, which stops the run | `banshee.sitl.bounded` on the host; `head -c` in the VM | `tests/test_sitl_bounded.py`: a chatty process, and a prompt loop like this one, each stop at the cap, and so do their children (measured) |
| 3-hour limit | `banshee.sitl.bounded`; `timeout` in the VM | same test file (measured, with a short limit) |
| No stdin | both | same test file (measured) |
| Refuses to start under 20 GB free, on the host or in the VM | `banshee.sitl.bounded` | same test file for the refusal; `run_provision.sh` passes `--vm` |
| VM disk fixed at 60 GiB | `banshee-sitl.yaml` | read back from the VM on restart |

The VM disk cap would not have stopped this incident, because the log was on the host. The log cap is what prevents a repeat.

**Disclosure.** After the crash the agent reran setup with the first three bounds. The owner then asked for this work to be done before any rerun, and the agent stopped that run, which had reached the agent build.

**Retro.** Check size as well as content when checking a log. Treat "will only build" as something to confirm, and keep bounds on regardless.

## Results
Not run. Later entries follow.
