from .models import BetSelection


def update_coupon_status(coupon):
    won = True  # Assume the coupon has won until proven otherwise

    # Get all the bet selections for this coupon
    selections = BetSelection.objects.filter(coupon=coupon)

    for selection in selections:
        match = selection.match
        result = match.result  # The result is already stored (1, 0, 2)

        # Check if the selected event matches the actual result
        if result == "1" and selection.event != "1":
            won = False
        elif result == "0" and selection.event != "0":
            won = False
        elif result == "2" and selection.event != "2":
            won = False

    # Update the coupon status based on the outcome
    coupon.status = "Won" if won else "Lost"
    coupon.save()

