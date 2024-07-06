# # File: product/signals.py

# import logging
# from django.db.models.signals import pre_delete
# from django.dispatch import receiver
# from .models import CustomUser, Product

# logger = logging.getLogger(__name__)

# @receiver(pre_delete, sender=CustomUser)
# def handle_user_deletion(sender, instance, **kwargs):
#     logger.info(f'Deleting user {instance.username} and related products')
#     # Delete related products before deleting the user
#     Product.objects.filter(created_by=instance).delete()
