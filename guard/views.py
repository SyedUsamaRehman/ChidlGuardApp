from django.shortcuts import render
from django.shortcuts import render, redirect,HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Parent,Child,Csv_data
from django.contrib.auth.models import User
from .utils import csv_to_dict
import pandas as pd

# Create your views here.



def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "guard/login.html", {"form": form, "msg": msg})

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    print(request.user)

    user=User.objects.get(username=request.user)
    # print(user.username)
    parent = Parent.objects.get(user=user.id)
    # print(parent)

    children = parent.children.all()
    # print(children.id)
    return render(request, "guard/dashboard.html", {'parent': parent, 'children': children})



def get_data(request,pk):

    user=User.objects.get(username=request.user)
    # print(user.username)
    parent = Parent.objects.get(user=user.id)
    # print(parent)
    user=User.objects.get(username=request.user)
    child=Child.objects.get(id=pk,parent=parent.id)
    children = parent.children.all()

    print(child)
    # csv_data=Csv_data.objects.filter(child=child,filetype='Oximeter Values Graph').order_by('created_at')[:1]
    csv_data=Csv_data.objects.filter(child=child.pk).order_by('created_at')[:3]
    context={'parent': parent, 'children': children}
    print(csv_data)
    if csv_data.exists():
        context['message']="DataFound"        
        print("this is running")
        for file in csv_data:
            if file.file_type=='oximeter values graph':
                context['oximeter_values_graph']=file.data_file
            if file.file_type=='ppG sensor graph':
                context['ppG_sensor_graph']=file.data_file
            if file.file_type=='perspiration sensor':
                context['perspiration_sensor']=file.data_file
    else: 
            
        context['message']="DataNotFound"        
    files_data=[]
    graph={}
    # for keys in context['oximeter_values_graph']:
        # prin)

    #     for data in csv_data:
    #         file={}
    #         # print(data.data_file)
    #         file['filetypes']=data.file_type
    #         file['path']=data.data_file
    #         files_data.append(file)
    #         # print(files_data)
       
    # for i in range(0,len(files_data)):
    #     path=files_data[i]['path']
    #     filetype=files_data[i]['filetypes']
    #     print(filetype)
    #     file=pd.read_csv(path)
    #     columns_name=file.columns.to_list()
    #     data=file.to_dict()
    #     print(columns_name)
    #     graph[filetype]=data
        
    



        
    # timestamps=graph['perspiration sensor']['Timestamp']
    
    # prespsensor=graph['perspiration sensor']['Perspiration Level (µS)']

    # print(type(timestamps))

    # print(type(graph['oximeter values graph']['Timestamp']))
    # print(type(graph['oximeter values graph']['Heart Rate (bpm)']))
    # print(type(graph['oximeter values graph']['SpO2 (%)']))


    # print(type(graph['ppG sensor graph']['Timestamp']))
    # print(type(graph['ppG sensor graph']['X-axis (m/s^2)']))
    # print(type(graph['ppG sensor graph']['Y-axis (m/s^2)']))
    # print(type(graph['ppG sensor graph']['Z-axis (m/s^2)']))


    
        
    # return HttpResponse("hello")
    return render(request, "guard/graphs.html",context )



