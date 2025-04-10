from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import CustomUser, UserProfile, OTP
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import CustomUser, UserProfile, OTP
def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']  # full name
        mobile = request.POST['mobile']
        email = request.POST['email']
        address = request.POST['address']
        aadhar = request.POST['aadhar']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(username=mobile).exists() or UserProfile.objects.filter(email=email).exists():
            messages.error(request, "User already exists.")
            return redirect('register')

        # Split full name into first and last name
        name_parts = name.strip().split()
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        # Save to session
        request.session['user_data'] = {
            'name': name,
            'mobile': mobile,
            'email': email,
            'address': address,
            'aadhar': aadhar,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }

        # Generate OTP
        otp = OTP.generate_otp()
        OTP.objects.create(mobile=mobile, otp=otp)

        # Send OTP via email
        try:
            send_mail(
                subject='Your OTP for Smart Finance Registration',
                message=f'Hi {name},\n\nYour OTP is: {otp}\n\nPlease enter this OTP to verify your registration.',
                from_email='your_email@gmail.com',  # Replace with your real email
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f"Failed to send OTP email: {e}")
            return redirect('register')

        messages.info(request, "An OTP has been sent to your email.")
        return redirect('verify_otp')

    return render(request, 'register.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        user_data = request.session.get('user_data')

        if not user_data:
            messages.error(request, "Session expired.")
            return redirect('register')

        try:
            latest_otp = OTP.objects.filter(mobile=user_data['mobile']).latest('created_at')
        except OTP.DoesNotExist:
            messages.error(request, "OTP not found.")
            return redirect('register')

        if entered_otp == latest_otp.otp:
            # Create CustomUser
            custom_user = CustomUser.objects.create(
                username=user_data['mobile'],
                email=user_data['email'],
                password=make_password(user_data['password']),
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_user=True
            )

            # Create UserProfile
            UserProfile.objects.create(
                user=custom_user,
                name=user_data['name'],
                mobile=user_data['mobile'],
                email=user_data['email'],
                address=user_data['address'],
                aadhar=user_data['aadhar'],
                is_verified=True
            )

            messages.success(request, "Registration successful.")
            del request.session['user_data']
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')





def logout_view(request):
    logout(request)
    return redirect('login')
