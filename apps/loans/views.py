from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Loan
from django.utils import timezone # Import timezone
from .forms import LoanForm, LoanEditForm
from apps.accounts.decorators import groups_required

@login_required
def loan_list(request):
    """
    Muestra una lista de todos los préstamos, con opciones de filtrado por estado.
    Calcula y muestra métricas generales sobre los préstamos.
    """
    all_loans = Loan.objects.select_related("asset", "user").all()

    # Obtener parámetros de filtrado de la solicitud GET.
    status_query = request.GET.get('status', '')

    # Aplicar filtro de estado si se proporciona.
    if status_query:
        all_loans = all_loans.filter(status=status_query)

    prestamos = all_loans
    overdue_loans = [loan for loan in prestamos if loan.is_overdue]

    # Calcular métricas para las tarjetas.
    total_loans = prestamos.count()
    active_loans = prestamos.filter(status="Activo").count()
    returned_loans = prestamos.filter(status="Devuelto").count()

    is_admin_or_staff = request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Staff']).exists()

    context = {
        "prestamos": prestamos,
        "overdue_loans": overdue_loans,
        "status_query": status_query,
        "total_loans": total_loans,
        "active_loans": active_loans,
        "returned_loans": returned_loans,
        "loan_statuses": Loan._meta.get_field('status').choices,
        "is_admin_or_staff": is_admin_or_staff,
        "now": timezone.now(), # Pass timezone.now() to the template context
    }
    return render(request, "loans/loan_list.html", context)

@groups_required(['Admin', 'Staff'])
def loan_create(request):
    """
    Crea un nuevo préstamo y actualiza el estado del activo asociado a 'en_uso'.
    """
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.status = "Activo"
            
            # Actualizar el estado del activo a 'en_uso'
            asset = loan.asset
            asset.status = 'en_uso'
            asset.save()
            
            loan.save()
            return redirect("loan_list")
    else:
        form = LoanForm()
    return render(request, "loans/loan_form.html", {"form": form})

@groups_required(['Admin', 'Staff'])
def loan_edit(request, pk):
    """
    Edita un préstamo existente y gestiona la actualización del estado de los activos
    si el activo prestado cambia.
    """
    loan = get_object_or_404(Loan, pk=pk)
    original_asset = loan.asset

    if request.method == "POST":
        form = LoanEditForm(request.POST, instance=loan)
        if form.is_valid():
            updated_loan = form.save(commit=False)

            # Si el activo ha cambiado
            if original_asset != updated_loan.asset:
                # El activo original vuelve a estar disponible
                original_asset.status = 'disponible'
                original_asset.save()
                # El nuevo activo se marca como en uso
                updated_loan.asset.status = 'en_uso'
                updated_loan.asset.save()
            
            updated_loan.save()
            return redirect("loan_list")
    else:
        form = LoanEditForm(instance=loan)
    return render(request, "loans/loan_form.html", {"form": form})

@groups_required(['Admin', 'Staff'])
def loan_return(request, pk):
    """
    Marca un préstamo como devuelto, establece la fecha de devolución
    y actualiza el estado del activo asociado a 'disponible'.
    """
    loan = get_object_or_404(Loan, pk=pk)
    loan.status = 'Devuelto'
    loan.return_date = timezone.now()
    
    # Actualizar el estado del activo a 'disponible'
    asset = loan.asset
    asset.status = 'disponible'
    asset.save()
    
    loan.save()
    return redirect("loan_list")

@groups_required(['Admin', 'Staff'])
def loan_delete(request, pk):
    """
    Elimina un préstamo existente. Si el préstamo estaba activo,
    el activo asociado vuelve a estar 'disponible'.
    """
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == "POST":
        asset = loan.asset
        is_active_loan = loan.status == 'Activo'

        loan.delete()

        if is_active_loan:
            # Si el préstamo estaba activo, el activo vuelve a estar disponible
            asset.status = 'disponible'
            asset.save()
            
        return redirect("loan_list")
    return render(request, "loans/loan_confirm_delete.html", {"prestamo": loan})
