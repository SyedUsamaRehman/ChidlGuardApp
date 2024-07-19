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
from django.conf import settings


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
    if 'abnormal_values' in request.session:
        if len(request.session['abnormal_values'])==2:
            context['perspiration_sensor'] = json.dumps(request.session['abnormal_values'])
            request.session.pop('abnormal_values', None)

        elif len(request.session['abnormal_values'])==3:
            context['oximeter_values_graph'] = json.dumps(request.session['abnormal_values'])
            request.session.pop('abnormal_values', None)


        elif len(request.session['abnormal_values'])==4:
            print(request.session['abnormal_values'],"4th")
            context['accelo_meter_graph'] = json.dumps(request.session['abnormal_values'])
            print(context['accelo_meter_graph'])
            request.session.pop('abnormal_values', None)
               
            print(context['accelo_meter_graph'])


        
        # context.update(request.session['abnormal_values'])

    if csv_data.exists():
        context['message'] = "DataFound"
        for file in csv_data:
            if file.file_type == 'oximeter values graph' and file.is_latest:
                    context['oximeter_values_graph'] = json.dumps(process_csv(file.data_file))
            if file.file_type == 'accelo meter graph' and file.is_latest:
                    context['accelo_meter_graph'] = json.dumps(process_csv(file.data_file))
            
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
    
    # Limit the output to just 17 lines of timestamp data
    df_filtered = df_filtered.head(17)
    
    # Convert filtered DataFrame back to JSON format
    return df_filtered.to_dict(orient='records')















def check_abnormal_values(request, pk, graph_name):
    # Fetch the child and parent objects
    try:
        parent = Parent.objects.get(username=request.user.username)
        child = parent.children.get(pk=pk)

        print(child)
    except Parent.DoesNotExist or Child.DoesNotExist:
        return HttpResponse('Parent or child not found', status=404)
    
    # Retrieve the latest data file based on graph_name
    try:
        data_file = Csv_data.objects.filter(child=child, file_type=graph_name).latest('created_at')
        data = process_csv(data_file.data_file)  # Assuming process_csv returns a list of dicts
        last_entry = data[-1]  # Get the last entry
    except Csv_data.DoesNotExist:
        return HttpResponse('Data file not found', status=404)

    # Example abnormal value checks (adapt as needed)
    context={}
    abnormal = False
    if graph_name == 'oximeter values graph':
        if last_entry['SpO2 (%)'] < 95 or last_entry['Heart Rate (bpm)'] < 60:
            value={'Timestamp':last_entry['Timestamp'],'Heart Rate (bpm)':last_entry['SpO2 (%)'],'SpO2 (%)':last_entry['Heart Rate (bpm)']}
            # context={'oximeter_values_graph':value}

            abnormal = True
    elif graph_name == 'accelo meter graph':
        if (last_entry['X-axis (m/s^2)'] < -2 or last_entry['X-axis (m/s^2)'] > 2) or \
           (last_entry['Y-axis (m/s^2)'] < -2 or last_entry['Y-axis (m/s^2)'] > 2) or \
           (last_entry['Z-axis (m/s^2)'] < -2 or last_entry['Z-axis (m/s^2)'] > 2):
            value={'Timestamp':last_entry['Timestamp'],'X-axis (m/s^2)':last_entry['X-axis (m/s^2)'],'Y-axis (m/s^2)':last_entry['Y-axis (m/s^2)'],'Z-axis (m/s^2)':last_entry['Z-axis (m/s^2)']}
            # context={'accelo_meter_graph':value}
            
            abnormal = True
    elif graph_name == 'perspiration sensor':
        if last_entry['Perspiration Level (µS)'] < 0.5:
            value={'Timestamp':last_entry['Timestamp'] ,'Perspiration Level (µS)':last_entry['Perspiration Level (µS)']}
            # context={'perspiration_sensor':value}

            abnormal = True

    if abnormal:
        # Send email to the parent
        print("ab")
        send_mail(
            'Abnormal Values Detected',
            f'Abnormal values detected in the latest data for child ID {child}.{graph_name},{value}',
            settings.EMAIL_HOST_USER,  # Replace with your email
            ['mohammadusamaz11@gmail.com','clientproductid@gmail.com'],       # Assuming Parent model has an email field
            fail_silently=False,
        )
        request.session['abnormal_values'] = value
        print(value,"this is")
        request.session['child_pk'] = pk
        request.session['graph_name'] = graph_name
    return redirect(f'getdata', pk=pk)    