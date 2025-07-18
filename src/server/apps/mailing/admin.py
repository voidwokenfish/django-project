from django.contrib import admin

from .models import EmailAttachment, EmailLetter, EmailLog, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(EmailLetter)
class EmailLetterAdmin(admin.ModelAdmin):
    pass

@admin.register(EmailAttachment)
class EmailAttachmentAdmin(admin.ModelAdmin):
    pass

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    pass