# Generated by Django 5.1.4 on 2025-01-18 13:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeMaster',
            fields=[
                ('resume_id', models.AutoField(primary_key=True, serialize=False)),
                ('resume_name', models.CharField(max_length=255)),
                ('resume_image', models.ImageField(blank=True, null=True, upload_to='resume_templates/')),
                ('resume_meta_info', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'resume_master',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SectionMaster',
            fields=[
                ('section_id', models.AutoField(primary_key=True, serialize=False)),
                ('section_name', models.CharField(max_length=100)),
                ('section_description', models.TextField(blank=True, null=True)),
                ('section_creation_time', models.DateTimeField(auto_now_add=True)),
                ('section_modified_time', models.DateTimeField(auto_now=True)),
                ('active_status', models.BooleanField(default=True)),
                ('has_subsections', models.BooleanField(default=False)),
                ('section_created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_sections', to=settings.AUTH_USER_MODEL)),
                ('section_modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_sections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'section_master',
                'ordering': ['section_name'],
            },
        ),
        migrations.CreateModel(
            name='ResumeSectionMapping',
            fields=[
                ('resume_field_id', models.AutoField(primary_key=True, serialize=False)),
                ('field_required', models.BooleanField(default=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('meta_info', models.JSONField(blank=True, null=True)),
                ('active_status', models.BooleanField(default=True)),
                ('section_order', models.IntegerField(default=0)),
                ('resume_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templts.resumemaster')),
                ('section_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templts.sectionmaster')),
            ],
            options={
                'db_table': 'resume_section_mapping',
                'ordering': ['section_order', 'section_id__section_name'],
            },
        ),
        migrations.CreateModel(
            name='SubSectionMaster',
            fields=[
                ('subsection_id', models.AutoField(primary_key=True, serialize=False)),
                ('subsection_name', models.CharField(max_length=100)),
                ('subsection_description', models.TextField(blank=True, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('active_status', models.BooleanField(default=True)),
                ('display_order', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_subsections', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_subsections', to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsections', to='templts.sectionmaster')),
            ],
            options={
                'db_table': 'subsection_master',
                'ordering': ['section', 'display_order', 'subsection_name'],
            },
        ),
    ]
