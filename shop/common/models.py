from django.db import models
from datetime import datetime
# Create your models here.

class Users(models.Model):
	#后台用户信息类
	username=models.CharField(max_length=255)
	name=models.CharField(max_length=255)
	password=models.CharField(max_length=32)
	sex=models.IntegerField(default=1)
	address=models.CharField(max_length=32)
	code=models.CharField(max_length=6)
	phone=models.CharField(max_length=32)
	email=models.CharField(max_length=32)
	state=models.IntegerField(default=1)
	addtime=models.DateTimeField(default=datetime.now)

	def toDict(self):
		return {'id':self.id,'username':self.name,'name':self.name,'password':self.password,'sex':self.sex,'address':self.address,'code':self.code,'phone':self.phone,'email':self.email,'state':self.state}

	class Meta:
		db_table="users"


class Types(models.Model):
	#商品管理类
	name = models.CharField(max_length=32)
	pid = models.IntegerField(default=0)
	path = models.CharField(max_length=32)

	class Meta:
		db_table='types'

class Goods(models.Model):
	typeid = models.IntegerField()
	goods = models.CharField(max_length=32)   #商品名称
	company = models.CharField(max_length=50) #生产厂家
	content = models.TextField()
	price = models.FloatField()               #价格
	picname = models.CharField(max_length=255)  #商品图片名
	store = models.IntegerField(default=0)	  #库存量
	num = models.IntegerField(default=0)
	clicknum = models.IntegerField(default=0) #点击量
	state = models.IntegerField(default=1)    #状态
	addtime = models.DateTimeField(default=datetime.now) #时间

	def toDict(self):
		return {'id':self.id,'typeid':self.typeid,'goods':self.goods,'company':self.company,'price':self.price,'picname':self.picname,'store':self.store,'num':self.num,'clicknum':self.clicknum,'state':self.state}

	class Meta:
		db_table = "goods"  # 更改表名