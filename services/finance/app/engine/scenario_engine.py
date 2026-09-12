"""Deterministic projections using explicitly supplied scenario assumptions."""

from .calculator import calculate_projections


def calculate_scenarios(*, conservative: dict, moderate: dict, optimistic: dict):
    """Return independent monthly results under the three existing scenario names.

    Each input dictionary supplies calculate_projections arguments, including
    both required costs. Names imply no guaranteed ordering of results.
    Caller dictionaries are never modified.
    """
    results = {}
    for name, inputs in (
        ("conservative", conservative),
        ("moderate", moderate),
        ("optimistic", optimistic),
    ):
        if not isinstance(inputs, dict):
            raise TypeError(f"{name}: scenario inputs must be a dictionary")
        try:
            results[name] = calculate_projections(**inputs)
        except (TypeError, ValueError) as exc:
            raise type(exc)(f"{name}: {exc}") from exc
    return results
