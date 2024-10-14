
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Health_Report
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

User = get_user_model()  # Get the custom user model


#---------------------------------------------------------------------------------------------------------------------------------------------------------
@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
def api_signup(request):
    if request.method == 'POST':
        # return JsonResponse({'error': 'Passwords do not match'}, status=400)
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.is_approved = False  # Admin needs to approve
            user.save()
            return JsonResponse({'message': 'Account created! Wait for admin approval.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def api_login(request):
    
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved:  # Check if the user is approved by the admin
                login(request, user)  # Log the user in (creates a session)

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return JsonResponse({
                    'message': 'Login successful!',
                    'access_token': access_token,
                    'refresh_token': str(refresh)
                }, status=200)
            else:
                return JsonResponse({'error': 'User is not approved by admin'}, status=403)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def api_health_report_view(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        # Fetch health reports for the authenticated user
        health_reports = Health_Report.objects.filter(user=request.user)
        data = [
            {
                'heart_rate': report.heart_rate,
                'blood_pressure': report.blood_pressure,
                'spo2': report.spo2,
                'breathing_rate': report.breathing_rate,
                'pro': report.pro,
                'hrv': report.hrv,
                'stress': report.stress,
                'sympathetic_ns': report.sympathetic_ns,
                'parasympathetic_ns': report.parasympathetic_ns,
                'current_date': report.current_date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
                'time' : report.current_time.strftime("%H:%M:%S")
            }
            for report in health_reports
        ]
        return JsonResponse(data, safe=False, status=200)


    if request.method == 'POST':
        data = request.POST
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
        
        if not request.user.is_approved:
            return JsonResponse({'error': 'User is not approved by admin'}, status=403)
        
        user = request.user  # Assuming logged-in user
        heart_rate = request.POST.get('heart_rate')
        blood_pressure = request.POST.get('blood_pressure')
        spo2 = request.POST.get('spo2')
        breathing_rate = request.POST.get('breathing_rate')
        pro = request.POST.get('pro')
        hrv = request.POST.get('hrv')
        stress = request.POST.get('stress')
        sympathetic_ns = request.POST.get('sympathetic_ns')
        parasympathetic_ns = request.POST.get('parasympathetic_ns')

        health_report = Health_Report(
            user=user,
            heart_rate=heart_rate,
            blood_pressure=blood_pressure,
            spo2=spo2,
            breathing_rate=breathing_rate,
            pro=pro,
            hrv=hrv,
            stress=stress,
            sympathetic_ns=sympathetic_ns,
            parasympathetic_ns=parasympathetic_ns,
            # current_date=timezone.now()  # Manually set current date
        )
        health_report.save()
        return JsonResponse({'message': 'datasend successfully'}, status=201)



    return JsonResponse({'error': 'Invalid request method'}, status=405)



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.is_approved = False  # Set to False for admin approval
                user.save()
                messages.success(request, 'Your account has been created! Please wait for admin approval.')
                return redirect('login')  # Redirect to login page
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved:  # Check for approval
                login(request, user)  # Built-in Django login function
                return redirect('home')  # Redirect to home or another page
            else:
                messages.error(request, 'Your account is not approved by the admin.')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    logout(request)  # This will clear the session
    return redirect('login')  # Redirect to login page after logout

@login_required
def home(request):
    return render(request, 'home.html')

