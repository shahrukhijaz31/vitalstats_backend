
from django.http import JsonResponse
from .models import Health_Report
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

User = get_user_model()  # Get the custom user model


@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
def api_signup(request):
    if request.method == 'POST':
        
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        role =  data.get('role')

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if username and email and password and role:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_approved = False  # Admin needs to approve
                user.user_role = role
                user.save()
                return JsonResponse({'message': 'Account created! Wait for admin approval.'}, status=201)
            except Exception as e:
                return JsonResponse({'error': "this username already exists"}, status=400)
        
        else:
            return JsonResponse({'error': 'Enter all fields again.'}, status=400)

    
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
@api_view(['GET'])
def api_health_report_get(request):
    if request.method == 'GET':
        try:
            auth = JWTAuthentication()
            user = auth.authenticate(request)  # User aur token dono ko extract karna
            if user is None:
                return JsonResponse({'Token is invalid or expired'}, status=401)

        except AuthenticationFailed:
            return JsonResponse({'Token is invalid or expired'}, status=401)
        
        if not request.user.is_approved:
            return JsonResponse({'error': 'User is not approved by admin'}, status=403)

        # Fetch health reports for the authenticated user
        health_reports = Health_Report.objects.filter(user=request.user)
        data = [
            {
                'pulse_rate': report.pulse_rate,
                'blood_pressure': report.blood_pressure,
                'mean_rri': report.mean_rri,
                'oxygen_saturation': report.oxygen_saturation,
                'hemoglobin': report.hemoglobin,
                'hrhemoglobin_a1cv': report.hrhemoglobin_a1cv,
                'lfhf': report.lfhf,
                'pns_index': report.pns_index,
                'pns_zone': report.pns_zone,
                'prq': report.prq,
                'rmssd': report.rmssd,
                'respiration_rate': report.respiration_rate,
                'sd1': report.sd1,
                'sd2': report.sd2,
                'sdnn': report.sdnn,
                'sns_index': report.sns_index,
                'sns_zone': report.sns_zone,
                'stress_level': report.stress_level,
                'stress_index': report.stress_index,
                'wellness_index': report.wellness_index,
                'wellness_level': report.wellness_level,
                'current_date': report.current_date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
                'time' : report.current_time.strftime("%H:%M:%S")
            }
            for report in health_reports
        ]
        return JsonResponse(data, safe=False, status=200)


@csrf_exempt
@api_view(['POST'])
def api_health_report_post(request):
    if request.method == 'POST':
        data = request.POST
        # JWT Authentication se token validate karna
        try:
            auth = JWTAuthentication()
            user = auth.authenticate(request)  # User aur token dono ko extract karna
            if user is None:
                return JsonResponse({'Token is invalid or expired'}, status=401)

        except AuthenticationFailed:
            return JsonResponse({'Token is invalid or expired'}, status=401)
        
        if not request.user.is_approved:
            return JsonResponse({'error': 'User is not approved by admin'}, status=403)
   
        user = request.user  # Assuming logged-in user
        pulse_rate = request.POST.get('pulse_rate')
        blood_pressure = request.POST.get('blood_pressure')
        mean_rri = request.POST.get('mean_rri')
        oxygen_saturation = request.POST.get('oxygen_saturation')
        hemoglobin = request.POST.get('hemoglobin')
        hrhemoglobin_a1cv = request.POST.get('hrhemoglobin_a1cv')
        lfhf = request.POST.get('lfhf')
        pns_index = request.POST.get('pns_index')
        pns_zone = request.POST.get('pns_zone')
        prq = request.POST.get('prq')
        rmssd = request.POST.get('rmssd')
        respiration_rate = request.POST.get('respiration_rate')
        sd1 = request.POST.get('sd1')
        sd2 = request.POST.get('sd2')
        sdnn = request.POST.get('sdnn')
        sns_index = request.POST.get('sns_index')
        sns_zone = request.POST.get('sns_zone')
        stress_level = request.POST.get('stress_level')
        stress_index = request.POST.get('stress_index')
        wellness_index = request.POST.get('wellness_index')
        wellness_level = request.POST.get('wellness_level')

        health_report = Health_Report(
            user=user,
            pulse_rate=pulse_rate,
            blood_pressure=blood_pressure,
            mean_rri=mean_rri,
            oxygen_saturation=oxygen_saturation,
            hemoglobin=hemoglobin,
            hrhemoglobin_a1cv=hrhemoglobin_a1cv,
            lfhf=lfhf,
            pns_index=pns_index,
            pns_zone=pns_zone,
            prq=prq,
            rmssd=rmssd,
            respiration_rate=respiration_rate,
            sd1=sd1,
            sd2=sd2,
            sdnn=sdnn,
            sns_index=sns_index,
            sns_zone=sns_zone,
            stress_level = stress_level,
            stress_index=stress_index,
            wellness_index=wellness_index,
            wellness_level=wellness_level
        )
        health_report.save()
        return JsonResponse({'message': 'success'}, status=201)