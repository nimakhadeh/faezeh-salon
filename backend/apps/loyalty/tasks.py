"""
Loyalty Celery Tasks - Award points on completion
"""

from celery import shared_task
from apps.loyalty.models import LoyaltyRule, LoyaltyPoint


@shared_task
def award_loyalty_points(user_id, amount, description=""):
    """Award loyalty points based on amount spent"""
    rule = LoyaltyRule.objects.filter(is_active=True).first()
    if not rule:
        return

    points = rule.calculate_points(amount)
    if points > 0:
        points_obj, _ = LoyaltyPoint.objects.get_or_create(user_id=user_id)
        points_obj.add_points(points, description)
        return points
    return 0
