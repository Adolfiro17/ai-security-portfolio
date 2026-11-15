# Notes: Securing an Agent That Takes Actions

## Core ideas

1. **A chatbot produces text. An agent does things.** The impact of a successful attack moves from
   embarrassment to action.
2. **Assume the model can be manipulated.** Design so the dangerous action fails anyway.
3. **The tool gateway is the security boundary.** It does not depend on the model behaving well.
4. **Controls overlap on purpose.** Allow-list, approval and scoped credentials each stop the
   attack alone. Losing one should not be fatal.

## The seven controls

| Control | What it prevents |
| --- | --- |
| Dedicated agent identity | Actions that cannot be attributed or governed |
| Allow-list per workflow | Tools the task never needed |
| Short-lived, single-use, tool-scoped credentials | Stolen or reused access |
| Human approval for high-impact tools | Silent high-impact actions |
| Input trust labels | Treating retrieved text as instructions |
| Complete tool-call logging | Blind spots in investigation |
| Emergency revocation | No way to stop an active incident |

## Honest limits of this lab

- The model is a mock, chosen so the proof rests on architecture.
- The gateway issues and redeems its own credentials and the approval queue is in-process. In
  production an identity provider issues tokens, tool backends validate them and approvals arrive
  over a channel the agent cannot write to.
- The two-agent escalation scenario in the project README is a planned extension, not yet built.

## Further reading

See the [interview guide](../../ai-security-interview-guide/README.md), especially Q2, Q4, Q9 and
Q16, and the OWASP LLM Top 10 (LLM01, LLM06, LLM07).
