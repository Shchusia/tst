from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Business(models.Model):
    business_title = models.CharField(max_length=200, unique=True, null=False)
    created = models.DateTimeField(auto_now=True, null=False)
    is_active = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "businesses"
        verbose_name = _("Business")
        verbose_name_plural = _("Businesses")

    def __str__(self):
        return self.business_title


class BusinessProduct(models.Model):
    builtins_product = models.CharField(max_length=200, unique=True, null=False)
    created = models.DateTimeField(auto_now=True, null=False)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)

    class Meta:
        db_table = "businesses_product"


class BusinessNews(models.Model):
    news_title = models.CharField(max_length=200, unique=True, null=False)
    news_text = models.CharField(max_length=200, unique=True, null=False)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)

    class Meta:
        db_table = "business_news"
