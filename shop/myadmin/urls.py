from django.urls import path,re_path
from myadmin.views import index,users,types,goods#导入视图

urlpatterns = [
	path('',index.index,name='myadmin_index'), #后台首页
	#会员登陆操作
	path('login',index.login,name="myadmin_login"),
	path('dologin',index.dologin,name='myadmin_dologin'),
	path('logout',index.logout,name='myadmin_logout'),
	path('verify',index.verify,name='myadmin_verify'), #验证码

	#后台会员操作
	re_path(r'^users/(?P<pIndex>[0-9]+)$',users.index,name='myadmin_users_index'),
	path('users/add',users.add,name='myadmin_users_add'),
	path('users/insert',users.insert,name='myadmin_users_insert'),
	re_path(r'^users/delete/(?P<uid>[0-9]+)$',users.delete,name='myadmin_users_delete'),
	re_path(r'^users/edit/(?P<uid>[0-9]+)$',users.edit,name='myadmin_users_edit'),
	re_path(r'^users/update/(?P<uid>[0-9]+)$',users.update,name='myadmin_users_update'),
	re_path(r'^users/reset/(?P<uid>[0-9]+)$',users.reset,name='myadmin_users_reset'),
	re_path(r'^users/resetps/(?P<uid>[0-9]+)$',users.resetps,name='myadmin_users_resetps'),


	#后台商品操作
	path('types',types.index,name='myadmin_types_index'),
	re_path(r'^types/add/(?P<tid>[0-9]+)$',types.add,name='myadmin_types_add'),
	path('types/insert',types.insert,name='myadmin_types_insert'),
	re_path(r'^types/delete/(?P<tid>[0-9]+)$',types.delete,name='myadmin_types_delete'),
	re_path(r'^types/edit/(?P<tid>[0-9]+)$',types.edit,name='myadmin_types_edit'),
	re_path(r'^types/update/(?P<tid>[0-9]+)$',types.update,name='myadmin_types_update'),

	#后台商品操作
	re_path(r'^goods/(?P<pIndex>[0-9]+)$',goods.index,name='myadmin_goods_index'),
	path('goods/add',goods.add,name='myadmin_goods_add'),
	path('goods/insert',goods.insert,name='myadmin_goods_insert'),
	re_path(r'^goods/delete/(?P<gid>[0-9]+)$',goods.delete,name='myadmin_goods_delete'),
	re_path(r'^goods/edit/(?P<gid>[0-9]+)$',goods.edit,name='myadmin_goods_edit'),
	re_path(r'^goods/update/(?P<gid>[0-9]+)$',goods.update,name='myadmin_goods_update'),
]
