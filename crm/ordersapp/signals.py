from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Order


@receiver(m2m_changed, sender=Order.items.through)
def update_order_total_price(sender, instance, action, **kwargs):
    """
    Автоматически пересчитывает total_price при изменении блюд в заказе.
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.total_price = sum(dish.price for dish in instance.items.all())
        instance.save(update_fields=["total_price"])  # Обновляем только total_price
