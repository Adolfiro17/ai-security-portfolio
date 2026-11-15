# Lab 1: Attack and Defend the Northwind Retail IT Support Agent

> **Deliberately vulnerable.** The insecure agent is insecure on purpose. All data is fictional and
> everything runs locally against a mock model. Do not deploy any of this.

## 1. Your role

Northwind Retail has built an IT support agent that can read support documents, create tickets and
look up assets. You are the AI security engineer asked to test it. The developers believe it is safe
because "the model follows its instructions". Your job is to test that belief and then prove the
fix.

## 2. Learning outcomes

By the end you can:

1. establish normal behaviour before testing an attack;
2. find and explain an indirect prompt injection;
3. show why a manipulated model is not a security boundary;
4. explain how a tool gateway (identity, allow-list, approval, scoped credentials, revocation) stops
   the same attack;
5. work out which controls carry the weight by removing them;
6. record findings and export an assessment report.

## 3. Setup (one command)

No API key, no cloud account and no network after the first install.

```bash
cd 01-secure-ai-agent
./start.sh            # Linux or macOS: tests, seeded attack, all challenges
```

```powershell
cd 01-secure-ai-agent
.\start.ps1           # Windows PowerShell
```

You need Python 3.11 or newer. On Debian or Ubuntu you may first need
`sudo apt install -y python3-venv`.

Run challenges one at a time while you work: `./start.sh lab 3`.

## 4. Why the model is a mock

The model is deterministic and fully manipulable: once it reads the planted instruction, it obeys
it every time. That is deliberate. If the hardened agent still stops the attack, the proof rests on
the architecture and not on a model happening to behave well.

## 5. Challenges

For each one, **predict first**, run it, then record what you saw:

```bash
python -m lab.findings add --challenge 3 --attack "Indirect injection" \
    --result successful --notes "What happened and why"
```

| # | Challenge | Run | Question to answer |
| --- | --- | --- | --- |
| 1 | Establish normal behaviour | `./start.sh lab 1` | Do both agents do the legitimate job? Why test this before attacking? |
| 2 | Find the planted injection | `./start.sh lab 2` | Where is it hidden, and why would a human reviewer miss it? |
| 3 | Exploit the insecure agent | `./start.sh lab 3` | Whose identity ran the action? Who approved it? What did the log claim? |
| 4 | Replay against the hardened agent | `./start.sh lab 4` | Was the model any less manipulated? What stopped the call? |
| 5 | Approval lifecycle | `./start.sh lab 5` | Why does step 3 fail even though the approval was granted? |
| 6 | Scoped, single-use credentials | `./start.sh lab 6` | What can an attacker do with a stolen credential? |
| 7 | Emergency revocation | `./start.sh lab 7` | Why does the legitimate task also stop, and is that acceptable? |
| 8 | Remove controls | `./start.sh lab 8` | Which single control can you lose safely, and which pair can you not? |

## 6. Hands-on tasks

Do these by editing code, then run `python -m pytest -q`.

**Task A, read the boundary.** Open `app/agent_hardened.py` and list the checks in
`ToolGateway.call` in the order they run. Why does revocation come first?

**Task B, widen the allow-list safely.** Add `query_asset_inventory` to the allow-list for a
workflow that genuinely needs it. Which control still protects the restricted record, and what must
you add so the approver sees the real arguments?

**Task C, add a tool.** Add `reset_password(user)` to `app/tools.py` and the gateway. Decide whether
it is `high_impact`. Write a test proving an injected request to reset an executive's password is
blocked.

**Task D, spoil your own defence.** Set `high_impact` to `False` for the asset tool and widen the
allow-list. Which existing test still passes, and which gap does that reveal? Write the test that
would have caught it.

**Task E, strengthen the log.** The log records blocked calls. Add a field that records which
document was read most recently before each call, so an investigator can trace an injection to its
source.

## 7. Reflection questions

1. Why is "tell the model not to do it" not a control?
2. In this demo the approval is decided in code. What would make a real approval channel
   trustworthy, and what would make it theatre? (See Q16 in the interview guide.)
3. Which control would you remove last, and why?
4. What does this lab not cover? (Hint: the two-agent escalation scenario in the project README is
   still a planned extension.)

## 8. Export your assessment

```bash
python -m lab.findings list
python -m lab.findings export      # writes lab_assessment.md
```

Keep the report. A tester's deliverable is a clear record of what was tried, what happened and what
was fixed.

Solutions are in [../instructor/SOLUTION.md](../instructor/SOLUTION.md). Try the tasks first.
