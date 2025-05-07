from django.db import models
# from enums import RecipientType, SendingStatus

class News(models.Model):
    pass

# class EmailLetter(models.Model):
#     subject = models.CharField(max_length=100)
#     body = models.TextField()
#     recipient_type = models.CharField(choices=RecipientType, default=None, null=True, blank=True)
#     ready_to_send = models.BooleanField(default=False)
#     is_processed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     recipient_list = models.ManyToManyField(to='', blank=True)
#     news = models.OneToOneField(to=News, null=True, blank=True, on_delete=models.SET_NULL)

# class EmailLog(models.Model):
#     letter = models.ForeignKey(EmailLetter, on_delete=models.CASCADE, related_name='logs')
#     email = models.EmailField(null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     sending_status = models.CharField(choices=SendingStatus, null=True, blank=True)
#     error = models.TextField(null=True, blank=True)

# class EmailAttachment(models.Model):
#     email = models.ForeignKey(EmailLetter, on_delete=models.CASCADE, related_name='attachments')
#     file = models.FileField(upload_to='email/%Y/%m/%d')

class Subscription(models.Model):
    email = models.EmailField(null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email




