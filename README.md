# Acrochoreo

A YAML-based version control system for acrobatic choreography.

## The Problem
Acrobatic sequences are complex interplays of individual moves (e.g., `move_pirouette_left_to_right_stage`, `move_right_leg_kick`). When you change one move, you often have to redraw or memorize the entire sequence from scratch. This is error-prone and inefficient.

## The Solution
`acrochoreo` treats each move as a discrete YAML file (prefixed with `move_`) and each sequence as a composition of those files (prefixed with `choreography_`). It allows you to:
- **Compose:** Build sequences from individual move files (`move_pirouette.yaml`, `move_right_leg_kick.yaml`).
- **Track:** Version-control the *sequence* itself, not just the moves.
- **Diff:** See exactly what changed between `v1` and `v2` of a sequence. No more redrawing from memory.

## Example Structure
```yaml
# choreographies/choreography_basic_v1.yaml
moves:
  - move_id: move_pirouette_left_to_right_stage
  - move_id: move_right_leg_kick
  - move_id: move_fold_in
