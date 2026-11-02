# WO-024 | Migrate the Jetson to JetPack 7 (placeholder)
**Phase:** D7 (placeholder, not scheduled; due before Humble's support ends in May 2027, whatever phase is current then)
**Exit tests advanced:** none
**Size:** stub; expand when it becomes next
**Prerequisites:** Holybro supports JetPack 7 on the Pixhawk Jetson Baseboard, which it did not on 2026-11-01 [D63].
**Authorization:** the owner's decision of 2026-11-02 asks for this placeholder. Any flashing of the Jetson needs its own dated owner approval.
**Files:** written when expanded.

Serves `PROGRAM §5.1`.

## Objective
Move the Jetson from JetPack 6.2.2, Ubuntu 22.04, ROS 2 Humble and Isaac ROS 3.2 to JetPack 7, Ubuntu 24.04, ROS 2 Jazzy and a current Isaac ROS, before Humble's support ends in May 2027.

## Scope
Written when expanded. Minimum: the baseboard's support confirmed from Holybro; the D1 regression and the D2 measurements re-run on the new stack and compared.

## Out of scope
Everything until Holybro supports JetPack 7 on this board.

## Verification
Written when expanded.

## Stop conditions
Holybro does not support it: stay on JetPack 6.2.2 and report the date the support ends.

## Report
`reports/WO-024-jetpack-7-migration.md`
