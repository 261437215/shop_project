from django.shortcuts import render
from django.http import HttpResponse
from common.models import Types

# Create your views here.
def index(request):
	'''浏览用户信息'''
	#typelist=Types.objects.all()
	typelist=Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
	#select *,concat(path,id) AS _has from types order by _has;
	#print(typelist)
	for vo in typelist:
		vo.pname=' . . . . ' * (vo.path.count(',')-1)
		#print(vo.path.count(','))
	context={'dicttype':typelist}
	#return HttpResponse(typelist)
	return render(request,'./myadmin/types/index.html',context)

def add(request,tid):
	'''跳转到添加页面'''
	if tid == '0' : #如果tid=0的话 就是创建一个根类别的商品
		context={'pid':0,'path':'0,','name':'根类别的商品'}
		return render(request,'./myadmin/types/add.html',context)

	else:
		typelist=Types.objects.get(id=tid)#如果tid!=0的话,就是在根类别下创建商品
		context={'pid':typelist.id,'path':typelist.path+str(typelist.id)+',','name':typelist.name}
		return render(request,'./myadmin/types/add.html',context)

	
def insert(request):
	'''执行添加操作'''
	try:
		types=Types()
		types.name=request.POST['name']
		types.pid=request.POST['pid']
		types.path=request.POST['path']
		types.save()
		context={'info':'添加成功!'}
	except Exception as err :
		print(f'错误原因是:{err}')
		context={'info':'添加失败!'}
	return render(request,'./myadmin/types/info.html',context)


def delete(request,tid):
	'''删除商品信息'''
	typelist=Types.objects.get(id=tid)#获取到删除的那一条信息
	print(typelist.id)
	try:
		typelist_subclass=Types.objects.get(pid=typelist.id)#根据删除信息的id,查询到是否有子类别信息
		context={'info':"删除失败!此商品还存在子商品."}
	except:
		typelist.delete() #如果不含有子类别商品信息,则删除。如果含有则提示删除失败.
		context={'info':'删除成功!'}
	return render(request,'./myadmin/types/info.html',context)


def edit(request,tid):
	'''跳转到编辑页面'''
	typelist=Types.objects.get(id=tid)
	# return HttpResponse(f"uid的值是{tid}")
	context={'dicttype':typelist}
	return render(request,'./myadmin/types/edit.html',context)
	
def update(request,tid):
	'''编辑商品信息'''
	try:
		print(f'tid is {tid}')
		types=Types.objects.get(id=tid)
		types.name=request.POST['name']
		types.save()
		context={'info':"修改成功!"}
	except Exception as err:
		context={'info':"修改失败!"}
	return render(request,"./myadmin/types/info.html",context)