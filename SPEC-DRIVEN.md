# Spec-Driven Development

How First Principle #1 — *"code is not stored in source control (other than as a cache); the spec is THE source of truth"* — is operationalized in this project.

The literal claim ("never version code, always regenerate") is not reliably feasible today and conflicts with the MVP goal of *boringly stable*. This document keeps the **spirit** — intent lives in prose, code is subordinate and disposable — while staying operable now.

## The core idea

We don't make the code generator deterministic and trust it. We make the **behavioral contract** durable and **verify** generated code against it. Determinism is optional; verification is the load-bearing part.

## Layers, by durability

| Layer | Who authors | Form | In git as |
|---|---|---|---|
| `spec` (this repo's docs) | **human** | prose | canonical source of truth |
| `test-specs` | **human** | prose criteria **+ golden examples** | canonical contract |
| generated test code | LLM, then frozen | code | committed **cache** |
| generated implementation | LLM | code | committed **cache** |
| runtime data (the answers) | runtime | SQLite | **durable, sacred — never regenerated** |

- **Canonical** = the human maintains it; intent lives here.
- **Cache** = generated, committed for diffing / review / rollback / reproducible deploys, but discardable and regenerable. We keep it in git for operational safety, not because it's the source of truth.
- **Sacred** = the user's answers. Never a cache. Schema changes are migrations, never regenerations.

## The rules

1. **Intent never lives only in code.** If behavior changes, the `spec` or a `test-spec` changes *first*. Code is always downstream. A hand-edit to code that diverges from the spec is a bug in the process.

2. **Tests are prose; test code is generated.** We do not maintain test code. We maintain `test-specs/` — natural-language behavioral criteria plus concrete golden examples. Test code is generated from them.

3. **Golden examples are mandatory and human-authored.** Every behavioral area carries at least one concrete `input → expected output` pair, written by a human. These pin ambiguity that prose alone cannot.
   - Not: *"streaks should be computed correctly."*
   - But: *"answers finalized on Mon, Tue, Thu → current streak = 1, total days = 3."*

4. **Tests-first, then freeze (independence).** Generate test code from the test-specs and freeze it *before* generating the implementation. The implementation generator must never edit the tests to make them pass. This breaks the shared-oracle blind spot where one model misreads ambiguous prose the same way in both test and code.

5. **Generate-then-freeze, not regenerate-per-run.** Once generated, code is ordinary code — it runs deterministically on a CPU. Commit it as a cache and run it normally in CI. Regenerate only when the prose above it changes. This is why we don't need a deterministic generator.

6. **Sacred data is out of the loop.** Regeneration touches code, never the answers DB. Schema evolves only through reviewed migrations.

## The verify loop

```
edit prose (spec / test-spec)
        │
        ▼
regenerate test code  ──►  freeze (commit)
        │
        ▼
regenerate implementation
        │
        ▼
run frozen test suite
        │
   ┌────┴────┐
 green      red
   │          │
 deploy   tighten prose / add golden example → loop
```

When a generated test surprises you, you don't fix the code — you tighten the `test-spec` or add a golden example. Over time the contract accretes precision exactly where bugs appeared, and the system converges instead of drifting.

## Toolchain (answers README TODO 1.B)

**MUST**
- `spec` (these docs) — canonical intent.
- `test-specs/` — prose criteria + golden examples.
- A regenerate-and-verify harness (generate tests → freeze → generate impl → run tests → gate deploy).

**OPTIONAL**
- Deterministic generation (pinned model snapshot, `temperature=0`, batch-invariant inference). Nice for reproducibility; not required, because verification covers correctness without it.

## What this is not

- Not "no code in git." Code is committed — as a cache.
- Not "the model is trusted because it's deterministic." It's trusted because its output passes a human-anchored contract.
- Not applicable to runtime data. The answers are sacred and never regenerated.

## Repo layout under this model

```
spec docs        → README.md, content/guidelines.md, this file   (canonical)
test-specs/      → prose behavioral criteria + golden examples    (canonical)
app/             → generated bot code + generated tests           (cache)
                   the answers DB lives at runtime, not in git    (sacred)
```
