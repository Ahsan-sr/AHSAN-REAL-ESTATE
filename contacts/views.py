from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact


# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        #checking if user has already make an inquiry
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request,'You Have Already Made An Inquiry For This Listing')
                return redirect('/listings/'+listing_id)
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email,
        phone=phone, message=message, user_id=user_id)
        contact.save()
        #sending mail
        send_mail(
            'AHSAN REAL ESTATE',
           'There Has Been An Inquiry For ' + listing + '. Sign Into Admin Panel For More Info',
            'ahsanullah2452000@gmail.com',
            [realtor_email,'ahsanullah2452000@gmail.com'],
            fail_silently=False)
        #send_mail('AHSAN REAL ESTATE','There Has Been An Inquiry For ' + listing + '. Sign Into Admin Panel For More Info', 'ahsanullah2452000@gmail.com', [realtor_email,'ahsanullah2452000@gmail.com'], fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
        messages.success(request, 'Your Request Has Been Submitted , A Realtor will Contact You Soon')
        return redirect('/listings/'+listing_id)
