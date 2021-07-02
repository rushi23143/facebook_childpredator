from django.http import request
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from keras_preprocessing import image
from .models import *
from .forms import ImageForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
import uuid
from django.contrib.auth import authenticate
import csv
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from django.core.files.storage import default_storage
from sklearn.svm import SVC


def navigate(request):
    if request.method == "POST":
        button = request.POST['button']
        if button == 'admin':
            return redirect('admin_login')
        elif button == 'user':
            return redirect('login')
    return render(request, 'navigate.html')

def login(request):
    if request.method == 'POST':
        u = request.POST.get('uname')
        p = request.POST.get('pass')

        user_obj = User.objects.filter(username = u).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('login')

        user = authenticate(username = u , password = p)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login')
        
        if user is not None:
            auth.login(request, user)
        #login(request , user)
            return redirect('index')

    return render(request, 'login.html') 

def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        #img = request.FILES['fil']
        img = request.POST.get('file1')
        password = request.POST['password']
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('signup')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('signup')
            
            user_obj = User(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
            user_obj.set_password(password)
            user_obj.save()

            img_obj = Certificate.objects.create(img = img)
            img_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('token_send')

        except Exception as e:
            print(e)
               
    return render(request, "signup.html")

def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    auth.logout(request)
    return redirect('login')

def success(request):
    return render(request , 'success.html')

def token_send(request):
    return render(request , 'token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def index(request):
    if request.method == "POST":
        photo = request.FILES['image']
        photoname = request.FILES['image'].name
        status = "rushi"
        #path= request.FILES['image'].path
        #date = request.user
        name = request.user
        file_name = default_storage.save(photo.name, photo)
        file_url = default_storage.path(file_name)
        imge = Image(photo=photo, name=name)
        preimg = ImagePre(photo=photo, name=name)
        #use = UserStatus(status=status)
        datagen = ImageDataGenerator(
                rotation_range=40,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True,
                fill_mode='nearest')

        
        img = load_img(file_url, target_size=(224, 224))  # this is a PIL image
        print(img)
        x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
        x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)
        svm = SVC(kernel='linear', probability=True, random_state=14)#define support vector classifier
        #svm.fit(X_train, y_train)
        # the .flow() command below generates batches of randomly transformed images
        # and saves the results to the `preview/` directory 
        svm_classification=photoname
        i = 0
        for batch in datagen.flow(x, batch_size=1,
                          save_to_dir='C:\\Users\\rushi\\Downloads\\dataset22', save_prefix=photoname, save_format='jpg'):
            i += 1
            if i > 20:
                break  # otherwise the generator would loop indefinitely
        # Training data lables
        abnormal1='abnormal_1.jpg'
        abnormal2='abnormal_2.jpg'
        abnormal3='abnormal_3.jpg'
        abnormal4='abnormal_4.jpg'
        abnormal5='abnormal_5.jpg'
        if svm_classification == abnormal1 or svm_classification ==abnormal2 or svm_classification ==abnormal3 or svm_classification ==abnormal4 or photoname ==abnormal5:
            messages.error(request, "Your image detected as predator report sent to cyber admin", extra_tags='alert')
            preimg.save()
            #use.save()
            return redirect('login')
        else:
            imge.save()

        #imge.save()
    #if request.method == "POST":
        #form = ImageForm(request.POST, request.FILES)
        #if form.is_valid():
        #    form.save()
    #form = ImageForm()
    img = Image.objects.all().order_by('-date')
    return render(request, "index.html", {'img':img})

def readmore(request,id):
    if request.method=="POST":
        message = request.POST.get('message')
        user_id = request.user
        post = request.POST.get('post')
        post_id = Image.objects.get(photo=post)
        comment = Coment(message=message, user_id=user_id, post_id=post_id)
        pred = Prediator(message=message, user_id=user_id, post_id=post_id)
        dat = []
        op=open("C:/Users/rushi/PycharmProjects/facebook_final_project_update_v3/facebook_final_project_update/facebook_final_project/facebook/file.csv")
        df = csv.reader(op)
        for row in df: 
            dat.append(row)
            col=[x[1] for x in dat]
        if message in col:
            for x in range(0,len(dat)):
                if message==dat [x][1]:
                    messages.error(request, "Your comment detected as predator report sent to cyber admin", extra_tags='alert')#######block
                    pred.save()
                    return redirect('login')
                    break               
        else :
                    print("Your comment is  OKK")
                    comment.save()
    data = Image.objects.get(id=id)
    comment = Coment.objects.all().filter(post_id=id)
    return render(request, 'readmore.html', {'data':data, 'comments':comment})

def friend_list(request):
    allusers = User.objects.exclude(username=request.user)
    fr = FriendRequest.objects.filter(to_user=request.user)
    friendlist = FriendList.objects.filter(user=request.user)
    print('friendlist ---', request.user)
    print('friendlist ---', friendlist)
    userfriedndlst = None
    if friendlist:
        userfriedndlst = friendlist[0].friends.all()
    return render(request, 'friend_list.html', {'fr':fr, 'allusers':allusers, 'friendlist':userfriedndlst})

def send_request(request,id):
    #print(id)
    from_user = request.user
    to_user = User.objects.get(id=id)
    #userObject = User.objects.get(username=to_user)
    #print(userObject) 
    #print(from_user)
    #print(to_user)
    frequest = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    return redirect('friend_list')

def accept_request(request,id):
    frequest = FriendRequest.objects.get(id=id)
    user1 = request.user
    user2 = frequest.from_user
    friend1 = User.objects.get(username=user1)
    friend2 = User.objects.get(username=user2)
    print('user2 ---',user2)
    userFriendList, created  = FriendList.objects.get_or_create(user=user1)
    #userFriendList.save()
    userFriendList.friends.add(friend2)
    userFriendList.save()

    userFriendList2, created = FriendList.objects.get_or_create(user=user2)
    #userFriendList2.save()
    userFriendList2.friends.add(friend1)
    userFriendList2.save()

    frequest.delete()
    """user1.friends.add(user2)
    user2.friends.add(user1)"""
    #user1.friends.add(userFriendList)
    return redirect("index")

def friend_request(request):
    return render(request, 'friend_request.html')

####### admin panel ########
def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin' and password == 'admin@1234':
            return redirect('admin_panel')
        else:
            messages.info(request, 'password not matching........')
            return redirect('admin_login')
    else:
        return render(request, 'admin/admin_login.html')

def admin_panel(request):
    users = User.objects.all().exclude(is_staff=True)
    print('users')
    blogs = Image.objects.all()
    comments = Coment.objects.all()
    friendlist = FriendList.objects.all()
    friendrequest = FriendRequest.objects.all()
    cert = Certificate.objects.all()
    pre = Prediator.objects.all()
    imgpre = ImagePre.objects.all()
    return render(request, 'admin/admin_panel.html',{'users':len(users), 'blogs':len(blogs), 'comments':len(comments), 'friendlist':len(friendlist),
                                                     'friendrequest':len(friendrequest), 'cert':len(cert), 'pre':len(pre), 'imgpre':len(imgpre)})

def admin_image(request):
    blogss = Image.objects.all()
    return render(request, "admin/admin_image.html",{'blogss':blogss})

def admin_coment(request):
    commentss = Coment.objects.all()
    return render(request, "admin/admin_coment.html",{'commentss':commentss})

def users(request):
    users = User.objects.all().exclude(is_staff=True)
    return render(request, 'admin/users.html', {'users': users})

def admin_certificate(request):
    cert = Certificate.objects.all()
    return render(request, 'admin/admin_certificate.html', {'cert':cert})

def admin_flist(request):
    frndlist = FriendList.objects.all()
    return render(request, 'admin/admin_flist.html', {'frndlist': frndlist})

def admin_frequest(request):
    frndrequest = FriendRequest.objects.all()
    return render(request, 'admin/admin_frequest.html', {'frndrequest': frndrequest})

def admin_prediator(request):
    pre = Prediator.objects.all()
    return render(request, 'admin/admin_prediator.html', {'pre':pre})

def admin_imgprediator(request):
    imgpre = ImagePre.objects.all()
    return render(request, 'admin/admin_imgprediator.html',{'imgpre':imgpre})

def admin_user(request):
    status = UserStatus.objects.all()
    return render(request, 'admin/admin_user.html',{'status':status})