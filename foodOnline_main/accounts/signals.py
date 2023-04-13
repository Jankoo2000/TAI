from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from foodOnline_main.accounts.models import User, UserProfile


# 26 after creating User it's created UserProfile

# @receiver(post_save, sender=User)
# def post_save_create_profile_receiver(sender, instance, created, **kwargs):
#     print(created)
#     if created:
#         UserProfile.objects.create(user=instance)
#         print('create the user profile')
#     else:
#         try:
#             profile = UserProfile.objects.get(user=instance)
#             profile.save()
#         except:
#             UserProfile.objects.create(user=instance)
#             print('Profile was not exist, but I created one')
#         print('user is updated')
#
#
# #26 - signal episode
# @receiver(pre_save, sender=User)
# def pre_save_profile_receiver(sender, instance, **kwargs):
#     print(instance.username, 'this user is being saved')