# Vision: Acrochoreo as a Training Journal

*Design north star. This document describes direction, not current capability.
See README.md for what exists today.*

## The core idea

Most AI training tools tell you what you did wrong. This system does the
opposite: it helps you remember what you already knew — across every session,
every revision, every apparatus.

Acrochoreo is being developed toward a **personal choreography journal on
steroids**: versioned sequences, agentic cross-referencing, and human-authored
annotation as a single loop.

## Design principles

1. **The human is the sole authority.** The agent never judges performance,
   never auto-corrects, never dictates. All evaluation comes from human
   annotations. The system's job is recall, coherence, and surfacing — not
   instruction.

2. **Surface, don't command.** Agent output takes the form of prompts to human
   judgment ("you've flagged this transition as unstable four times but kept
   it in rotation — revisit?"), never directives.

3. **Superhuman memory, ordinary judgment.** The system holds everything a
   paper journal can't: every annotation, every sequence version, every
   dependency between moves. It connects patterns across time that no human
   could track unaided.

4. **Coherence over generation.** When one move changes, the supervisor graph
   tracks which downstream elements depend on it, keeping the journal
   internally consistent instead of drifting into contradictions.

## Scope

- **Solo athlete only.** One body, one sequence, one progression arc. No
  troupe logistics, no partner negotiation. The "human in the loop" is the
  athlete.
- **Apparatus-aware specialization path:** floor, pole, aerial (silks, hoop),
  and similar disciplines. Each apparatus has distinct failure modes, risk
  classes, and flow logic; routing and critique specialize per apparatus while
  the general supervisor architecture stays intact.
- **General-first, niche-later.** The current implementation is a general
  supervisor graph. Domain depth (apparatus constraints, per-discipline
  rubrics, progression gating) layers on top without rewriting the core.

## The analogy

Ableton didn't replace musicians with AI — it gave them non-destructive
editing, undo, and version history for creative decisions. Nobody asks why a
DAW needs undo. Acrochoreo applies the same logic to movement composition:
non-destructive sequence revision, full history of choreographic decisions,
and a recall layer over years of training notes.

Movement notation tools exist. Training log apps exist. Music software with
AI agents exists. Nothing combines versioned choreography + agentic
cross-referencing + human-authored annotation in the acrobatics domain. That
is the open territory.

## Where this goes

- Annotation loop: sessions produce human-written notes; the system indexes
  and links them to specific moves and sequence versions.
- Cross-session correlation: recurring annotations surfaced automatically as
  questions, never verdicts.
- Progression tracking: element-level history per athlete (self-reported and
  annotation-derived), enabling the Choreographer to respect prerequisites
  and the Director to ask better questions.
- Evaluation integration: agentic-eval-harness scores *journal quality and
  consistency*, not the athlete.

## Non-goals

- Not an auto-judge of movement quality (no pose estimation verdicts).
- Not a troupe or partner-acro coordination tool.
- Not acro yoga — floor, pole, and aerial apparatus are the domain.
- Not a replacement for coaching judgment; it is infrastructure *for* that
  judgment.
