from django.contrib import admin

from cprompt.darulez.models import School, Application, DocumentRule, DocumentRequest


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
  list_display = ['name']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
  list_display = ['id', 'school']
  raw_id_fields = ('school',)


@admin.register(DocumentRule)
class DocRuleAdmin(admin.ModelAdmin):
  list_display = ['school', 'action']
  raw_id_fields = ('school',)

@admin.register(DocumentRequest)
class DocRequestAdmin(admin.ModelAdmin):
  list_display = ['application', 'created', 'sent']
  raw_id_fields = ('application',)
