from django.shortcuts import render
from django.http import HttpResponse
from common.models import Types,Goods
from PIL import Image
import time,os
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def index(request,pIndex):
	'''浏览商品信息'''
	name=request.GET.get('goods')
	typeid=request.GET.get('typeid')
	if typeid =='0':
		typeid=None
	state=request.GET.get('state')
	if state =='0':
		state=None
	types=Types.objects.extra(select={'_has':"concat(path,id)"}).order_by('_has')
	goods=Goods.objects.filter()
	wherelist=[]
	if name:
		goods=goods.filter(Q(goods__contains=name))
		wherelist.append('goods='+name)
		if state :
			goods=goods.filter(Q(state=state))
			wherelist.append('state='+state)
	if typeid :
		goods=Goods.objects.raw("select * from goods as a left join types as b on a.typeid=b.id where b.id=%s or b.pid=%s;",[typeid,typeid])
		wherelist.append('typeid='+typeid)
	print(f"查询条件是{wherelist}")
	for go in goods:
		ty=Types.objects.get(id=go.typeid)
		go.typename=ty.name
	for vo in types:
		vo.pname='. .'*(vo.path.count(',')-1) 
	p=Paginator(goods,3)
	datelist=p.page(pIndex)
	pIndex=int(pIndex)
	plist=p.page_range#获取信息的所有页数
	plist_min=int(plist[0])#前面的页数
	plist_max=int(plist[-1])#后面的页数
	if pIndex >= plist_max :
		pIndex=plist_max
	if pIndex <= plist_min :
		pIndex = plist_min

	context={"dictgoods":datelist,'typelist':types,'plist':plist,'plist_min':plist_min,'plist_max':plist_max,'wherelist':wherelist}
	return render(request,'./myadmin/goods/index.html',context)

def add(request):
	'''跳转到添加页面'''
	types=Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
	for vo in types:
		vo.pname='. . .'*(vo.path.count(',')-1)
		#print(vo.path.count(',')-1)
	context={'dicttypes':types}

	return render(request,'./myadmin/goods/add.html',context)
	
def insert(request):
	'''执行添加操作'''
	goods=Goods()
	goods.goods=request.POST['goods'] #商品名称
	goods.typeid=request.POST['typeid']
	goods.company=request.POST['company'] #生产厂家
	goods.price=request.POST['price'] #价格
	goods.store=request.POST['store'] #库存
	goods.state=1                     #状态
	goods.content=request.POST['content'] #商品简介
	goods.addtime=datetime.now().strftime("%Y-%m-%d %H:%H:%S")

	photofile=request.FILES.get('file',None)
	if photofile == None:
		context={'info':'未获取到图片信息!请重新添加。'}
		return render(request,'./myadmin/goods/info.html',context)
	goods.picname=str(time.time())+'.'+photofile.name.split('.').pop()
	openphoto=open('./static/myadmin/photo/'+goods.picname,'wb+')
	for chunk in photofile.chunks():
		openphoto.write(chunk)
	openphoto.close()


	# 执行图片缩放
	im = Image.open("./static/myadmin/photo/"+goods.picname)
	# 缩放到75*75(缩放后的宽高比例不变):
	im.thumbnail((100, 100))
	im.save("./static/myadmin/photo/s_"+goods.picname,None)

	#执行图片删除
	os.remove("./static/myadmin/photo/"+goods.picname)
	goods.save()
	context={'info':'商品信息添加成功!'}
	return render(request,'./myadmin/goods/info.html',context)

def delete(request,gid):
	'''删除商品信息'''
	goods=Goods.objects.get(id=gid)
	if goods.state == 1 :
		os.remove('./static/myadmin/photo/s_'+goods.picname)
		goods.delete()
		context={"info":"删除成功!"}
	else:
		context={"info":'删除失败,该商品不是新品.'}
	return render(request,'./myadmin/goods/info.html',context)

def edit(request,gid):
	'''跳转到编辑页面'''
	goods=Goods.objects.get(id=gid)
	types=Types.objects.extra(select={"_has":'concat(path,id)'}).order_by("_has")
	for ty in types:
		ty.pname='. . .'*(ty.path.count(',')-1)
	context={'dictgoods':goods,'dicttypes':types}
	return render(request,'./myadmin/goods/edit.html',context)
	# return HttpResponse("跳转到编辑页面",context)
	
def update(request,gid):
	'''编辑商品信息'''
	try:
		goods=Goods.objects.get(id=gid)
		print(f"gid is {gid}")
		goods.goods=request.POST['goods'] #商品名称
		goods.typeid=request.POST['typeid']
		goods.company=request.POST['company'] #生产厂家
		goods.price=request.POST['price'] #价格
		goods.store=request.POST['store'] #库存
		goods.state=request.POST.get('state',1)                #状态
		goods.content=request.POST['content']#商品简介
		goods.addtime=datetime.now().strftime("%Y-%m-%d %H:%H:%S")
		goods.save()

		photofile=request.FILES.get('file')
		if photofile == None:
			content={"info":'未获取到图片信息!'}
			return render(request,'./myadmin/goods/info.html',context)
		os.remove('./static/myadmin/photo/s_'+goods.picname)
	except:
		goods.picname=str(time.time())+'.'+photofile.name.split('.').pop()
		openphoto=open('./static/myadmin/photo/'+goods.picname,'wb+')
		for chunk in photofile.chunks():
			openphoto.write(chunk)
		openphoto.close()
		# 执行图片缩放
		im = Image.open("./static/myadmin/photo/"+goods.picname)
		# 缩放到75*75(缩放后的宽高比例不变):
		im.thumbnail((75, 75))
		im.save("./static/myadmin/photo/s_"+goods.picname,None)

		#执行图片删除
		os.remove("./static/myadmin/photo/"+goods.picname)
		goods.save()
		context={'info':'请填写编辑页面的内容!'}
		return render(request,'./myadmin/goods/info.html',context)
	else:
		goods.picname=str(time.time())+'.'+photofile.name.split('.').pop()
		openphoto=open('./static/myadmin/photo/'+goods.picname,'wb+')
		for chunk in photofile.chunks():
			openphoto.write(chunk)
		openphoto.close()
		# 执行图片缩放
		im = Image.open("./static/myadmin/photo/"+goods.picname)
		# 缩放到75*75(缩放后的宽高比例不变):
		im.thumbnail((75, 75))
		im.save("./static/myadmin/photo/s_"+goods.picname,None)

		#执行图片删除
		os.remove("./static/myadmin/photo/"+goods.picname)
		goods.save()
		context={'info':'商品信息已修改!'}
	return render(request,'./myadmin/goods/info.html',context)





