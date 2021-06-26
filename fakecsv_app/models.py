from django.db import models
from django.contrib.auth.models import User

import os


class Schema(models.Model):
	status_types= (
		('ready_to_generate', 'ready to generate'),
		('processing', 'processing'),
		('ready_to_download', 'ready to download'),
	)
	author = models.ForeignKey(User, on_delete=models.CASCADE, 
		verbose_name='schemas owner', blank=True, null=True)
	title = models.CharField(max_length=30, verbose_name='schemas title')
	sepataror = models.CharField(max_length=30, verbose_name='columns separator')
	character = models.CharField(max_length=30, verbose_name='string character')
	modified = models.DateField(auto_now=True)
	status = models.CharField(choices=status_types, max_length=30, 
		verbose_name='schemas type')
	link = models.CharField(max_length=30, verbose_name='schemas link')

	def __str__(self):
		str_name = self.title + ' id-' + str(self.id)
		return str_name

class List(models.Model):
	column_types = (
		('full_name', 'Full name'),
		('Job', 'Job'),
		('Email', 'Email'),
		('domain_name', 'Domain name'),
		('phone_number', 'Phone number'),
		('company_name', 'Company name'),
		('text', 'Text'),
		('integer', 'Integer'),
		('address', 'Address'),
		('date', 'Date'),
	)
	column_name = models.CharField(max_length=30, verbose_name='column name')
	column_type = models.CharField(choices=column_types, 
		max_length=30, verbose_name='columns type')
	parameters = models.CharField(max_length=30, 
		verbose_name='parameters', blank=True, null=True)
	order = models.IntegerField(verbose_name='order')
	schema_id = models.ForeignKey(Schema, on_delete=models.CASCADE, 
		verbose_name='list of schema', blank=True, null=True)
	
	def __str__(self):
		str_name = 'id-' + str(self.id) + ' ' + self.column_name
		return str_name

# when i changed structure of database i cant delete part of code of last model
def file_path(instance, filename):
	path = 'csv_files'
	format = 'name-' + filename
	return os.path.join(path, format)
