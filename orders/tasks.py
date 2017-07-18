from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'RunhuaOil\'s shop 订单: {}'.format(order.id)
    message = '亲爱的 {},您的商品已经成功下单,您的订单ID: {}'.format(order.customer_name, order.id)
    mail_sent = send_mail(subject, message, 'runhuaoil@shop.com', [order.email])
    return mail_sent
