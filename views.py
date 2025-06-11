from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

def customer_form(request):
    # Check if editing from session
    is_edit = request.session.get('is_edit', False)
    customer_id = request.session.get('customer_id', None)
    customer = None

    if is_edit and customer_id:
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            # Clear session if customer not found
            if 'is_edit' in request.session:
                del request.session['is_edit']
            if 'customer_id' in request.session:
                del request.session['customer_id']
            is_edit = False
            customer_id = None

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        equipment = request.POST.get('equipment')
        issue = request.POST.get('issue')

        # Validation
        errors = {}
        if not name:
            errors['name'] = "Name is required."
        if not address:
            errors['address'] = "Address is required."
        if not phone or not re.match(r'^\+?1?\d{9,15}$', phone):
            errors['phone'] = "Enter a valid phone number (9-15 digits)."
        try:
            validate_email(email)
            if is_edit and customer:
                if Customer.objects.filter(email=email).exclude(pk=customer_id).exists():
                    errors['email'] = "This email is already registered."
            else:
                if Customer.objects.filter(email=email).exists():
                    errors['email'] = "This email is already registered."
        except ValidationError:
            errors['email'] = "Enter a valid email address."
        if not equipment:
            errors['equipment'] = "Equipment is required."
        if not issue:
            errors['issue'] = "Issue description is required."

        if not errors:
            if is_edit and customer:
                # Update existing customer
                customer.name = name
                customer.address = address
                customer.phone = phone
                customer.email = email
                customer.equipment = equipment
                customer.issue = issue
                customer.save()
                # Clear session data after successful update
                if 'is_edit' in request.session:
                    del request.session['is_edit']
                if 'customer_id' in request.session:
                    del request.session['customer_id']
                return redirect('customer_list')
            else:
                # Create new customer
                customer = Customer(
                    name=name,
                    address=address,
                    phone=phone,
                    email=email,
                    equipment=equipment,
                    issue=issue
                )
                customer.save()
                # Clear session data after successful creation
                if 'is_edit' in request.session:
                    del request.session['is_edit']
                if 'customer_id' in request.session:
                    del request.session['customer_id']
                return redirect('customer_list')

        # Return form with errors and entered data
        return render(request, 'customer_form.html', {
            'errors': errors,
            'name': name,
            'address': address,
            'phone': phone,
            'email': email,
            'equipment': equipment,
            'issue': issue,
            'is_edit': is_edit,
            'customer': customer
        })

    # Clear session if explicitly canceling
    if request.GET.get('action') == 'cancel':
        if 'is_edit' in request.session:
            del request.session['is_edit']
        if 'customer_id' in request.session:
            del request.session['customer_id']
        return redirect('customer_list')

    # Pre-populate form with customer data if editing
    context = {'is_edit': is_edit}
    if customer:
        context.update({
            'name': customer.name,
            'address': customer.address,
            'phone': customer.phone,
            'email': customer.email,
            'equipment': customer.equipment,
            'issue': customer.issue
        })
    return render(request, 'customer_form.html', context)

def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    return render(request, 'customer_list.html', {'customers': customers, 'query': query})

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    # Store customer data in session
    request.session['is_edit'] = True
    request.session['customer_id'] = customer.pk
    return redirect('customer_form')

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customer_list.html', {'customer': customer})