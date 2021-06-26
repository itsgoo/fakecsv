from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

from .forms import Authform, SchemaForm, ListForm, EmptyListForm
from .models import Schema, List
from .tasks import create_csv

from datetime import date


class Index(LoginRequiredMixin, ListView):
	template_name = 'index.html'
	context_object_name = 'list_schemas'
	def get_queryset(self):
		return Schema.objects.filter(author=self.request.user)

class Login(LoginView):
	template_name = 'login.html'
	form_class = Authform
	succcess_url = reverse_lazy('index_page')
	def get_success_url(self):
		return self.succcess_url

class Logout(LogoutView):
	next_page = reverse_lazy('index_page')

class NewSchema(LoginRequiredMixin, View):
	def get(self, request):
		create_schema = Schema()
		create_schema.author = request.user
		create_schema.title = 'New schemas name'
		create_schema.sepataror = ';'
		create_schema.character = 'qwerty'
		create_schema.modified = date.today() 
		create_schema.status = 'ready_to_generate'
		create_schema.save()
		url_name = 'detail/' + str(create_schema.id)
		return redirect(url_name)

class DeleteColumn(LoginRequiredMixin, View):
	def get(self, request, pk1, pk2):
		obj_to_delete= List.objects.get(id=pk2)
		obj_to_delete.delete()
		url = '/detail/' + str(pk1)
		if obj_to_delete.schema_id.author != request.user:
			return HttpResponseForbidden()
		return redirect(url)

class DeleteSchema(LoginRequiredMixin, View):
	def get(self, request, pk):
		obj_to_delete= Schema.objects.get(id=pk)
		if obj_to_delete.author != request.user:
			return HttpResponseForbidden()
		obj_to_delete.delete()
		return redirect('index_page')

class DetailSchema(LoginRequiredMixin, View):
	def get(self, request, pk):
		obj_schema = Schema.objects.get(id=pk)
		form_schema = SchemaForm(instance=obj_schema)
		obj_list = List.objects.filter(schema_id=pk).order_by('order')
		empty_form_list = EmptyListForm()
		ctx = {
			'obj_list' : obj_list,
			'form_schema' : form_schema,
			'empty_form_list' : empty_form_list,
		}
		if obj_schema.author != request.user:
			return HttpResponseForbidden()
		return render(request, 'detail.html', ctx)

	def post(self, request, pk):
		# cath any forms from page by method 
		req = request.POST
		if request.method== 'POST' and 'empty_form_list' in req:
			list_form = ListForm(req)
			if list_form.is_valid():
				add_list_element = list_form.save(commit=True)
				add_list_element.column_name = req.get('column_name')
				add_list_element.column_type = req.get('column_type')
				add_list_element.parameters = req.get('parameters')
				add_list_element.order = req.get('order') 
				add_list_element.schema_id = get_object_or_404(Schema, id=pk)

				if add_list_element.schema_id.author != request.user:
					return HttpResponseForbidden()
				add_list_element.save()
				return HttpResponseRedirect(self.request.path_info)

		elif request.method == 'POST' \
			and 'empty_form_list' not in req \
			and 'form_schema' not in req:
			list_form = ListForm(request.POST)
			if list_form.is_valid():
				change_list_element = get_object_or_404(List, id=req.get('id'))
				change_list_element.column_name = req.get('column_name')
				change_list_element.column_type = req.get('column_type')
				change_list_element.parameters = req.get('parameters')
				change_list_element.order = req.get('order') 
				if change_list_element.schema_id.author != request.user:
					return HttpResponseForbidden()
				change_list_element.save()
				schema = Schema.objects.get(id=change_list_element.schema_id.id)
				schema.status = 'ready_to_generate'
				schema.save()
				return HttpResponseRedirect(self.request.path_info)
		
		elif request.method== 'POST' and 'form_schema' in req:
			schema_form = SchemaForm(req)
			if schema_form.is_valid():
				edit_schema = get_object_or_404(Schema, id=pk)
				edit_schema.title = req.get('title')
				edit_schema.sepataror = req.get('sepataror')
				edit_schema.character = req.get('character')
				edit_schema.status = 'ready_to_generate'
				edit_schema.modified = date.today() 

				if edit_schema.author != request.user:
					return HttpResponseForbidden()
				edit_schema.save()
				return redirect('index_page')



class CsvSchema(LoginRequiredMixin, ListView):
	template_name = 'csv_schema.html'
	context_object_name = 'list_schemas'
	def get_queryset(self):
		return Schema.objects.filter(author=self.request.user)
	def post(self, request, **kwargs):
		# was a problem with values in list from request.POST
		# Meaning desapired there
		# and so there is code below
		form = request.POST
		val = 0
		
		print('user id!', self.request.user.id)
		for key in request.POST:
			valuelist = request.POST.getlist(key)
			for val in valuelist:
				if key == 'quantity' and val != '':
					print('val!', val)
					create_csv.delay(val , self.request.user.id)
					pass
		return redirect('csv_page')


class SaveCsv(View):
	def download_course(request, pk):
		schema_obj = Schema.objects.get(id=pk)
		path_to_file = schema_obj.link

		response = HttpResponse(mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' \
			% str(schema_obj.title)
		response['X-Sendfile'] = path_to_file
		return response