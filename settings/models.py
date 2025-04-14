from django.db import models
from solo.models import SingletonModel


"""
I used Chat-GPT for an idea to use model 
for setup delivery setting via admin panel.
DeliverySettings model with free delivery 
threshold and standard delivery percentage fields.
"""
class DeliverySettings(SingletonModel):
    free_delivery_threshold = models.DecimalField(max_digits=6, decimal_places=2, default=50)
    standard_delivery_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)

    def __str__(self):
        return f"Delivery Settings (Free over ${self.free_delivery_threshold})"