# WO-023 — The owner's decisions of 2026-11-02 recorded

**Status:** passed, pending review; one line of the final list has an unconfirmed gauge and price
**Date:** 2026-11-02 · **Author:** claude-code-banshee · **Work order:** WO-023 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Nothing ran here; this work order records decisions and prices.

## 1. What was done
| Decision | Where it is now |
|---|---|
| D3 temporary rule: 10 m, 4 m/s, 160 m; later stages re-derive from D3 data with the ARK Flow MR as backup velocity | `evals/D3-temporary-rule-2026-11-02.json`, frozen; envelope rows for height, wind and bystanders |
| Crew 85 m upwind | the same file; envelope's crew row |
| ET-D2-4: software cut accepted; SIGSTOP and Jetson-reboot cases | `config/phases.json`, `docs/PHASES.md`, `evals/D2-exit-tests.json` (now sha256 `3bc5eb53ed6af9e02864204f97fb2c734aa659cf0ca603ae971f9415525e1340`) |
| Gate trips explained before any armed flight | `evals/D2-exit-tests.json`, a new `blocking` list, separate from the reported items |
| JetPack 6.2.2, Humble, Isaac ROS 3.2 | ADR-0007; envelope's compute row; `docs/CONTEXT_AND_DECISIONS.md` |
| JetPack 7 placeholder | `work_orders/WO-024-jetpack-7-migration.md` |
| D1 on Humble | D1 ran on Jazzy (Ubuntu 24.04 in `config/stack-lock.resolved.json`), so `work_orders/WO-025-d1-regression-on-humble.md` |
| Tier B defined | ADR-0007; `docs/CONTEXT_AND_DECISIONS.md`; the final list |
| Buy list | `docs/BUY_LIST-FINAL-2026-11-02.md`: planning total $7,203.89 |
Each decision is in `ledgers/approvals.jsonl` with the owner's words.

## 2. Choices I made inside the decisions
- **ET-D2-4's new cases use the same trials and threshold as the link cut,** 3/3 each. The report must also state what the node sends after SIGCONT and what it does when the Jetson starts again. Those are reported, not thresholded, because the owner did not set a threshold for them.
- **The gate trips are a blocking item,** not one of the reported items whose note says none moves a pass to a fail.
- **The D3 rule supersedes, for D3 only,** the radius and crew in `evals/D3-standoffs-x650.json` and the envelope's height and wind table. Both stay as the record and as input to the re-derivation.
- **WO-024 is filed under D7,** because the consistency check needs a known phase; it is due before May 2027 whatever phase is current.

## 3. Buy list
- **LiPo safe:** BAT-SAFE XXL E-Bike Edition, 777 Wh combined against 666 Wh for three packs, $206.99 on sale, fulfilled from Texas. No US box in the hobby range was found rated for three packs: the Bat-Safe XL takes two and appears discontinued; the two 666 Wh European boxes' pages did not load.
- **Adapter leads: not fully read.** Gens Ace XT60 male to EC5 female, $4.99 each, from a search result; the seller's page returned HTTP 429 four times. 12 AWG is not confirmed, and connector genders are named inconsistently between sellers, so the list asks the owner to check the mating before ordering.
- **Removed:** NVMe and spare props. The props move to D3 with another source.

## 4. Verification
`make check` passes. Independent review: §6.

## 6. Independent review
Read-only, from the diff and the owner's words. It found: ET-D2-4's new cases had no start time for the bound; the gate-trip item sat under a note saying it moves nothing, and nothing checked stopped an arm; the three D2 files disagreed on the reported items; stale D3 text in the envelope and `evals/D3-standoffs-x650.json`; the shear condition behind the 4 m/s limit left out of the rule; two ledger readings beyond the owner's words; buy-list notes dropped from the earlier list; and smaller items. All are fixed. The gate item is now checked in ET-D3-4, before the first arm, which changes a D3 statement before any D3 result, by the owner's decision. The ledger is append-only, so its two readings are corrected by a new record. **There was no second pass on these fixes.**

**Question for the owner.** The new ET-D2-4 cases test that PX4 sees the loss. What the node sends after SIGCONT or on restart is reported, not thresholded. AGENTS §13.4 says expired setpoints are never sent; a threshold of "after SIGCONT and after restart, no setpoint older than the 200 ms bound is sent; 3/3" would test that. I have not added it, because you did not set it.

## 5. Retro
Shopify sellers rate-limit repeated reads; one read per seller per minute, and a search snippet is not a page read.
