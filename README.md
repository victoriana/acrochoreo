# Acrochoreo

A supervisor graph for orchestrating acrobatic move sequences.

The name reflects the core problem: like a choreographer sequencing 
moves, an orchestrator must decide which move executes next, when a 
handoff is safe, and when the routine is performance-ready.

## How It Works
- **Choreographer** (supervisor node): model decides next move
- **Acrobats** (specialist workers): execute individual moves
- **Director** (critic node): judges readiness, triggers retries
- **Showtime check** (termination): model or max iterations decides when to stop

## Related
- [agentic-eval-harness](https://github.com/victoriana/agentic-eval-harness) — evaluation harness scores this system
- [github-actions-reusable-workflow](https://github.com/victoriana/github-actions-reusable-workflow) — CI governance template
