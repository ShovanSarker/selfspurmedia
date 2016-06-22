from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from subscriber.models import Subscriber
from package.models import Package, PackageRequest,SubscribedPackage
# Create your views here.
# index page
# login page
# product page
# products page
# register page
# spur page

'''
Start common section
'''


def logout_now(request):
    logout(request)
    return redirect('/')


def login(request):
    postdata = request.POST
    if 'email' in postdata and 'password' in postdata:
        user = authenticate(username=postdata['email'], password=postdata['password'])
        if not Subscriber.objects.filter().exists():
            createAdmin = Subscriber(name='admin', email=postdata['email'], secretQuestion='Who are you?',
                                     secretAnswer='noone', isAdmin=True, isProductOwner=True)
            createAdmin.save()
        if user is not None and Subscriber.objects.get(email=postdata['email']).isActive:
            auth_login(request, user)
            request.session['user'] = postdata['email']
            if user.is_superuser:
                res = redirect('/admin')
            else:
                res = redirect('/')
        else:
            res = redirect('/logout')
    else:
        res = redirect('/')
    return res


def home(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])

        return render(request, 'common/index.sho', {'admin': userObject.isAdmin,
                                                    'productOwner': userObject.isProductOwner,
                                                    'userName': userObject.name,
                                                    'registered': True})
    else:
        return render(request, 'common/index.sho', {'registered': False})


def product(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])

        return render(request, 'common/detail.html', {'admin': userObject.isAdmin,
                                                      'productOwner': userObject.isProductOwner,
                                                      'userName': userObject.name,
                                                      'registered': True})
    else:
        return render(request, 'common/detail.html', {'registered': False})


def products(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])

        return render(request, 'common/category.html', {'admin': userObject.isAdmin,
                                                        'productOwner': userObject.isProductOwner,
                                                        'userName': userObject.name,
                                                        'registered': True})
    else:
        return render(request, 'common/category.html', {'registered': False})


@csrf_exempt
def register(request):
    postdata = request.POST
    print(postdata)
    all_packages = Package.objects.filter(isActive=True)
    if 'email_reg' in postdata and not Subscriber.objects.filter(email=postdata['email_reg']).exists():

        new_user = User.objects.create_user(postdata['email_reg'],
                                            postdata['email_reg'],
                                            postdata['password'])
        new_user.save()
        new_user_details = Subscriber(name=postdata['name'],
                                      email=postdata['email_reg'],
                                      secretQuestion=postdata['security_ques'],
                                      secretAnswer=postdata['secret_answer'],
                                      isAdmin=False,
                                      isProductOwner=False,
                                      isActive=False)
        new_user_details.save()
        if 'package'in postdata:
            package_id = postdata['package']
            selected_package = Package.objects.get(id=package_id)
            print(selected_package.name)
            this_user_package = PackageRequest(subscriber=new_user_details,
                                               package=selected_package)
            this_user_package.save()

        user = authenticate(username=postdata['email_reg'], password=postdata['password'])
        auth_login(request, user)
        request.session['user'] = postdata['email_reg']
        return redirect('/')
    else:
        return render(request, 'common/register.html', {'all_packages': all_packages})


def spur(request):
    return render(request, 'common/spur.html', {})


def contact(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])

        return render(request, 'common/contact.html', {'admin': userObject.isAdmin,
                                                       'productOwner': userObject.isProductOwner,
                                                       'userName': userObject.name,
                                                       'registered': True})
    else:
        return render(request, 'common/contact.html', {'registered': False})


def profile(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])

        return render(request, 'common/contact.html', {'admin': userObject.isAdmin,
                                                       'productOwner': userObject.isProductOwner,
                                                       'userName': userObject.name,
                                                       'registered': True})
    else:
        return render(request, 'common/contact.html', {'registered': False})

'''
End common section
'''
'''
Start admin section
'''


@login_required(login_url='/login/')
def dashboard(request):

    return render(request, 'admin/index.html', {})


@login_required(login_url='/login/')
def subscriber(request):
    admin_subscribers = Subscriber.objects.filter(isAdmin=True)
    shopowner_subscribers = Subscriber.objects.filter(isProductOwner=True, isAdmin=False, isActive=True)
    banned_subscribers = Subscriber.objects.filter(isProductOwner=True, isAdmin=False, isActive=False)
    pending_subscribers = Subscriber.objects.filter(isProductOwner=False, isAdmin=False, isActive=False)

    return render(request, 'admin/subscribers.html', {'admin_subscribers': admin_subscribers,
                                                      'shopowner_subscribers': shopowner_subscribers,
                                                      'banned_subscribers': banned_subscribers,
                                                      'pending_subscribers': pending_subscribers})


@login_required(login_url='/login/')
def unblock(request, sid):
    this_subscriber = Subscriber.objects.get(id=sid)
    this_subscriber.isActive = True
    this_subscriber.save()
    return redirect('/subscriber')


@login_required(login_url='/login/')
def block(request, sid):
    this_subscriber = Subscriber.objects.get(id=sid)
    this_subscriber.isActive = False
    this_subscriber.save()
    return redirect('/subscriber')


@login_required(login_url='/login/')
def active(request, sid):
    this_subscriber = Subscriber.objects.get(id=sid)
    this_subscriber.isActive = True
    this_subscriber.isProductOwner = True
    this_subscriber.save()
    return redirect('/subscriber')


@login_required(login_url='/login/')
def package(request):
    post_data = request.POST
    get_data = request.GET
    if 'name' and 'limit' in post_data:
        new_package = Package(name=post_data['name'], remarks=post_data['details'], limit=int(post_data['limit']))
        new_package.save()
    active_packages = Package.objects.filter(isActive=True)
    inactive_packages = Package.objects.filter(isActive=False)
    if 'toggle' in get_data:
        package_id = get_data['toggle']
        if Package.objects.filter(id=package_id).exists:
            this_package = Package.objects.get(id=package_id)
            if this_package.isActive:
                this_package.isActive = False
            else:
                this_package.isActive = True
            this_package.save()
        return redirect('/package')
    else:
        return render(request, 'admin/package.html', {'active_packages': active_packages,
                                                      'inactive_packages': inactive_packages})


@login_required(login_url='/login/')
def package_request(request):
    get_data = request.GET
    requested_packages = PackageRequest.objects.filter(isPending=True)
    subscribed_packages = SubscribedPackage.objects.all()
    if 'accept' in get_data:
        package_request_id = get_data['accept']
        package_request_object = PackageRequest.objects.get(id=package_request_id)
        new_package = SubscribedPackage(subscriber=package_request_object.subscriber,
                                        package=package_request_object.package)
        new_package.save()
        package_request_object.isPending = False
        package_request_object.save()
        return redirect('/package_request')
    elif 'reject' in get_data:
        package_request_id = get_data['reject']
        package_request_object = PackageRequest.objects.get(id=package_request_id)
        package_request_object.isPending = False
        package_request_object.save()
        return redirect('/package_request')
    else:
        return render(request, 'admin/package_request.html', {'requested_packages': requested_packages,
                                                              'subscribed_packages': subscribed_packages})
'''
End admin section
'''
