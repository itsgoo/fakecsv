from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from fakecsv_app.models import Schema, List


class Authform(AuthenticationForm, forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

class SchemaForm(forms.ModelForm):
	class Meta:
		model = Schema
		fields = {"character", "sepataror", "title"}
		field_order = {"title", "sepataror", "character"}
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control  mb-3'
			

class ListForm(forms.ModelForm):
	class Meta:
		model = List
		fields = {'column_name', 'column_type', 'parameters', 'order',}
		field_order = ["order", "parameters", "column_type", "column_name"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'
			

class EmptyListForm(forms.ModelForm):
	class Meta:
		model = List
		fields = {'column_name', 'column_type', 'parameters', 'order',}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'
		
