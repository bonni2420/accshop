from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'category'
        verbose_name_plural = "Danh Mục"
    
    def __str__(self):
        return self.name


class GameAccount(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='account/thumbnails/%Y/%m',
        blank=True,
        null=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=25, blank=True, null=True)
    is_sold = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'game_account'
        verbose_name_plural = "Tài Khoản Game"

    def __str__(self):
        return f"[{self.pk}] {self.name}"
    
    
class GameAccountImage(models.Model):
    game_account = models.ForeignKey(
        GameAccount,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to='account/images/%Y/%m')
    
    class Meta:
        db_table = 'game_account_image'

    def __str__(self):
        return f"Ảnh của Game Account {self.game_account.pk}"