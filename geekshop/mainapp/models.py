from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(verbose_name='название', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    image = models.ImageField(upload_to='product_image', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)

    def __str__(self):
        return f"{self.name} ({self.category.name})"