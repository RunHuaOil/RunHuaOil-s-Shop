from django.db import models
from django.core.urlresolvers import reverse
from parler.models import TranslatableModel, TranslatedFields
from uuslug import uuslug


class Category(TranslatableModel):
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True,
                            allow_unicode=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=200,
                              db_index=True),
    )

    class Meta:
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Product, self).save(*args, **kwargs)
