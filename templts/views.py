from django.shortcuts import render
from django.views.generic import ListView, DetailView,FormView, TemplateView
from .models import ResumeMaster
from django.urls import reverse_lazy
from .models import ResumeMaster, SectionMaster, ResumeSectionMapping, SubSectionMaster
from django import forms
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json,time
import os
from .services.latex_generator import LaTeXGenerator
from django.contrib.auth.mixins import LoginRequiredMixin


class ResumeListView(ListView):
    model = ResumeMaster
    template_name = 'templts/resume_list.html'
    context_object_name = 'resumes'
    paginate_by = 10

    def get_queryset(self):
        # Customize the queryset
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(resume_name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        # Add extra context
        context = super().get_context_data(**kwargs)
        context['total_resumes'] = self.model.objects.count()
        return context 
    


class ResumeDetailView(DetailView):
    model = ResumeMaster
    template_name = 'templts/resume_detail.html'
    context_object_name = 'resume'

def home(request):
    return render(request, 'templts/home.html') 


class DynamicResumeForm(forms.Form):
    def __init__(self, *args, resume_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if resume_id:
            sections = ResumeSectionMapping.objects.filter(
                resume_id=resume_id,
                active_status=True
            ).select_related('section_id').order_by('section_id__section_name')
            
            for section_mapping in sections:
                if section_mapping.section_id.has_subsections:
                    # Add a header for the main section
                    self.fields[f"section_{section_mapping.section_id.section_id}_header"] = forms.CharField(
                        widget=forms.HiddenInput(),
                        initial=section_mapping.section_id.section_name
                    )
                    
                    # Get subsections for this section
                    subsections = SubSectionMaster.objects.filter(
                        section=section_mapping.section_id,
                        active_status=True
                    ).order_by('display_order')
                    
                    # Create fields for each subsection
                    for subsection in subsections:
                        field_name = f"section_{section_mapping.section_id.section_id}_sub_{subsection.subsection_id}"
                        self.fields[field_name] = forms.CharField(
                            label=subsection.subsection_name,
                            required=section_mapping.field_required,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': f"Enter {subsection.subsection_name}"
                            })
                        )
                else:
                    field_name = f"section_{section_mapping.section_id.section_id}"
                    self.fields[field_name] = forms.CharField(
                        label=section_mapping.section_id.section_name,
                        required=section_mapping.field_required,
                        widget=forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': f"Enter {section_mapping.section_id.section_name}"
                        })
                    )
  

class UseTemplateView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'  # Specify the login URL
    template_name = 'templts/use_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume_id = self.kwargs.get('pk')
        
        # Get resume details
        resume = ResumeMaster.objects.get(pk=resume_id)
        
        # Get all sections for this resume
        sections_dict = {}
        resume_sections = ResumeSectionMapping.objects.filter(
            resume_id=resume_id,
            active_status=True
        ).select_related('section_id')
        sections_fields = resume_sections.order_by('section_order','field_order')

 
        for section_mapping in sections_fields:
            section = section_mapping.section_id
            if section.section_id not in sections_dict:
                
                sections_dict[section.section_id]={
                        'section_name':section.section_name,
                        'fields':[{'field_id':section_mapping.field_id.field_id,
                                    'field_name':section_mapping.field_id.field_name,   
                                    'field_required':section_mapping.field_required,
                                    'field_order':section_mapping.field_order,
                                    'field_type':section_mapping.field_id.field_type,
                                    }]}
                        
                    
            else:
                field_dict = {'field_id':section_mapping.field_id.field_id,
                'field_name':section_mapping.field_id.field_name,
                'field_required':section_mapping.field_required,
                'field_order':section_mapping.field_order,
                'field_type':section_mapping.field_id.field_type,
                    }
                sections_dict[section.section_id]['fields'].append(field_dict)
                

          
        
        context['resume'] = resume
        context['sections'] = sections_dict
        return context

@csrf_exempt
@require_http_methods(["POST"])
def generate_resume(request):
    try:
        # Parse form data
        data = json.loads(request.body)
        
        # Initialize LaTeX generator
        generator = LaTeXGenerator()
        
        
        # Generate LaTeX code
        latex_code = generator.generate_latex(data)

        cwd = os.getcwd()

      
        # Generate PDF
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_filename = f"resume_test.pdf"
        output_file_name_with_timestamp = f"{timestamp}_{output_filename}"

        output_path = os.path.join(cwd,'media', 'generated_resumes')
       
        
        if generator.generate_pdf(latex_code, output_path,output_file_name_with_timestamp):
            return JsonResponse({
                'success': True,
                'pdf_url': f'/media/generated_resumes/{output_file_name_with_timestamp}'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to generate PDF'
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
