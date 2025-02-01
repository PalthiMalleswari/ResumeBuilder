from django.contrib import admin
from .models import *

@admin.register(ResumeMaster)
class ResumeMasterAdmin(admin.ModelAdmin):
    list_display = ('resume_id', 'resume_name', 'has_image', 'created_at', 'updated_at')
    search_fields = ('resume_name',)
    list_filter = ('created_at', 'updated_at')

    def has_image(self, obj):
        return bool(obj.resume_image)
    has_image.boolean = True

@admin.register(SectionMaster)
class SectionMasterAdmin(admin.ModelAdmin):
    list_display = ('section_id','section_name','section_created_by','section_modified_by')
    search_fields = ('section_id',)

@admin.register(FieldMaster)
class FieldMasterAdmin(admin.ModelAdmin):
    list_display = ('field_id','field_name','field_type','field_created_by','field_modified_by','active_status')
    search_fields = ('field_id',)

@admin.register(ResumeSectionMapping)
class ResumeSectionMappingAdmin(admin.ModelAdmin):
    list_display = ('resume_field_id','resume_id','section_id','field_id','section_order','field_order','active_status')
    search_fields = ('resume_field_id',)

    




