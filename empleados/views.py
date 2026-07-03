from io import BytesIO

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .forms import CargoForm, EmpleadoForm
from .models import Cargo, Empleado


def home(request):
    return render(request, 'home.html')


def _get_search_query(request):
    return (request.GET.get('q') or '').strip()


def _filter_cargos(queryset, query):
    if query:
        return queryset.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
    return queryset


def _filter_empleados(queryset, query):
    if query:
        return queryset.filter(
            Q(nombres__icontains=query)
            | Q(apellidos__icontains=query)
            | Q(correo__icontains=query)
            | Q(cargo__nombre__icontains=query)
        )
    return queryset


def _build_pdf_response(title, headers, rows, filename):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=40, rightMargin=40,
                            topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.fontName = 'Helvetica-Bold'
    title_style.fontSize = 20
    title_style.leading = 24
    title_style.textColor = colors.HexColor('#1d4ed8')

    subtitle_style = styles['Normal']
    subtitle_style.fontSize = 10
    subtitle_style.leading = 14
    subtitle_style.textColor = colors.HexColor('#475569')

    date_style = styles['Normal']
    date_style.fontSize = 9
    date_style.textColor = colors.HexColor('#475569')
    date_style.alignment = 2

    story = [Paragraph(title, title_style), Spacer(1, 6)]
    story.append(Paragraph('Reporte generado automáticamente', subtitle_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'Fecha: {timezone.now().strftime("%Y-%m-%d %H:%M")}', date_style))
    story.append(Spacer(1, 18))

    table_data = [headers] + rows
    table = Table(table_data, repeatRows=1, hAlign='LEFT')
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1d4ed8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#eff6ff'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    table.setStyle(table_style)
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _build_excel_response(title, headers, rows, filename):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Datos'
    sheet.append([title])
    sheet.append(headers)
    for row in rows:
        sheet.append([str(value) if value is not None else '' for value in row])
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _export_cargos(queryset, export_type):
    headers = ['Nombre', 'Descripción']
    rows = [[cargo.nombre, cargo.descripcion or '—'] for cargo in queryset]
    if export_type == 'pdf':
        return _build_pdf_response('Cargos', headers, rows, 'cargos.pdf')
    return _build_excel_response('Cargos', headers, rows, 'cargos.xlsx')


def _export_empleados(queryset, export_type):
    headers = ['Nombres', 'Apellidos', 'Correo', 'Sueldo', 'Ingreso', 'Cargo']
    rows = [
        [
            empleado.nombres,
            empleado.apellidos,
            empleado.correo,
            str(empleado.sueldo),
            empleado.fecha_ingreso.strftime('%Y-%m-%d'),
            empleado.cargo.nombre,
        ]
        for empleado in queryset
    ]
    if export_type == 'pdf':
        return _build_pdf_response('Empleados', headers, rows, 'empleados.pdf')
    return _build_excel_response('Empleados', headers, rows, 'empleados.xlsx')





# ================= CARGO - BASADO EN FUNCIONES (VBF) =================

def cargo_list(request):
    query = _get_search_query(request)
    cargos = _filter_cargos(Cargo.objects.all(), query)
    export_type = request.GET.get('export')
    if export_type in {'pdf', 'excel'}:
        return _export_cargos(cargos, export_type)
    return render(request, 'cargo_list_fbv.html', {'cargos': cargos, 'query': query})


def cargo_create(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fbv_cargo_list')
    else:
        form = CargoForm()
    return render(request, 'cargo_form_fbv.html', {'form': form, 'titulo': 'Registrar cargo'})


def cargo_update(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('fbv_cargo_list')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'cargo_form_fbv.html', {'form': form, 'titulo': 'Editar cargo'})


def cargo_delete(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        cargo.delete()
        return redirect('fbv_cargo_list')
    return render(request, 'cargo_confirm_delete_fbv.html', {'cargo': cargo})


# ================= EMPLEADO - BASADO EN FUNCIONES (VBF) =================

def empleado_list(request):
    query = _get_search_query(request)
    empleados = _filter_empleados(Empleado.objects.select_related('cargo').all(), query)
    export_type = request.GET.get('export')
    if export_type in {'pdf', 'excel'}:
        return _export_empleados(empleados, export_type)
    return render(request, 'empleado_list_fbv.html', {'empleados': empleados, 'query': query})


def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fbv_empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'empleado_form_fbv.html', {'form': form, 'titulo': 'Registrar empleado'})


def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('fbv_empleado_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleado_form_fbv.html', {'form': form, 'titulo': 'Editar empleado'})


def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('fbv_empleado_list')
    return render(request, 'empleado_confirm_delete_fbv.html', {'empleado': empleado})


# ================= CARGO - BASADO EN CLASES (VBC) =================

class CargoListView(ListView):
    model = Cargo
    template_name = 'cargo_list_cbv.html'
    context_object_name = 'cargos'

    def get_queryset(self):
        queryset = Cargo.objects.all()
        query = (self.request.GET.get('q') or '').strip()
        return _filter_cargos(queryset, query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = (self.request.GET.get('q') or '').strip()
        return context

    def get(self, request, *args, **kwargs):
        export_type = request.GET.get('export')
        if export_type in {'pdf', 'excel'}:
            return _export_cargos(self.get_queryset(), export_type)
        return super().get(request, *args, **kwargs)


class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargo_form_cbv.html'
    success_url = reverse_lazy('cbv_cargo_list')
    extra_context = {'titulo': 'Registrar cargo'}


class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargo_form_cbv.html'
    success_url = reverse_lazy('cbv_cargo_list')
    extra_context = {'titulo': 'Editar cargo'}


class CargoDeleteView(DeleteView):
    model = Cargo
    template_name = 'cargo_confirm_delete_cbv.html'
    success_url = reverse_lazy('cbv_cargo_list')


# ================= EMPLEADO - BASADO EN CLASES (VBC) =================

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'empleado_list_cbv.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        queryset = Empleado.objects.select_related('cargo').all()
        query = (self.request.GET.get('q') or '').strip()
        return _filter_empleados(queryset, query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = (self.request.GET.get('q') or '').strip()
        return context

    def get(self, request, *args, **kwargs):
        export_type = request.GET.get('export')
        if export_type in {'pdf', 'excel'}:
            return _export_empleados(self.get_queryset(), export_type)
        return super().get(request, *args, **kwargs)


class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado_form_cbv.html'
    success_url = reverse_lazy('cbv_empleado_list')
    extra_context = {'titulo': 'Registrar empleado'}


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado_form_cbv.html'
    success_url = reverse_lazy('cbv_empleado_list')
    extra_context = {'titulo': 'Editar empleado'}


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'empleado_confirm_delete_cbv.html'
    success_url = reverse_lazy('cbv_empleado_list')
