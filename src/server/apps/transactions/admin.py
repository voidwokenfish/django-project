from django.contrib import admin

from server.apps.transactions.models import Transaction
from server.apps.transactions.permission import NotAnyObjectPermissionMixin


@admin.register(Transaction)
class TransactionAdmin(NotAnyObjectPermissionMixin, admin.ModelAdmin):
    pass