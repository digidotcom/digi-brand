---
type: blueprint
genre: POC test plan
output: markdown
---

# POC Test Plan

A proof-of-concept test plan exists to make the outcome of a POC
non-negotiable in advance. Its whole value is that success and failure are
defined before the equipment is powered on. A POC without written exit criteria
ends in a debate about whether it worked.

Written by the PM, agreed with the customer or internal sponsor before the POC
starts.

## Section order

### Objective

One paragraph. What question does this POC answer? Frame it as a question with a
yes or no answer, not as an activity. "Can {{PRODUCT}} sustain {{REQUIREMENT}}
in {{ENVIRONMENT}}?" beats "Evaluate {{PRODUCT}}."

Name the decision that follows: what happens if the answer is yes, and what
happens if it is no.

### Success Criteria

The heart of the document. A numbered list of measurable statements, each with a
threshold and a method:

| # | Criterion | Threshold | How measured |
| --- | --- | --- | --- |
| 1 | {{CRITERION}} | {{THRESHOLD}} | {{METHOD}} |

Rules:

- Every criterion has a number, not an adjective. "Reliable" is not a criterion;
  "{{THRESHOLD}} uptime measured over {{DURATION}}" is.
- Every criterion names how it is measured, and by whom.
- Distinguish **must-pass** from **nice-to-have**. Mark each row.
- If a criterion cannot be measured with the equipment on hand, it does not
  belong in the POC.

### Scope

Two lists, both explicit.

**In scope** — what is being tested.

**Out of scope** — what is not. This list is the one that prevents the POC from
growing sideways. Include anything a stakeholder might reasonably assume is
covered.

### Environment

What is being tested, on what, where.

- **Hardware under test:** {{PRODUCT}}, {{FIRMWARE_VERSION}}
- **Management platform:** {{PLATFORM}}, {{VERSION}}
- **Network:** {{CARRIER_OR_TOPOLOGY}}
- **Site:** {{LOCATION}}, {{CONDITIONS}}
- **Comparison baseline:** {{INCUMBENT}}, if any

Record firmware and platform versions. A POC result without a version is not
reproducible.

### Test Cases

One block per case. Keep them small enough that a single case fails cleanly.

**Case {{N}}: {{TITLE}}**
- **Maps to criterion:** {{CRITERION_NUMBER}}
- **Preconditions:** {{STATE_BEFORE}}
- **Steps:** numbered, each one action
- **Expected result:** {{OBSERVABLE_OUTCOME}}
- **Actual result:** filled in during execution
- **Pass/Fail:** filled in during execution

Every case maps to a numbered success criterion. A case that maps to nothing is
either a missing criterion or a test nobody needs.

### Schedule

| Phase | Dates | Owner |
| --- | --- | --- |
| Preparation | {{DATES}} | {{OWNER}} |
| Execution | {{DATES}} | {{OWNER}} |
| Review and readout | {{DATES}} | {{OWNER}} |

### Roles

Who does what. Name the role and the person.

- **POC owner:** {{NAME}} — runs the plan, owns the readout
- **Technical lead:** {{NAME}} — executes test cases
- **Customer sponsor:** {{NAME}} — accepts or disputes results
- **Escalation:** {{NAME}} — decides when a blocker changes the plan

### Exit Criteria

When the POC is over, and what the outcome means.

- **Pass:** all must-pass criteria met. Next step: {{NEXT_STEP}}.
- **Conditional pass:** must-pass met, some nice-to-have missed. Next step:
  {{NEXT_STEP}}, with {{CONDITIONS}} tracked.
- **Fail:** any must-pass criterion missed. Next step: {{NEXT_STEP}}.
- **Abandoned:** blocked for {{DURATION}} without resolution.

State who declares the outcome. One named person, agreed in advance.
