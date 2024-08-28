from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from .models import CustomUser, CustomerMeasurements
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from .models import CustomerMeasurements
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
import json
from django.http import JsonResponse

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'my-account.html', {'register_email': ''})        
        user = CustomUser.objects.create_user(email=email, password=password)
        login(request, user)
        messages.success(request, 'Registration successful')
        return redirect('core:login_view')    
    return render(request, 'my-account.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)        
        if user is not None:
            login(request, user)
            if not user.first_name and not user.phone_number:  # Add other fields as needed
                return redirect('core:user_popup')  # Redirect to user_popup for first-time users
            else:
                return redirect('core:user_page')  # Redirect to user page for returning users
        else:
            messages.error(request, 'Invalid email or password')    
    return render(request, 'my-account.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect(reverse('core:login_view'))
@login_required
def my_account(request):
    return render(request, 'my-account.html')
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('fullName').split()[0]
        user.last_name = ' '.join(request.POST.get('fullName').split()[1:])
        user.phone_number = request.POST.get('phoneNumber')
        user.city = request.POST.get('city')
        user.pincode = request.POST.get('pincode')
        user.address = request.POST.get('address')
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('core:user_page')
    return redirect('core:user_page')
@login_required
def user_popup(request):
    print("user_popup view called")
    print("Request method:", request.method)
    if request.method == 'POST':
        print("POST data:", request.POST)
        user = request.user
        print("Current user:", user)        
        # Update user fields
        user.first_name = request.POST.get('fullName', '').split()[0]
        user.last_name = ' '.join(request.POST.get('fullName', '').split()[1:])
        user.phone_number = request.POST.get('phoneNumber', '')
        user.city = request.POST.get('city', '')
        user.pincode = request.POST.get('pincode', '')
        user.address = request.POST.get('address', '')
        try:
            user.save()
            print("User saved successfully")
            messages.success(request, 'Profile updated successfully')
            return redirect('core:user_page') 
        except Exception as e:
            print("Error saving user:", str(e))
            messages.error(request, f'Error updating profile: {str(e)}')    
    return render(request, 'user_popup.html', {'user': request.user})
@login_required
def user_page(request):
    has_measurements = CustomerMeasurements.objects.filter(customer=request.user).exists()
    context = {        'has_measurements': has_measurements    }
    return render(request, 'user_page.html', context)
@login_required
def edit_user_details(request):
    if request.method == 'POST':
        user = request.user        
        # Update fields only if they are provided and not empty
        name = request.POST.get('name', '').strip()
        if name:
            user.first_name = name.split()[0]
            user.last_name = ' '.join(name.split()[1:])        
        phone = request.POST.get('phone', '').strip()
        if phone:
            user.phone_number = phone        
        city = request.POST.get('city', '').strip()
        if city:
            user.city = city        
        pincode = request.POST.get('pincode', '').strip()
        if pincode:
            user.pincode = pincode        
        address = request.POST.get('address', '').strip()
        if address:
            user.address = address
        if 'image-upload' in request.FILES:
            user.profile_picture = request.FILES['image-upload']
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('core:user_page')
    return render(request, 'edit_user_details.html', {'user': request.user})
@login_required
@require_POST
def update_profile_picture(request):
    if 'profile_picture' in request.FILES:
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        return JsonResponse({'success': True, 'image_url': user.profile_picture.url})
    return JsonResponse({'success': False})
@login_required
@require_POST
def delete_account(request):
    user = request.user
    user.delete()
    logout(request)
    return JsonResponse({'success': True})

def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def blog(request):
    return render(request, 'blog.html')
def contact(request):
    return render(request, 'contact.html')
def get_recommendations(request):
    # get user measurements and style preferences
    # generate recommendations using collaborative filtering and KNN
    # return recommendations to user
    return render(request,'recommendations.html')
@login_required
def submit_measurements(request):
    if request.method == 'POST':
        try:
            measurements = CustomerMeasurements.objects.get(customer=request.user)
        except CustomerMeasurements.DoesNotExist:
            measurements = CustomerMeasurements(customer=request.user)
        fields = ['height', 'torso', 'chest', 'waist', 'neck', 'sleeve', 'inseam', 'hip']        
        for field in fields:
            value = request.POST.get(field)
            if value:
                try:
                    setattr(measurements, field, float(value))
                except ValueError:
                    messages.error(request, f"Invalid value for {field}. Please enter a number.")
                    return render(request, 'measurements.html')
            else:
                messages.error(request, f"{field.capitalize()} is required.")
                return render(request, 'measurements.html')
        try:
            measurements.save()
            messages.success(request, "Measurements saved successfully.")
            return redirect('core:user_page')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'measurements.html')
    return render(request, 'measurements.html')
@login_required
def edit_measurements(request):
    measurements = CustomerMeasurements.objects.filter(customer=request.user)
    if measurements.count() > 1:
        # Keep the most recent one and delete others
        latest = measurements.latest('id')
        measurements.exclude(id=latest.id).delete()
        measurements = latest
    elif measurements.exists():
        measurements = measurements.first()
    else:
        measurements = CustomerMeasurements(customer=request.user)
    if request.method == 'POST':
        measurements.height = request.POST.get('height')
        measurements.torso = request.POST.get('torso')
        measurements.chest = request.POST.get('chest')
        measurements.waist = request.POST.get('waist')
        measurements.neck = request.POST.get('neck')
        measurements.sleeve = request.POST.get('sleeve')
        measurements.inseam = request.POST.get('inseam')
        measurements.hip = request.POST.get('hip')
        measurements.save()
        messages.success(request, 'Measurements updated successfully.')
        return redirect('core:user_page')
    return render(request, 'edit_measurements.html', {'measurements': measurements})
def view_measurements(request):
    measurements = CustomerMeasurements.objects.get(user=request.user)
    return render(request, 'view_measurements.html', {'measurements': measurements})

@staff_member_required
def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    total_measurements = CustomerMeasurements.objects.count()
    users_with_measurements = CustomUser.objects.annotate(measurement_count=Count('measurements')).filter(measurement_count__gt=0).count()
    
    context = {
        'total_users': total_users,
        'total_measurements': total_measurements,
        'users_with_measurements': users_with_measurements,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def admin_user_view(request):
    users = CustomUser.objects.filter(is_staff=False, is_superuser=False)
    context = {
        'users': users,
    }
    return render(request, 'admin_user.html', context)

@login_required
@require_http_methods(["PUT", "DELETE"])
def user_api(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            if 'name' in data:
                name_parts = data['name'].split(maxsplit=1)
                user.first_name = name_parts[0] if name_parts else ''
                user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            if 'email' in data:
                user.email = data['email']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']
            if 'city' in data:
                user.city = data['city']
            user.save()
            return JsonResponse({
                'success': 'User updated successfully',
                'name': user.get_full_name(),
                'email': user.email,
                'phone_number': user.phone_number,
                'city': user.city
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            with transaction.atomic():
                CustomerMeasurements.objects.filter(customer=user).delete()
                user.delete()
            return JsonResponse({'success': 'User and related data deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

