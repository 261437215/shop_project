from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users
import time
from django.core.paginator import Paginator
# from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
# Create your views here.
def index(request,pIndex):
	'''浏览用户信息'''
	wherelist=[]
	name=request.GET.get('name',None)
	sex=request.GET.get('sex')
	if sex == '0':
		sex=None
	if name :
		users=Users.objects.filter(Q(username__icontains=name)|Q(name__icontains=name)).order_by('state')
		wherelist.append('name='+name)
	else:
		users=Users.objects.filter().order_by('state')

	if sex != None:
		users=users.filter(Q(sex=int(sex)))#users=Users.objects.filter(Q(username__icontains=name)|Q(name__icontains=name),Q(sex=int(sex))).order_by('state')
		wherelist.append('sex='+sex)

	print(f'搜索条件是:{wherelist}')
	p = Paginator(users,3) #获取到处理过的信息,以三条信息为一页
	pIndex=int(pIndex)
	userslist = p.page(pIndex) #当前页数数据
	plist = p.page_range #以列表的形式获取到所有信息的页号
	print(f'当前页数一共有:{plist}')
	plist_min=plist[0]#最大页数
	plist_max=plist[-1]#最小页数
	if pIndex > plist_max :
		pIndex=int(plist_max)
	if pIndex < 1 or pIndex is None:
		pIndex = 1
	context={'dictusers':userslist,'plist':plist,'plist_max':plist_max,'plist_min':plist_min,'wherelist':wherelist}
	return render(request,'myadmin/users/index.html',context)

def add(request):
	'''跳转到添加页面'''
	return render(request,'myadmin/users/add.html')
# @csrf_exempt
def insert(request):
	try:
		user=Users()
		user.username=request.POST['username']
		user.name=request.POST['name']

		import hashlib
		md5=hashlib.md5()#md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
		md5.update(bytes(request.POST['password'],encoding='utf-8'))#要对哪个字符串进行加密，就放这里
		user.password=md5.hexdigest()#拿到加密字符串
		print(f"md5加密之后的结果:{user.password}")


		user.sex=request.POST['sex']
		user.address=request.POST['address']
		user.code=request.POST['code']
		user.phone=request.POST['phone']
		user.email=request.POST['email']
		user.state='1'
		user.addtime=datetime.now().strftime("%Y-%m-%d %H:%H:%S")
		user.save()
		print(user.addtime)
		context={'info':'会员添加成功!'}
	except Exception as err:
		context={'info':'会员添加失败!'}
		print(f"添加失败的原因是:{err}")
	return render(request,'./myadmin/users/info.html',context)
	
def delete(request,uid):
	'''删除用户信息'''
	try:
		user=Users.objects.get(id=uid)
		user.delete()
		context={'info':"删除成功!"}
	except Exception as err:
		context={"info":'删除失败!'}
	return render(request,'./myadmin/users/info.html',context)
	
def edit(request,uid):
	'''跳转到编辑页面'''
	userlist=Users.objects.get(id=uid)
	# return HttpResponse(f"uid的值是{uid}")
	context={'dictuser':userlist}
	return render(request,'./myadmin/users/edit.html',context)
	
def update(request,uid):
	'''编辑用户信息'''
	try:
		print(f'uid is {uid}')
		userlist=Users.objects.get(id=uid)
		userlist.name=request.POST['name']
		import hashlib
		md5=hashlib.md5()
		md5.update(bytes(request.POST['password'],encoding="utf-8"))
		userlist.password=md5.hexdigest()

		userlist.sex=request.POST['sex']
		userlist.address=request.POST['address']
		userlist.code=request.POST['code']
		userlist.phone=request.POST['phone']
		userlist.email=request.POST['email']
		userlist.state=request.POST['state']
		userlist.addtime=datetime.now().strftime("%Y-%m-%d %H:%H:%S")
		userlist.save()
		context={'info':"修改成功!"}
	except Exception as err:
		context={'info':'修改失败,编辑信息没有填写完整,请重新填写.'}
	return render(request,"./myadmin/users/info.html",context)

def reset(request,uid):
	userlist=Users.objects.get(id=uid)
	context={'dictuser':userlist}
	return render(request,'./myadmin/users/resetps.html',context)

def resetps(request,uid):
	try:
		userslist=Users.objects.get(id=uid)
		import hashlib
		md5=hashlib.md5()
		md5.update(bytes(request.POST['password'],encoding='utf-8'))
		userslist.password=md5.hexdigest()
		userslist.save()
		context={'info':'密码重置成功!'}
	except Exception as err:
		context={'info':'密码重置失败!'}
		print(f'密码重置失败的原因是:{err}')
	return render(request,'./myadmin/users/info.html',context) 

