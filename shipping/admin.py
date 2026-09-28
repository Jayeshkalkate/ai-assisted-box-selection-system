from django.contrib import admin

# Register your models here.

from .models import Box, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "dimensions", "weight_kg")
    search_fields = ("sku", "name")
    ordering = ("sku",)

    @admin.display(description="Dimensions (cm)")
    def dimensions(self, obj):
        return f"{obj.length_cm} × {obj.width_cm} × {obj.height_cm}"


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "dimensions",
        "max_weight_kg",
        "cost",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("cost", "name")

    @admin.display(description="Inner dimensions (cm)")
    def dimensions(self, obj):
        return (
            f"{obj.inner_length_cm} × {obj.inner_width_cm} × "
            f"{obj.inner_height_cm}"
        )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("reference", "created_at", "item_count")
    search_fields = ("reference",)
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]
    ordering = ("-created_at",)

    @admin.display(description="Line items")
    def item_count(self, obj):
        return obj.items.count()
