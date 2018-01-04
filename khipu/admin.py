from django.contrib import admin

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    """
    Modelo de administracion de Ordenes de Khipu
    """
    list_display = (
        "id", "payment_id", "subject", "currency", "amount",
        "status"
    )
    search_fields = ["payment_id"]
    list_per_page = 100


admin.site.register(Payment, PaymentAdmin)
