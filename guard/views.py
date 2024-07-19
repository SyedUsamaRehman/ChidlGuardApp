from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from datetime import timedelta,datetime
import json
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Parent, Child, Csv_data
from .utils import csv_to_dict
import pandas as pd

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    login(request, user)
                    return redirect('dashboard')
                except:
                    return redirect('dashboard')
            else:
                msg = 'Invalid credentials'
                print(msg)
        else:
            msg = 'Error validating the form'

    return render(request, "guard/login.html", {"form": form, "msg": msg})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    parent = Parent.objects.get(username=request.user.username)
    children = parent.children.all()
    return render(request, "guard/dashboard.html", {'parent': parent, 'children': children})

@login_required
def get_data(request, pk):
    parent = Parent.objects.get(username=request.user.username)
    child = Child.objects.get(id=pk, parent=parent)
    children = parent.children.all()

    csv_data = Csv_data.objects.filter(child=child).order_by('created_at')[:3]
    context = {'parent': parent, 'children': children,"childpk":child.pk}
    print(csv_data)
    if csv_data.exists():
        context['message'] = "DataFound"
        for file in csv_data:
            if file.file_type == 'oximeter values graph' and file.is_latest:
                context['oximeter_values_graph'] = json.dumps(process_csv(file.data_file))
            if file.file_type == 'ppG sensor graph' and file.is_latest:
                context['ppG_sensor_graph'] = json.dumps(process_csv(file.data_file))
            
            if file.file_type == 'perspiration sensor' and file.is_latest:
                context['perspiration_sensor'] = json.dumps(process_csv(file.data_file))

    else:
        context['message'] = "DataNotFound"

    return render(request, "guard/graphs.html", context)






import pandas as pd
from datetime import datetime, timedelta
def process_csv(file):
    # Load the CSV file
    df = pd.read_csv(file)
    
    # Ensure the 'Timestamp' column is in datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    
    # Calculate the date 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    # Convert 'seven_days_ago' to pandas Timestamp for compatibility
    seven_days_ago = pd.Timestamp(seven_days_ago)

    # Filter data for the last 7 days
    df_filtered = df[df['Timestamp'] >= seven_days_ago]
    
    # Convert 'Timestamp' column to string for JSON serialization
    df_filtered['Timestamp'] = df_filtered['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Convert filtered DataFrame back to JSON format
    return df_filtered.to_dict(orient='records')














@csrf_exempt
def check_abnormal_values(request):
    if request.method == 'POST':
        child_pk = request.POST.get('child_pk')
        graph_name = request.POST.get('graph_name')

        # Map graph names to file types
        file_type_map = {
            'oximeter': 'oximeter values graph',
            'accelerometer': 'accelerometer values graph',
            'perspiration': 'perspiration sensor'
        }

        file_type = file_type_map.get(graph_name)
        if not file_type:
            return JsonResponse({'status': 'error', 'message': 'Invalid graph name'})

        child = get_object_or_404(Child, pk=child_pk)
        today = datetime.now().strftime('%Y-%m-%d')
        data_file = Csv_data.objects.filter(child=child, file_type=file_type, created_at__date=today, is_latest=True).first()

        if not data_file:
            return JsonResponse({'status': 'error', 'message': 'No data file found'})

        # Process the CSV file
        data = processing_csv(data_file.data_file)

        if not data:
            return JsonResponse({'status': 'error', 'message': 'No data available in the file'})

        # Mark the latest data entry as abnormal
        latest_entry = data[-1]  # Get the last data entry

        # Notify parents
        notify_parents(child, graph_name, latest_entry)

        return JsonResponse({'status': 'success', 'message': 'Abnormal value flagged and notification sent.'})

def processing_csv(file):
    df = pd.read_csv(file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    return df.to_dict(orient='records')

def notify_parents(child, sensor_type, data_entry):
    parents = Parent.objects.filter(children=child)
    subject = f"Abnormal {sensor_type.capitalize()} Data Detected"
    message = f"Dear Parent,\n\nAn abnormal {sensor_type} data entry has been detected for your child {child.name}.\n\nDetails:\n{data_entry}\n\nPlease review the data and consult with a healthcare provider if necessary.\n\nBest regards,\nChildGuard Team"

    for parent in parents:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [parent.email],
            fail_silently=False,
        )