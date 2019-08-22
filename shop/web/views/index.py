from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from common.models import Users,Types,Goods
from django.core.paginator import Paginator

def loadinfo(request):
	#公共函数
	#typelist=Types.objects.filter(pid=0)
	typelist=Types.objects.raw('select * from types where pid=0')
	context={'typelist':typelist}
	return context

def index(request):
	# return HttpResponse("这是网站前台!")
	context=loadinfo(request)
	return render(request,'./web/index.html',context)

def list(request,pIndex=1):
	#商品列表页
	context=loadinfo(request)
	mod = Goods.objects
	tid=int(request.GET.get('tid',0))
	price=int(request.GET.get('price',0))
	addtime=int(request.GET.get('addtime',0))
	# print(tid)
	wherelist=[]
	if tid > 0 :
		goodslist=mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid)).order_by("-clicknum")
		#goodslist=mod.raw("select * from goods as a left join types as b on  a.typeid=b.id where b.pid=%s order by a.clicknum ",[tid])
		wherelist.append('tid='+str(tid))
		if price == 1: #1是升序
			goodslist=mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid)).order_by("price")
			wherelist.append('price='+str(price))
		elif addtime == 1: #对商品添加时间进行降序
			goodslist=mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid)).order_by("-addtime")
			wherelist.append('addtime='+str(addtime))
	else :
		goodslist=mod.filter().order_by("-clicknum")
		if price == 1: #1是升序
			goodslist=mod.filter().order_by("price")
			wherelist.append('price='+str(price))
		elif addtime == 1: #对商品添加时间进行降序
			goodslist=mod.filter().order_by("-addtime")
			wherelist.append('addtime='+str(addtime))


	print(f"搜索条件是:{wherelist}")
	p=Paginator(goodslist,4)
	p_list=p.page_range 
	pIndex=int(pIndex)
	p_list_max=int(p_list[-1])
	p_list_min=int(p_list[0])
	if pIndex < p_list_min or pIndex =='' :
		pIndex=1
	elif  pIndex > p_list_max :
		pIndex=p_list_max
	currentlist=p.page(pIndex)#当前页数商品信息

	# print(f'最大页数{p_list_max},最小页数{p_list_min}')
	context['currentlist']=currentlist
	context['pIndex']=pIndex
	context['p_list']=p_list
	context['p_list_max']=p_list_max
	context['p_list_min']=p_list_min
	context['wherelist']=wherelist
	context['goodslist']=goodslist
	return render(request,'./web/list.html',context)

def detail(request,gid):
	#商品详情页
	context=loadinfo(request)
	print(gid)
	goods=Goods.objects.filter(id=gid)
	#goods=Goods.objects.raw("select * from goods where id = %s",[gid])
	print(goods)
	for go in goods:
		go.clicknum += 1
		go.save()
	context['goods']=goods
	return render(request,'./web/detail.html',context)

def login(request):
	#跳转到登陆页面
	return render(request,'./web/login.html')

def verify(request):
	#引入随机函数模块
	import random
	from PIL import Image, ImageDraw, ImageFont
	#定义变量，用于画面的背景色、宽、高
	#bgcolor = (random.randrange(20, 100), random.randrange(
	#    20, 100),100)
	bgcolor = (242,164,247)
	width = 100
	height = 25
	#创建画面对象
	im = Image.new('RGB', (width, height), bgcolor)
	#创建画笔对象
	draw = ImageDraw.Draw(im)
	#调用画笔的point()函数绘制噪点
	for i in range(0, 100):
		xy = (random.randrange(0, width), random.randrange(0, height))
		fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
		draw.point(xy, fill=fill)
	#定义验证码的备选值
	#str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	str1 = '0123456789'
	#随机选取4个值作为验证码
	rand_str = ''
	for i in range(0, 4):
		rand_str += str1[random.randrange(0, len(str1))]
	#构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
	font = ImageFont.truetype('static/STXIHEI.TTF', 21)
	#font = ImageFont.load_default().font
	#构造字体颜色
	fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
	#绘制4个字
	draw.text((5,-3), rand_str[0], font=font, fill=fontcolor)
	draw.text((25,-3), rand_str[1], font=font, fill=fontcolor)
	draw.text((50,-3), rand_str[2], font=font, fill=fontcolor)
	draw.text((75,-3), rand_str[3], font=font, fill=fontcolor)
	#释放画笔
	del draw
	#存入session，用于做进一步验证
	request.session['verifycode'] = rand_str
	"""
	python2的为
	# 内存文件操作
	import cStringIO
	buf = cStringIO.StringIO()
	"""
	# 内存文件操作-->此方法为python3的
	import io
	buf = io.BytesIO()
	#将图片保存在内存中，文件类型为png
	im.save(buf, 'png')
	#将内存中的图片数据返回给客户端，MIME类型为图片png
	return HttpResponse(buf.getvalue(), 'image/png') #验证码

def dologin(request):
	#执行登陆操作
	verifycode = request.session['verifycode']
	code = request.POST['code'] 
	if verifycode != code:
		context = {'info':'验证码错误！'}
		return render(request,"./web/login.html",context)
	try:
		user = Users.objects.get(username=request.POST['username'])
		if user.state != 2:
			import hashlib
			m = hashlib.md5() 
			m.update(bytes(request.POST['password'],encoding="utf8"))
			if user.password == m.hexdigest():
				request.session['webuser'] = user.toDict() #request.session是键,'webuser'是值
				return render(request,'./web/index.html')
			else:
				context={'info':'账号,密码错误!'}  
		else :
			context={'info':'账号,密码错误!'}  
	except :
		context={'info':'账号,密码错误!'} 
	return render(request,'./web/login.html',context)

def logout(request):
	try:
		del request.session['webuser']  # 删除键是'webuser'的条目
	except:
		return render(request,'./web/index.html')
	return render(request,'./web/index.html')

def registration(request):
	#跳转到注册页面
	return render(request,'./web/registration.html')

def insert(request):
	#执行注册
	user=Users()
	verifycode = request.session['verifycode']
	code = request.POST['code'] 
	if verifycode != code:
		context = {'info':'验证码错误！'}
		return render(request,"./web/login.html",context)
	user.username=request.POST['username']
	password1=request.POST.get('password1')
	password2=request.POST.get('password2')
	if password1 != password2:
		context={'info':'两次密码不一致!'}
		return render(request,'./web/login.html',context)
	else:
		#如果注册成功,则直接跳转到首页.
		import hashlib
		m = hashlib.md5() 
		m.update(bytes(password2,encoding="utf8"))
		user.password=m.hexdigest()
		user.save()
		request.session['webuser']=user.toDict()
		return render(request,'./web/index.html')
