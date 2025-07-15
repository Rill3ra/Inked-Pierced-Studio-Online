# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):  # Или admin.StackedInline для другого вида
    model = OrderItem
    raw_id_fields = ['product']  # Удобный виджет для выбора продукта

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email',
                    'shipping_address', 'city', 'postal_code', 'country',
                    'created_at', 'updated_at', 'is_paid']
    list_filter = ['is_paid', 'created_at', 'updated_at']
    search_fields = ['first_name', 'last_name', 'email', 'shipping_address']
    inlines = [OrderItemInline]  # Отображаем OrderItem прямо в форме Order
    date_hierarchy = 'created_at'  # Удобная навигация по датам

    # Дополнительные поля, доступные только для чтения (полезно для автоматически заполняемых полей)
    readonly_fields = ['created_at', 'updated_at']  # Или другие поля

    # Можно добавить действия для массового изменения заказов (например, отметить как оплаченные)
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
    mark_as_paid.short_description = "Отметить выбранные заказы как оплаченные"