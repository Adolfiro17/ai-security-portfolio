"""The lab layer must keep working, because learners depend on its output."""
import json

import pytest

from lab import challenges, findings, mutations


@pytest.mark.parametrize("n", list(challenges.CHALLENGES))
def test_every_challenge_runs(n, capsys):
    challenges.run(n)
    assert "Challenge" in capsys.readouterr().out


def test_mutations_show_defence_in_depth():
    assert mutations.baseline()["blocked"] is True
    # One control removed: still blocked, nothing leaked.
    one = mutations.without_allow_list()
    assert one["blocked"] is True and not mutations._leaked(one)
    # Two controls removed: the manipulated model reaches the record.
    two = mutations.without_allow_list_and_approval()
    assert mutations._leaked(two)


def test_findings_roundtrip_and_export(tmp_path, monkeypatch):
    monkeypatch.setenv("LAB_FINDINGS_FILE", str(tmp_path / "f.jsonl"))
    findings.record(3, "Injected document", "successful", "insecure agent leaked")
    findings.record(4, "Same attack, hardened", "blocked")
    assert len(findings.load()) == 2
    out = findings.export_markdown(tmp_path / "report.md")
    text = out.read_text()
    assert "Injected document" in text and "| blocked | 1 |" in text


def test_findings_reject_unknown_result(tmp_path, monkeypatch):
    monkeypatch.setenv("LAB_FINDINGS_FILE", str(tmp_path / "f.jsonl"))
    with pytest.raises(ValueError):
        findings.record(1, "x", "maybe")
