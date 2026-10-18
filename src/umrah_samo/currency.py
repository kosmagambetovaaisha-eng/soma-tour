"""Currency conversion.

SAR services convert at 3.825 SAR per USD: the 3.75 peg plus 2 % for cash
payment. This is intentional.
"""

SAR_PER_USD = 3.75 * 1.02  # 3.825


def sar_to_usd(amount_sar: float) -> float:
    return amount_sar / SAR_PER_USD
