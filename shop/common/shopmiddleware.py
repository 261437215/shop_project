#自定义中间件类
from django.shortcuts import redirect
from django.urls import reverse
import re

class ShopMiddleware(object):
	def __init__(self,get_response):
		self.get_response = get_response
		print("一次性配置和加载.")

	def __call__(self,request):
		#request到达views之前的代码
		urllist=['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']
		path=request.path
		if re.match('/myadmin',path) and (path not in urllist):
			if 'adminuser' not in request.session:
				return redirect(reverse("myadmin_login"))
				
		response = self.get_response(request)
		#response到达浏览器之后的代码
		return response