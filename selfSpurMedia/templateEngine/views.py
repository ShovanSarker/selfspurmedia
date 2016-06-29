from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from subscriber.models import Subscriber
from product.models import Product, Brand, Category, Type
from package.models import Package, PackageRequest, SubscribedPackage
from review.models import Review
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
                res = redirect('/')
            else:
                res = redirect('/')
        else:
            res = redirect('/logout')
    else:
        res = redirect('/')
    return res


def home(request):
    brands = Brand.objects.filter(isActive=True)
    types = Type.objects.filter(isActive=True)
    categories = Category.objects.filter(isActive=True)
    featured_products1 = Product.objects.filter(isFeatured=True)[0:3]
    featured_products2 = Product.objects.filter(isFeatured=True)[4:7]
    featured_products3 = Product.objects.filter(isFeatured=True)[8:11]
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])
        return render(request, 'common/index.sho', {'admin': userObject.isAdmin,
                                                    'productOwner': userObject.isProductOwner,
                                                    'brands': brands,
                                                    'types': types,
                                                    'categories': categories,
                                                    'userName': userObject.name,
                                                    'featured_products1': featured_products1,
                                                    'featured_products2': featured_products2,
                                                    'featured_products3': featured_products3,
                                                    'registered': True})
    else:
        return render(request, 'common/index.sho', {'registered': False,
                                                    'brands': brands,
                                                    'types': types,
                                                    'featured_products1': featured_products1,
                                                    'featured_products2': featured_products2,
                                                    'featured_products3': featured_products3,
                                                    'categories': categories})


def product(request, pid):
    this_product = Product.objects.get(id=pid)
    review_of_this_product = Review.objects.filter(product=this_product).order_by('-dateAdded')
    suggested_products1 = Product.objects.filter(type=this_product.type, category=this_product.category)[0:3]
    suggested_products2 = Product.objects.filter(type=this_product.type, category=this_product.category)[4:7]
    suggested_products3 = Product.objects.filter(type=this_product.type, category=this_product.category)[8:11]
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])
        return render(request, 'common/detail.html', {'admin': userObject.isAdmin,
                                                      'productOwner': userObject.isProductOwner,
                                                      'this_product': this_product,
                                                      'userName': userObject.name,
                                                      'suggested_products1': suggested_products1,
                                                      'review_of_this_product': review_of_this_product,
                                                      'registered': True})
    else:
        return render(request, 'common/detail.html', {'registered': False,
                                                      'suggested_products1': suggested_products1,
                                                      'suggested_products2': suggested_products2,
                                                      'suggested_products3': suggested_products3,
                                                      'review_of_this_product': review_of_this_product,
                                                      'this_product': this_product})


def products(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])

        return render(request, 'common/category.html', {'admin': userObject.isAdmin,
                                                        'productOwner': userObject.isProductOwner,
                                                        'userName': userObject.name,
                                                        'registered': True})
    else:
        return render(request, 'common/category.html', {'registered': False})


def categories(request, iid):
    all_categories = Category.objects.filter(isActive=True)
    this_category = Category.objects.get(id=iid)
    items_in_this_category = Product.objects.filter(category=this_category)
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])
        return render(request, 'common/category.html', {'admin': userObject.isAdmin,
                                                        'productOwner': userObject.isProductOwner,
                                                        'userName': userObject.name,
                                                        'all_categories': all_categories,
                                                        'this_category': this_category,
                                                        'items_in_this_category': items_in_this_category,
                                                        'registered': True})
    else:
        return render(request, 'common/category.html', {'registered': False,
                                                        'this_category': this_category,
                                                        'items_in_this_category': items_in_this_category,
                                                        'all_categories': all_categories})


def brands(request, iid):
    all_categories = Brand.objects.filter(isActive=True)
    this_category = Brand.objects.get(id=iid)
    items_in_this_category = Product.objects.filter(brand=this_category)
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])
        return render(request, 'common/brand.html', {'admin': userObject.isAdmin,
                                                     'productOwner': userObject.isProductOwner,
                                                     'userName': userObject.name,
                                                     'all_categories': all_categories,
                                                     'this_category': this_category,
                                                     'items_in_this_category': items_in_this_category,
                                                     'registered': True})
    else:
        return render(request, 'common/brand.html', {'registered': False,
                                                     'this_category': this_category,
                                                     'items_in_this_category': items_in_this_category,
                                                     'all_categories': all_categories})


def types(request, iid):
    all_categories = Type.objects.filter(isActive=True)
    this_category = Type.objects.get(id=iid)
    items_in_this_category = Product.objects.filter(type=this_category)
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])
        return render(request, 'common/types.html', {'admin': userObject.isAdmin,
                                                     'productOwner': userObject.isProductOwner,
                                                     'userName': userObject.name,
                                                     'all_categories': all_categories,
                                                     'this_category': this_category,
                                                     'items_in_this_category': items_in_this_category,
                                                     'registered': True})
    else:
        return render(request, 'common/types.html', {'registered': False,
                                                     'this_category': this_category,
                                                     'items_in_this_category': items_in_this_category,
                                                     'all_categories': all_categories})


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
        return render(request, 'common/register.sho', {'all_packages': all_packages})


def spur(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])
        all_type = Type.objects.all()
        all_category = Category.objects.all()
        all_brand = Brand.objects.all()
        return render(request, 'common/spur.html', {'admin': userObject.isAdmin,
                                                    'productOwner': userObject.isProductOwner,
                                                    'userName': userObject.name,
                                                    'all_type': all_type,
                                                    'all_category': all_category,
                                                    'all_brand': all_brand,
                                                    'registered': True})
    else:
        return redirect('/register')


def submitreview(request, pid):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        post_data = request.POST
        this_product = Product.objects.get(id=pid)
        userObject = Subscriber.objects.get(email=request.session['user'])
        new_review = Review(subscriber=userObject,
                            product=this_product,
                            rating=post_data['rating'],
                            review=post_data['comment'])
        new_review.save()
        old_review_count = this_product.totalNumberOfRating
        old_star_rating = this_product.totalNumberOfStars
        new_star_rating = (int(old_review_count) * int(old_star_rating) +
                           int(post_data['rating'])) / (int(old_review_count)+1)
        new_review_count = int(old_review_count) + 1
        this_product.totalNumberOfRating = new_review_count
        this_product.totalNumberOfStars = new_star_rating
        this_product.save()

        return redirect('/product/'+pid)
    else:
        return redirect('/register')


def submit_spur(request):

    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])
        post_data = request.POST
        file_data = request.FILES
        print(file_data)
        category_id = post_data['category']
        brand_id = post_data['brand']
        type_id = post_data['type']
        description = post_data['contact-message']
        product = post_data['product']
        category_object = Category.objects.get(id=category_id)
        brand_object = Brand.objects.get(id=brand_id)
        type_object = Type.objects.get(id=type_id)
        if 'avatar1' in file_data:
            avatar1 = file_data['avatar1']
        else:
            avatar1 = None

        if 'avatar2' in file_data:
            avatar2 = file_data['avatar2']
        else:
            avatar2 = None

        if 'avatar3' in file_data:
            avatar3 = file_data['avatar3']
        else:
            avatar3 = None

        if 'avatar4' in file_data:
            avatar4 = file_data['avatar4']
        else:
            avatar4 = None

        if 'avatar5' in file_data:
            avatar5 = file_data['avatar5']
        else:
            avatar5 = None
        new_product = Product(name=product,
                              description=description,
                              type=type_object,
                              brand=brand_object,
                              category=category_object,
                              addedBy=userObject,
                              image1=avatar1,
                              image2=avatar2,
                              image3=avatar3,
                              image4=avatar4,
                              image5=avatar5)
        new_product.save()
        return redirect('/')
    else:
        return redirect('/register')


def contact(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])

        return render(request, 'common/contact.sho', {'admin': userObject.isAdmin,
                                                      'productOwner': userObject.isProductOwner,
                                                      'userName': userObject.name,
                                                      'registered': True})
    else:
        return render(request, 'common/contact.sho', {'registered': False})


def profile(request):
    if 'user' in request.session and Subscriber.objects.filter(email=request.session['user']).exists():
        userObject = Subscriber.objects.get(email=request.session['user'])

        return render(request, 'common/contact.sho', {'admin': userObject.isAdmin,
                                                      'productOwner': userObject.isProductOwner,
                                                      'userName': userObject.name,
                                                      'registered': True})
    else:
        return render(request, 'common/contact.sho', {'registered': False})

'''
End common section
'''
'''
Start admin section
'''


@login_required(login_url='/login/')
def dashboard(request):

    return render(request, 'admin/index.sho', {})


@login_required(login_url='/login/')
def subscriber(request):
    admin_subscribers = Subscriber.objects.filter(isAdmin=True)
    shopowner_subscribers = Subscriber.objects.filter(isProductOwner=True, isAdmin=False, isActive=True)
    banned_subscribers = Subscriber.objects.filter(isProductOwner=True, isAdmin=False, isActive=False)
    pending_subscribers = Subscriber.objects.filter(isProductOwner=False, isAdmin=False, isActive=False)

    return render(request, 'admin/subscribers.sho', {'admin_subscribers': admin_subscribers,
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
        return render(request, 'admin/package.sho', {'active_packages': active_packages,
                                                     'inactive_packages': inactive_packages})


@login_required(login_url='/login/')
def other_request(request):
    post_data = request.POST
    get_data = request.GET
    # print(post_data)
    # print(get_data)
    if 'name' and 'option' in post_data:
        if post_data['option'] == 'category':
            new_category = Category(name=post_data['name'],
                                    remarks=post_data['remarks'],
                                    isPendingForApproval=False)
            new_category.save()
        elif post_data['option'] == 'type':
            new_type = Type(name=post_data['name'],
                            remarks=post_data['remarks'])
            new_type.save()
        elif post_data['option'] == 'brand':
            new_brand = Brand(name=post_data['name'],
                              remarks=post_data['remarks'],
                              isPendingForApproval=False)
            new_brand.save()

    all_categories = Category.objects.all()
    all_types = Type.objects.all()
    all_brands = Brand.objects.all()
    if 'toggle' and 'item' in get_data:
        package_id = get_data['toggle']
        if get_data['item'] == 'category':
            this_package = Category.objects.get(id=package_id)
        elif get_data['item'] == 'type':
            print('here')
            this_package = Type.objects.get(id=package_id)
        elif get_data['item'] == 'brand':
            this_package = Brand.objects.get(id=package_id)

        if this_package.isActive:
            this_package.isActive = False
        else:
            this_package.isActive = True
        this_package.save()
        return redirect('/other_request')
    else:
        return render(request, 'admin/other_requests.sho', {'all_categories': all_categories,
                                                            'all_types': all_types,
                                                            'all_brands': all_brands})


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
        return render(request, 'admin/package_request.sho', {'requested_packages': requested_packages,
                                                             'subscribed_packages': subscribed_packages})
'''
End admin section
'''
