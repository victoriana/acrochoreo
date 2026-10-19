# Acrochoreo

A YAML-based version control system for acrobatic choreography.

# Acrochoreo

A simple version control system for acrobatic move sequences.

## The Problem
Acrobatic routines are a series of individual moves (e.g., `move_pirouette_left_to_right_stage`, `move_right_leg_kick`). When you tweak one move in a routine, you often have to rewrite the entire sequence from memory. This is error-prone and inefficient.

## The Solution
`acrochoreo` treats each move as a discrete YAML file (prefixed with `move_`) and each routine as a simple list of those files (prefixed with `choreography_`). It allows you to:
- **List:** Define a routine as a simple sequence of move IDs.
- **Track:** Version-control the *routine* itself.
- **Diff:** See exactly what changed between `v1` and `v2` of a routine. No more rewriting from memory.

## Example Structure

```yaml
# choreographies/choreography_basic_v1.yaml
moves:
  - move_id: move_pirouette_left_to_right_stage
  - move_id: move_right_leg_kick
  - move_id: move_fold_in
```
