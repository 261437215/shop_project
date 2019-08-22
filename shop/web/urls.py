from django.urls import path,re_path
from web.views import index #导入视图

urlpatterns = [
	path('',index.index,name='index'),
	path('list',index.list,name='web_list'),#商品列表页
	re_path(r'^list/(?P<pIndex>[0-9]+)$',index.list,name='web_list'),
	re_path(r'^detail/(?P<gid>[0-9]+)$',index.detail,name='web_detail'),

	#前台登陆操作
	path('login',index.login,name="web_login"),
	path('verify',index.verify,name='web_verify'), #验证码
	path('dologin',index.dologin,name='web_dologin'),#执行登陆
	path('logout',index.logout,name='web_logout'),#退出登陆
	path('registration',index.registration,name='web_registration'),#跳转到注册页面
	path('insert',index.insert,name='web_insert'),#执行注册
]
