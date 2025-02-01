from django.db import models
from django.contrib.auth.models import User

class ResumeMaster(models.Model):
    resume_id = models.AutoField(primary_key=True)
    resume_name = models.CharField(max_length=255)
    resume_image = models.ImageField(upload_to='resume_templates/', null=True, blank=True)
    resume_meta_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    rating = models.DecimalField(max_digits = 5,decimal_places=1,default=4.0)
    downloads = models.DecimalField(max_digits=5,decimal_places=3,default=3.0)
    ats = models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        db_table = 'resume_master'
        ordering = ['-created_at']

    def __str__(self):
        return self.resume_name

class SectionMaster(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=100)
    section_description = models.TextField(null=True, blank=True)
    section_creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    section_modified_time = models.DateTimeField(auto_now=True,null=True,blank=True)
    section_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_sections')
    section_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_sections')
    active_status = models.BooleanField(default=True)
    has_subsections = models.BooleanField(default=False)

    class Meta:
        db_table = 'section_master'
        ordering = ['section_name']

    def __str__(self):
        return self.section_name

class SubSectionMaster(models.Model):
    subsection_id = models.AutoField(primary_key=True)
    section = models.ForeignKey(SectionMaster, on_delete=models.CASCADE, related_name='subsections')
    subsection_name = models.CharField(max_length=100)
    subsection_description = models.TextField(null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    modified_time = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_subsections')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_subsections')
    active_status = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'subsection_master'
        ordering = ['section', 'display_order', 'subsection_name']

    def __str__(self):
        return f"{self.section.section_name} - {self.subsection_name}"
    
class FieldMaster(models.Model):
    field_id = models.AutoField(primary_key=True)
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100)
    field_creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    field_modified_time = models.DateTimeField(auto_now=True,null=True,blank=True)
    field_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_fields')
    field_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_fields')
    active_status = models.BooleanField(default=True)
    

    class Meta:
        db_table = 'field_master'
        ordering = ['field_name']

    def __str__(self):
        return self.field_name

class ResumeSectionMapping(models.Model):
    resume_field_id = models.AutoField(primary_key=True)
    resume_id = models.ForeignKey(ResumeMaster, on_delete=models.CASCADE)
    section_id = models.ForeignKey(SectionMaster, on_delete=models.CASCADE)
    field_id = models.ForeignKey(FieldMaster, on_delete=models.CASCADE)
    field_required = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    modified_time = models.DateTimeField(auto_now=True,null=True,blank=True)
    meta_info = models.JSONField(null=True, blank=True)
    active_status = models.BooleanField(default=True)
    section_order = models.IntegerField(default=0)
    field_order = models.IntegerField(default=0)
    
    

    class Meta:
        db_table = 'resume_section_mapping'
        ordering = ['section_order', 'section_id__section_name']

    def save(self, *args, **kwargs):
        if self.section_order == 0:  # Auto-assign order if not specified
            last_order = ResumeSectionMapping.objects.filter(
                resume_id=self.resume_id
            ).aggregate(models.Max('section_order'))['section_order__max']
            self.section_order = (last_order or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.resume_id.resume_name} - {self.section_id.section_name}"
    

