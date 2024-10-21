from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm

# List view for all customers
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

# View to create a new customer
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form})

# View to update an existing customer
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    projects = customer.projects.all()
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'projects': projects})

# View to delete a customer
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})

# List all projects of a specific customer
def customer_project_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    projects = customer.projects.all()
    return render(request, 'projects/customer_project_list.html', {'customer': customer, 'projects': projects})



