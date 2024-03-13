from django.db.models.signals import post_save
from django.dispatch import receiver
from NidsModels.models.system import Intrusions, Alerts


@receiver(post_save, sender=Intrusions)
def create_alert(sender, instance, **kwargs):
    """
    Signal receiver that triggers after a userschema instance is saved.

    Parameters:
    sender (Model): The model class that sent the signal.
    instance (UserSchema): The instance of the model being saved.
    **kwargs: Additional keyword arguments sent by the signal.
    """

    Alerts.objects.create(
        user=instance.user,
        intrusion=instance,
        severity=instance.severity,
    )
