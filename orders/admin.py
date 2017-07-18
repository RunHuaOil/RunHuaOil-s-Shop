from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _


#  订单导出为CSV的 action
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta

    response = HttpResponse(content_type='text/csv; charset=gb2312')  # gb2312防止csv打开中文乱码
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response, dialect='excel')

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = _('导出为CSV')


#  定制自己的订单管理界面
def order_detail(obj):
    return '<a href="{}">{}</a>'.format(reverse('orders:admin_order_detail', args=[obj.id]), _('详情'))


order_detail.allow_tags = True


#  打印PDF按钮
def order_pdf(obj):
    return '<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf', args=[obj.id]))


order_pdf.allow_tags = True
order_pdf.short_description = _('PDF打印')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)
