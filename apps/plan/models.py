from django.db import models


class Plan(models.Model):
    class PlanType(models.TextChoices):
        STARTER = "starter", "Starter"
        PROFESSIONAL = "professional", "Professional"
        PREMIUM = "premium", "Premium"

    name = models.CharField(max_length=50, choices=PlanType.choices, unique=True)
    description = models.TextField()
    price_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Percentage per ticket"
    )
    card_color = models.CharField(
        max_length=100, blank=True, help_text="Bootstrap color for card header"
    )
    button_class = models.CharField(
        max_length=100, blank=True, help_text="Bootstrap button class"
    )

    def __str__(self):
        return f"{self.get_name_display()} Plan"


class Feature(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="features")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.plan})"
