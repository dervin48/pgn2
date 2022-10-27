from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import ServicioForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Servicio


class ServicioListView(ValidatePermissionRequiredMixin, ListView):
    model = Servicio
    template_name = 'servicio/list.html'
    permission_required = 'view_servicio'
    url_redirect = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Servicio.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Servicios'
        context['create_url'] = reverse_lazy('servicio_create')
        context['list_url'] = reverse_lazy('servicio_list')
        context['entity'] = 'Servicios'
        return context


class ServicioCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/create.html'
    success_url = reverse_lazy('servicio_list')
    url_redirect = success_url
    permission_required = 'add_servicio'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ServicioUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/create.html'
    success_url = reverse_lazy('servicio_list')
    url_redirect = success_url
    permission_required = 'change_servicio'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ServicioDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Servicio
    template_name = 'servicio/delete.html'
    success_url = reverse_lazy('servicio_list')
    url_redirect = success_url
    permission_required = 'delete_servicio'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = self.success_url
        return context
