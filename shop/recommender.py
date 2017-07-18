import redis
from django.conf import settings
from .models import Product

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender(object):
    # 给每个产品ID起一个key name
    def get_product_key(self, product_id):
        return 'product:{}:purchased_with'.format(product_id)

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # 一样的产品ID不做计算
                if product_id != with_id:
                    # 以其中一个产品 id 为集合name, 其他一起买的产品 id 作为成员，增加 1 分
                    r.zincrby(self.get_product_key(product_id), with_id, amount=1)

    def suggest_products_for(self, products, max_results=6):
        if len(products) == 0:
            return
        # 取选购商品的所有 id
        products_ids = [p.id for p in products]
        # 假如只有一个选购商品
        if len(products) == 1:
            # 获取该 key 的集合所有一起购买商品的 id 分数做降序
            suggestions = r.zrange(self.get_product_key(products_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # 在多个选购商品的情况下
            # 以选购商品的ID生成一个临时 key ，来进行并集计算
            flat_ids = ''.join([str(each_id) for each_id in products_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            # 获取所有选购商品的 key name
            products_keys = [self.get_product_key(each_id) for each_id in products_ids]
            # 将各个产品id的集合做 并集 计算，相同 member 的分数相加，最后存储在key name是tmp_key的集合中
            r.zunionstore(tmp_key, products_keys)
            # 从tmp_key中通过 id 删除已经选购的商品(member)
            r.zrem(tmp_key, *products_ids)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)
        # 此时的 list 是有序的
        suggested_products_ids = [int(each_id) for each_id in suggestions]
        # 获取对象后的 list 是无序的
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))

        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

