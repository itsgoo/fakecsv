from django.urls import path, re_path

from .views import Index, Login, Logout, NewSchema, DetailSchema
from .views import DeleteColumn, DeleteSchema, CsvSchema, SaveCsv

urlpatterns = [
	re_path(r'^$', Index.as_view(), name='index_page'),
	re_path('csv_download', CsvSchema.as_view(), name='csv_page'),
	path('save_csv/<int:pk>', SaveCsv.as_view(), name='save_csv'),
	path('accounts/login/', Login.as_view(), name='login_page'),
	path('logout', Logout.as_view(), name='logout_page'),
	path('new_schema', NewSchema.as_view(), name='new_schema'),
	path('delete_schema/<int:pk>', DeleteSchema.as_view(), name='delete_schema'),
	path('detail/<int:pk>', DetailSchema.as_view(), name='detail_schema'),
	path('detail/<int:pk1>/delete_column/<int:pk2>', DeleteColumn.as_view(), 
		name='delete_column'),
]


