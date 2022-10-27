from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import CargoForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Cargo


class CargoListView(ValidatePermissionRequiredMixin, ListView):
    model = Cargo
    template_name = 'cargo/list.html'
    permission_required = 'view_cargo'
    url_redirect = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Cargo.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cargo'
        context['create_url'] = reverse_lazy('cargo_create')
        context['list_url'] = reverse_lazy('cargo_list')
        context['entity'] = 'Cargos'
        return context


class CargoCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargo/create.html'
    success_url = reverse_lazy('cargo_list')
    url_redirect = success_url
    permission_required = 'add_cargo'

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
        context['title'] = 'Creación de un Cargo'
        context['entity'] = ''
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CargoUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargo/create.html'
    success_url = reverse_lazy('cargo_list')
    url_redirect = success_url
    permission_required = 'change_cargo'

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
        context['title'] = 'Edición de un Cargo'
        context['entity'] = 'Cargo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CargoDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Cargo
    template_name = 'cargo/delete.html'
    success_url = reverse_lazy('cargo_list')
    url_redirect = success_url
    permission_required = 'delete_cargo'

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
        context['title'] = 'Eliminación de una Cargo'
        context['entity'] = 'Cargo'
        context['list_url'] = self.success_url
        return context
