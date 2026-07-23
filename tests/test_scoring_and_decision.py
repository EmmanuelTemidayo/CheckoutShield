from app.models.signals import RiskSignal


def test_empty_signal_set_has_zero_score():

    result = RiskScorer().calculate([])

    assert result.score == 0
    assert result.level == RiskLevel.LOW


def test_score_is_capped_when_multiple_signals_exceed_limit():

    result = RiskScorer().calculate(
        [
            RiskSignal("A", 80, "a"),
            RiskSignal("B", 80, "b"),
        ]
    )

    assert result.score == 100
    assert result.level == RiskLevel.CRITICAL