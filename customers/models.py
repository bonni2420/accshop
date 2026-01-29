from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password, identify_hasher


class Customer(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, unique=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=265)
    
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    
    @property
    def is_authenticated(self):
        return True

    class Meta:
        db_table = 'customer'
        ordering = ['-created_at']
        verbose_name_plural = "Khách Hàng"
        
    def __str__(self):
        return f"{self.name or self.username} (ID:{self.pk})"
    
    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        self.is_delete = True
        self.save()
    
    def check_password(self, raw_password):
        """ Kiểm tra mật khẩu người dùng nhập có khớp không"""
        return check_password(raw_password, self.password)
        
    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
