from app.models.risk import RiskCheckRequest


def check_high_value_transaction(
    request: RiskCheckRequest,
) -> tuple[int, str] | None:

    if request.payment.amount >= 1000:
        return (
            20,
            "High transaction amount",
        )

    return None


def check_country_mismatch(
    request: RiskCheckRequest,
) -> tuple[int, str] | None:

    bin_country = request.payment.bin_country

    if (
        bin_country
        and bin_country.upper()
        != request.shipping.country.upper()
    ):
        return (
            15,
            "Payment country differs from shipping country",
        )

    return None


def check_new_device(
    request: RiskCheckRequest,
) -> tuple[int, str] | None:

    if request.device.id.startswith("new-"):
        return (
            10,
            "Transaction is coming from a new device",
        )

    return None


def evaluate_rules(
    request: RiskCheckRequest,
) -> list[tuple[int, str]]:

    rules = [
        check_high_value_transaction,
        check_country_mismatch,
        check_new_device,
    ]

    results = []

    for rule in rules:
        result = rule(request)

        if result is not None:
            results.append(result)

    return results


def check_country_mismatch(
    request: RiskCheckRequest,
    config: RiskRuleConfig | None = None,
) -> RiskSignal | None:

    config = config or RiskRuleConfig()

    bin_country = request.payment.bin_country
    shipping_country = request.shipping.country

    if (
        bin_country
        and bin_country != shipping_country
    ):
        return RiskSignal(
            "COUNTRY_MISMATCH",
            config.country_mismatch_score,
            "Payment country differs from shipping country",
        )

    return None