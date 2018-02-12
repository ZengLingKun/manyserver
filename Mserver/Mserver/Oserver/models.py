from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=50)
  def __str__(self):
    return self.name

class Server(models.Model):
    OS_CHOICES = (
        ('w', 'Windowns'),
        ('l', 'RedHat'),
    )
    host_ip = models.GenericIPAddressField(unique=True,blank=False,null=False)
    host_user = models.CharField(max_length=50,default='root')
    where_add = models.CharField(max_length=50,default='admin')
    host_passwd = models.CharField(max_length=50,default='ops123!')
    has_nmon = models.BooleanField(default=0)
    category = models.ForeignKey(Category,
                                related_name='host_category')
    body = models.TextField(blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    host_os = models.CharField(max_length=50,  
                                choices=OS_CHOICES,
                                default='l')
    class Meta:
      ordering=('category','-host_ip',)
    def __str__(self):
      return self.host_ip

