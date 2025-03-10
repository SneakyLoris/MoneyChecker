import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils.timezone import now

from web.models import Purchase, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date = now()

        purchases = []

        for i in range(1, 31):
            user = User.objects.first()
            purchase = Purchase(
                title = f"{i}-ая покупка",
                value = random.randint(250, 3000),
                date = current_date,
                is_planed = False,
                user = user
            )
            purchases.append(purchase)

        saved = Purchase.objects.bulk_create(purchases)



    """
    class Purchase(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    value = models.FloatField(verbose_name="Значение")
    date = models.DateTimeField(verbose_name="Дата")
    is_planed = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(PurchaseCategory)
    """