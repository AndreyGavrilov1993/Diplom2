# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Computer, Printing, Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .temp.temp import temp_bookprinting, temp_book, \
    temp_bookcomputer

def book(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, temp_book, {'bookings': bookings})

@login_required
def book_computer(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        available_computers = Computer.objects.filter(status='available', start_date__gte=start_date, end_date__lte=end_date)
        if available_computers.exists():
            computer = available_computers.first()
            computer.status = 'occupied'
            computer.start_date = start_date
            computer.end_date = end_date
            computer.save()
            booking = Booking.objects.create(user=request.user, computer=computer, start_date=start_date, end_date=end_date)
            messages.error(request, 'No available computers for the selected dates.')
            return redirect('book')
        else:
            computer = Computer.objects.create(status='aviable', start_date=start_date, end_date=end_date)
            booking = Booking.objects.create(user=request.user, computer=computer, start_date=start_date,
                                             end_date=end_date)
            messages.success(request, 'Computer booked successfully.')
            return redirect('book')
    return render(request, temp_bookcomputer)

@login_required
def book_printing(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        pages = request.POST['pages']
        printing = Printing.objects.create(pages=pages, start_date=start_date, end_date=end_date)
        booking = Booking.objects.create(user=request.user, printing=printing, start_date=start_date, end_date=end_date)
        messages.success(request, 'Printing booked successfully.')
        return redirect('book')
    return render(request, temp_bookprinting)

