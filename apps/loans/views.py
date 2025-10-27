from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Loan
from .forms import LoanForm
from apps.accounts.decorators import groups_required

@login_required
def loan_list(request):
    """
    Muestra una lista de todos los préstamos, con opciones de filtrado.

    Permite filtrar los préstamos por su estado ('Activo' o 'Devuelto').
    También calcula y muestra métricas generales sobre los préstamos.
    """
    all_loans = Loan.objects.select_related("asset", "user").all()

    # Obtener parámetros de filtrado de la solicitud GET.
    status_query = request.GET.get('status', '')

    # Aplicar filtro de estado si se proporciona.
    if status_query:
        all_loans = all_loans.filter(status=status_query)

    prestamos = all_loans

    # Calcular métricas para las tarjetas.
    total_loans = prestamos.count()
    active_loans = prestamos.filter(status="Activo").count()
    returned_loans = prestamos.filter(status="Devuelto").count()

    context = {
        "prestamos": prestamos,
        "status_query": status_query,
        "total_loans": total_loans,
        "active_loans": active_loans,
        "returned_loans": returned_loans,
        "loan_statuses": Loan._meta.get_field('status').choices,
    }
    return render(request, "loans/loan_list.html", context)

@groups_required(['Admin', 'Staff'])
def loan_create(request):
    """
    Crea un nuevo préstamo.

    Muestra un formulario para crear un nuevo préstamo y procesa los datos
    enviados.
    """
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loan_list")
    else:
        form = LoanForm()
    return render(request, "loans/loan_form.html", {"form": form})

@groups_required(['Admin', 'Staff'])
def loan_edit(request, pk):
    """
    Edita un préstamo existente.

    Muestra un formulario pre-rellenado para editar un préstamo
    identificado por su clave primaria (pk).
    """
    prestamo = get_object_or_404(Loan, pk=pk)
    if request.method == "POST":
        form = LoanForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect("loan_list")
    else:
        form = LoanForm(instance=prestamo)
    return render(request, "loans/loan_form.html", {"form": form})

@groups_required(['Admin', 'Staff'])
def loan_delete(request, pk):
    """
    Elimina un préstamo existente.

    Pide confirmación antes de eliminar un préstamo identificado por su
    clave primaria (pk).
    """
    prestamo = get_object_or_404(Loan, pk=pk)
    if request.method == "POST":
        prestamo.delete()
        return redirect("loan_list")
    return render(request, "loans/loan_confirm_delete.html", {"prestamo": prestamo})
