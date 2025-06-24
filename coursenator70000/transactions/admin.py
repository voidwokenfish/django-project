from django.contrib import admin

from transactions.models import Transaction
from transactions.permission import NotAnyObjectPermissionMixin


@admin.register(Transaction)
class TransactionAdmin(NotAnyObjectPermissionMixin, admin.ModelAdmin):
    pass