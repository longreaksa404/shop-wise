from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    #allow add sub category
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        if self.parent_category:
            return f'{self.parent_category.name} - {self.name}'
        return self.name