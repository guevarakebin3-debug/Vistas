from django.test import TestCase
from django.urls import reverse

from .models import Cargo, Empleado


class ListaExportSearchTests(TestCase):
    def setUp(self):
        cargo = Cargo.objects.create(nombre='Desarrollo', descripcion='Equipo de software')
        Empleado.objects.create(
            nombres='Ana',
            apellidos='Pérez',
            correo='ana@example.com',
            sueldo='1200.00',
            fecha_ingreso='2024-01-05',
            cargo=cargo,
        )
        Empleado.objects.create(
            nombres='Luis',
            apellidos='García',
            correo='luis@example.com',
            sueldo='1500.00',
            fecha_ingreso='2024-02-01',
            cargo=cargo,
        )

    def test_empleado_search_filters_results(self):
        response = self.client.get(reverse('fbv_empleado_list'), {'q': 'ana'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana')
        self.assertNotContains(response, 'Luis')

    def test_empleado_export_pdf(self):
        response = self.client.get(reverse('fbv_empleado_list'), {'q': 'ana', 'export': 'pdf'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
