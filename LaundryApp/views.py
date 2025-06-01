from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import numpy as np
import pymysql
import os
import matplotlib.pyplot as plt #use to visualize dataset vallues
import io
import base64
from datetime import date

import torch
import cv2
import pathlib
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

global uname
model = torch.hub.load('yolov5', 'custom', path='model/best.pt', force_reload=True,source='local')
global service, shirt, tshirt, shorts, pants, towels, suits, inner, kurta, paijama, skirt, address, delivery_date

def WriteDescriptionAction(request):
    if request.method == 'POST':
        global uname, utype, otp
        lid = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update laundry_service set delivery_status = '"+desc+"' where laundry_id='"+lid+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':'Delivery Task Completed'}
        return render(request, 'AdminScreen.html', context)

def WriteDescription(request):
    if request.method == 'GET':
        name = request.GET['name']
        output = '<tr><td><font size="" color="black">Laundry&nbsp;ID</b></td><td><input type="text" name="t1" size="15" value="'+name+'" readonly/></td></tr>'
        context= {'data1':output}
        return render(request, 'WriteDescription.html', context)  

def ViewOrderStatus(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Laundry ID</th><th><font size="" color="black">Owner Name</th><th><font size="" color="black">Laundry Date</th>'
        output+='<th><font size="" color="black">Service Type</th><th><font size="" color="black">Shirts</th>'
        output+='<th><font size="" color="black">T-Shirts</th><th><font size="" color="black">Shorts</th>'
        output+='<th><font size="" color="black">Pants</th><th><font size="" color="black">Towels</th>'
        output+='<th><font size="" color="black">Suits</th><th><font size="" color="black">Inner Wears</th>'
        output+='<th><font size="" color="black">Kurtas</th><th><font size="" color="black">Paijamas</th>'
        output+='<th><font size="" color="black">Skirts</th><th><font size="" color="black">Stain Result</th>'
        output+='<th><font size="" color="black">Delivery Date</th><th><font size="" color="black">Delivery Address</th>'
        output+='<th><font size="" color="black">Status</th><th><font size="" color="black">Image</th><th><font size="" color="black">Click Here for Description</th><tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from laundry_service")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td>'
                output+='<td><font size="" color="black">'+row[5]+'</td>'
                output+='<td><font size="" color="black">'+row[6]+'</td>'
                output+='<td><font size="" color="black">'+row[7]+'</td>'
                output+='<td><font size="" color="black">'+row[8]+'</td>'
                output+='<td><font size="" color="black">'+row[9]+'</td>'
                output+='<td><font size="" color="black">'+row[10]+'</td>'
                output+='<td><font size="" color="black">'+row[11]+'</td>'
                output+='<td><font size="" color="black">'+row[12]+'</td>'
                output+='<td><font size="" color="black">'+row[13]+'</td>'
                output+='<td><font size="" color="black">'+row[15]+'</td>'
                output+='<td><font size="" color="black">'+row[16]+'</td>'
                output+='<td><font size="" color="black">'+row[17]+'</td>'
                output+='<td><font size="" color="black">'+row[18]+'</td>'
                output+='<td><img src="static/files/'+row[14]+'" height="300" width="300"/></td>'
                if row[18] == 'Pending':
                    output+='<td><a href=\'WriteDescription?name='+str(row[0])+'\'><font size="" color="black">Click Here</a></td></tr>'
                else:
                    output+='<td><font size="" color="black">-</td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)        

def ViewCustomers(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Username</th><th><font size="" color="black">Password</th>'
        output+='<th><font size="" color="black">Contact No</th><th><font size="" color="black">Email ID</th>'
        output+='<th><font size="" color="black">Address</th><th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from register")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<tr><td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td></tr>'
               
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)   

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def AdminLoginAction(request):
    if request.method == 'POST':
        global uname, utype, otp
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'Welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'AdminLogin.html', context)

def predict(filename):
    global model
    img = cv2.imread(filename)
    img = cv2.resize(img, (512, 512))
    results = model(img)
    results.xyxy[0]  # im predictions (tensor)
    out = results.pandas().xyxy[0]  # im predictions (pandas)
    print(out)
    result = "Not Found"
    if len(out) > 0:
        for i in range(len(out)):
            xmin = int(out['xmin'].ravel()[i])
            ymin = int(out['ymin'].ravel()[i])
            xmax = int(out['xmax'].ravel()[i])
            ymax = int(out['ymax'].ravel()[i])
            name = out['name'].ravel()[i]
            confidence = float(out['confidence'].ravel()[i])
            if confidence > 0.80:
                result = "Found"
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                cv2.putText(img, name, (xmin, ymin-20), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    return img, result            

def UploadImageAction(request):
    if request.method == 'POST':
        global uname
        global service, shirt, tshirt, shorts, pants, towels, suits, inner, kurta, paijama, skirt, address, delivery_date
        today = str(date.today())
        image = request.FILES['t1']
        imagename = request.FILES['t1'].name
        fs = FileSystemStorage()
        if os.path.exists('LaundryApp/static/files/'+imagename):
            os.remove('LaundryApp/static/files/'+imagename)
        filename = fs.save('LaundryApp/static/files/'+imagename, image)
        img, result = predict('LaundryApp/static/files/'+imagename)
        os.remove('LaundryApp/static/files/'+imagename)
        cv2.imwrite('LaundryApp/static/files/'+imagename, img)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
        lid = 0
        with con:
            cur = con.cursor()
            cur.execute("select max(laundry_id) from laundry_service")
            rows = cur.fetchall()
            for row in rows:
                lid = row[0]
        if lid is not None:
            lid = lid + 1
        else:
            lid = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO laundry_service(laundry_id,username, submit_date, service_type, num_shirts, num_tshirts, num_shorts, num_pants, num_towels, num_suits, num_innerwears, num_kurtas, num_paijamas, num_skirts, image_file, stain_condition,delivery_date,delivery_address,delivery_status) VALUES('"+str(lid)+"','"+uname+"','"+today+"','"+service+"','"+shirt+"','"+tshirt+"','"+shorts+"','"+pants+"','"+towels+"','"+suits+"','"+inner+"','"+kurta+"','"+paijama+"','"+skirt+"','"+imagename+"','"+result+"','"+delivery_date+"','"+address+"','Pending')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        plt.imshow(img)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        context= {'data': 'Stains '+result+"<br/>Laundry data successfully saved in Databse", 'img': img_b64}
        return render(request, 'UserScreen.html', context) 
        

def LaundryServiceAction(request):
    if request.method == 'POST':
        global uname
        global service, shirt, tshirt, shorts, pants, towels, suits, inner, kurta, paijama, skirt, address, delivery_date
        service = request.POST.get('t1', False)
        shirt = request.POST.get('t2', False)
        tshirt = request.POST.get('t3', False)
        shorts = request.POST.get('t4', False)
        pants = request.POST.get('t5', False)
        towels = request.POST.get('t6', False)
        suits = request.POST.get('t7', False)
        inner = request.POST.get('t8', False)
        kurta = request.POST.get('t9', False)
        paijama = request.POST.get('t10', False)
        skirt = request.POST.get('t11', False)
        address = request.POST.get('t12', False)
        delivery_date = request.POST.get('t13', False)        
        context= {'data': 'Upload Image'}
        return render(request, 'UploadImage.html', context)   

def YoloGraph(request):
    if request.method == 'GET':
        img = cv2.imread("model/results.png")
        img = cv2.resize(img, (1000, 800))
        plt.figure(figsize=(12, 8))
        plt.imshow(img)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        context= {'data': 'Yolo Performance Graph', 'img': img_b64}
        return render(request, 'UserScreen.html', context) 

def ViewLaundry(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Laundry ID</th><th><font size="" color="black">Owner Name</th><th><font size="" color="black">Laundry Date</th>'
        output+='<th><font size="" color="black">Service Type</th><th><font size="" color="black">Shirts</th>'
        output+='<th><font size="" color="black">T-Shirts</th><th><font size="" color="black">Shorts</th>'
        output+='<th><font size="" color="black">Pants</th><th><font size="" color="black">Towels</th>'
        output+='<th><font size="" color="black">Suits</th><th><font size="" color="black">Inner Wears</th>'
        output+='<th><font size="" color="black">Kurtas</th><th><font size="" color="black">Paijamas</th>'
        output+='<th><font size="" color="black">Skirts</th><th><font size="" color="black">Stain Result</th>'
        output+='<th><font size="" color="black">Delivery Date</th><th><font size="" color="black">Delivery Address</th>'
        output+='<th><font size="" color="black">Status</th><th><font size="" color="black">Image</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from laundry_service where username='"+uname+"'")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td>'
                output+='<td><font size="" color="black">'+row[5]+'</td>'
                output+='<td><font size="" color="black">'+row[6]+'</td>'
                output+='<td><font size="" color="black">'+row[7]+'</td>'
                output+='<td><font size="" color="black">'+row[8]+'</td>'
                output+='<td><font size="" color="black">'+row[9]+'</td>'
                output+='<td><font size="" color="black">'+row[10]+'</td>'
                output+='<td><font size="" color="black">'+row[11]+'</td>'
                output+='<td><font size="" color="black">'+row[12]+'</td>'
                output+='<td><font size="" color="black">'+row[13]+'</td>'
                output+='<td><font size="" color="black">'+row[15]+'</td>'
                output+='<td><font size="" color="black">'+row[16]+'</td>'
                output+='<td><font size="" color="black">'+row[17]+'</td>'
                output+='<td><font size="" color="black">'+row[18]+'</td>'
                output+='<td><img src="static/files/'+row[14]+'" height="300" width="300"/></td></tr>'
               
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'UserScreen.html', context)            

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def LaundryService(request):
    if request.method == 'GET':
       return render(request, 'LaundryService.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
                
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact_no,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup completed<br/>You can login with "+username
        context= {'data': status}
        return render(request, 'Register.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global uname, utype, otp
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'laundry',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username, password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1                    
                    break		
        if index == 1:
            context= {'data':'Welcome '+uname}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)                 

def About(request):
    if request.method == 'GET':
        return render(request, 'About.html', {})

def Contact(request):
    if request.method == 'GET':
        return render(request, 'Contact.html', {})

def ContactAction(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you can add code to save the message to database or send email
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('Contact')
    
    return redirect('Contact')


