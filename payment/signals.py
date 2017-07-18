from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO


# 支付成功将通过信号通知执行该函数
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()

        # 创建发票 e-mail
        subject = 'RunhuaOil\'s Shop - 发票号码: {}'.format(order.id)
        message = '请查收您购买物品的发票'
        email = EmailMessage(subject,
                             message,
                             'runhuaoil@shop.com',
                             [order.email])

        # 生成 PDF
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

        # 增加 PDF file
        email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
        # 发送 e-mail
        email.send()

valid_ipn_received.connect(payment_notification)
