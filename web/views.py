import datetime
from datetime import timedelta
from builtins import str
# from datetime import datetime, timedelta

from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import mysql.connector

from web.forms import RegistrationForm, OrderForm
from web.models import MyUser, Order, zone_connection, dir_connection, zone, order_sales, final_order

# from web.forms import OrderForm, RegistrationForm


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    # form = RegistrationForm()
    form = RegistrationForm(request.POST)
    context = {'form': form}
    if request.method == "POST":
        if form.is_valid():
            username = request.POST['username']
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            # password2 = request.POST['password2']
            type1 = request.POST['type']
            phone = request.POST['phone']
            # company = request.POST['company']
            print(type1, "type")
            print(User.objects.all())

            if User.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect('signin')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!!")
                return redirect('signin')

            if len(username) > 20:
                messages.error(request, "Username must be under 20 charcters!!")
                return redirect('signin')

            # if password != password2:
            #     messages.error(request, "Passwords didn't matched!!")
            #     return redirect('home')

            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!!")
                return redirect('home')

            saveuser = User.objects.create(username=username, email=email, password=password)
            saveuser.is_active = True
            saveuser.save()


            save = MyUser.objects.create(first_name=fname ,last_name=lname ,username=username, type=type1, email=email, password=password, phone=phone)
            print(save)
            save.is_active = True
            save.save()

            if type1 == "director":
                return redirect('signin')
            elif type1 == "sales":
                return render(request, "authentication/enter_sales.html", {"name": username})
            elif type1 == "zone":
                return render(request, "authentication/enter_zonal.html", {"name": username})
        else:
            print("Invalid")
    return render(request, "authentication/signup.html", context)

def signin(request):
    if request.method == 'POST':
        if MyUser.objects.filter(username=request.POST['username'], password=request.POST['password']).exists():
            member = MyUser.objects.get(username=request.POST['username'], password=request.POST['password'])
            char = []
            nam = []
            sum = 0
            filtered_data = []
            da = []
            dates = []
            list1 = []
            list2 = []
            table = []
            for i in dir_connection.objects.filter(director_name=member.username):
                for j in zone_connection.objects.filter(zonal_name=i.zonal_name):
                    list1.append([j.zonal_name, j.sales_name])
                    for x in final_order.objects.filter(username=j.sales_name):
                        list2.append([j.zonal_name, x.product_name, x.quantity, x.rate])
                        table.append([j.zonal_name, x.product_name, x.quantity, x.rate, x.date, x.company])

            print(list1, "list1")
            print(list2, "list2")
            sum1 = 0
            i = 0
            quantity = []
            name = []
            f_list = [['Zone Name', 'Total sales Amount'],]
            global r, r1
            while i < len(list2):
                j = i + 1
                while j < len(list2):
                    print(list2[i][0], 'list2[i][0]')
                    if list2[i][0] == list2[j][0]:
                        # name.append(list2[i][0])
                        r = int(list2[i][2]) * int(list2[i][3])
                        r1 = int(list2[j][2]) * int(list2[j][3])
                        sum1 = sum1 + r + r1
                        list2[i][2] = 1
                        list2[i][3] = r1 + r
                        del list2[j]
                    else:
                        j += 1
                quantity.append(list2[i][3])
                name.append(list2[i][0])
                f_list.append([list2[i][0],list2[i][3]])
                i += 1

            print(f_list, "f_list")
            if member.type == "director":
                print('access')
                zonal =  dir_connection.objects.filter(director_name=member.username)
                print(zonal, "zonal")
                for i in zonal:
                    print('acces2')
                    sale = final_order.objects.filter(username=i.zonal_name)
                    print(sale, "sale")
                    today = datetime.datetime.today()
                    today = today.date()
                    last_14_days = today - timedelta(days=14)
                    for record in sale:
                        print(record, "record")
                        filtered_data.append(
                            [record.product_name, record.date, record.username, record.quantity, record.rate]
                        )
                        dates.append(record.date)

                    for i in sale:
                        char.append(int(i.rate))
                        nam.append(i.product_name)
                        sum += int(i.rate) * int(i.quantity)

                i = 0
                while i < len(filtered_data):
                    j = i + 1
                    while j < len(filtered_data):

                        if filtered_data[i][0] == filtered_data[j][0] and filtered_data[i][1] == filtered_data[j][1]:
                            filtered_data[i][3] = int(filtered_data[i][3]) + int(filtered_data[j][3])
                            del filtered_data[j]
                        else:
                            j += 1

                    filtered_data[i].append(int(filtered_data[i][3]) * int(filtered_data[i][4]))
                    i += 1

                dates = list(set(dates))
                i = 0
                while i < len(filtered_data):
                    if filtered_data[i][1] in dates:
                        da.append([filtered_data[i][1], filtered_data[i][0], filtered_data[i][-1]])
                    i += 1

                lis = []
                i = 0
                numpy = []
                while i < len(da):
                    x = i + 1
                    while x < len(da):
                        if da[i][0] == da[x][0]:
                            lis.append([da[i][0], da[i][-1], da[x][-1]])
                            numpy.append(da[i][1])
                            numpy.append(da[x][1])
                            del da[i][1]
                            del da[x][1]
                            del da[i], da[x - 1]
                        x += 1

                    i += 1

                dat = []
                nam = []
                for i in lis:
                    i[0] = str(i[0])
                for i in da:
                    i[0] = str(i[0])
                    numpy.append(i[1])
                    del i[1]

                final = da + lis
                for i in filtered_data:
                    dat.append(i[0])
                    nam.append(i[0])


                keys = ['z_name', 'name', 'qty', 'rate', 'date', 'company']
                list_of_dict = [dict(zip(keys, i)) for i in table]
                print(f_list, "f_list")
                return render(request, "authentication/dashboard-r.html", {"name": member.username, "zonal": zonal, "filter":list_of_dict, "sum": sum, "list":f_list})
            elif member.type == "sales":
                # return render(request, "authentication/enter_sales.html", {"name": member.username})
                sales = zone_connection.objects.filter(sales_name=member.username)
                return render(request, "authentication/dashboard-s.html", {"name": member.username, "sales": sales})
            elif member.type == "zone":
                # return render(request, "authentication/enter_zonal.html", {"name": member.username})
                return render(request, "authentication/dashboard-s.html", {"name": member.username})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
        # if authenticate(request, username=request.POST['username'], password=request.POST['password']) is not None:
        #     member = User.objects.filter(username=request.POST['username'], password=request.POST['password']).first()
        #     # member = get_object_or_404(User, username=request.POST['username'], password=request.POST['password'])
        #     login(request, member)
        #     # if member.type == "director":
        #     #     return redirect('dashboard-r')
        #     # elif member.type == "sales":
        #     #     return render(request, "authentication/dashboard-s.html", {"fname": member.username})
        #     # elif member.type == "zones":
        #     #     return render(request, "authentication/dashboard-z.html", {"fname": member.username})
        # else:
        #     messages.error(request, "Bad Credentials!!")

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def acc_type(request):
    if request.method == "POST":
        global type
        zones = request.POST['zones']
        sales = request.POST['sales']
        director = request.POST['director']
        if zones:
            type = "Zones"
        elif sales:
            type = "Sales"
        elif director:
            type = "Director"

        print(type)
    return render(request, "authentication/acc-type.html")

def enter_sales(request, name):
    if request.method == "POST":
        username = request.POST['username']

        # if MyUser.objects.filter(username=username).exists():
        if MyUser.objects.filter(username=name).exists() == False:
            print("yes exists","if")
            messages.error(request, "This user is already linked with Zonal Manager!!")
            return redirect('signin')
        else:
            print("no exists.ellse")
            save = zone_connection.objects.create(sales_name=name, zonal_name=username)
            save.save()
            return render(request, "authentication/dashboard-s.html", {"name": name})
        # else:
        #     print("no exists")
        #     messages.error(request, "No such user!!")
        #     return redirect('home')
    return render(request, "authentication/enter_sales.html", {"name": name})

def enter_zonal(request,name):
    if request.method == "POST":
        print("access")
        username = request.POST['username']
        if MyUser.objects.filter(username=username).exists():
            print("yes exists zonal")
            save = dir_connection.objects.create(director_name=username, zonal_name=name)
            save.save()
            return render(request, "authentication/dashboard-r.html", {"name": name})
        else:
            messages.error(request, "No such user!!")
            return redirect('home')
    return render(request, "authentication/enter_zonal.html", {"name": name})

def test(request):
    return render(request, "authentication/test.html")

def director_detail(request):
    return render(request, "authentication/director-detail.html")

def enter_products(request,name):
    order_form = OrderForm()
    context = {'order_form': order_form, 'name': name}
    if request.method == "POST":
        product = request.POST['product_name']
        quantity = request.POST['quantity']
        price = request.POST['rate']
        packing = request.POST['packing']
        print(product, quantity, price,name,packing)
        save = Order.objects.create(product_name=product, quantity=quantity, rate=price, packing=packing, username=name)
        save.save()
        print("done")
    else:
        print("get")
    return render(request, "authentication/enter-products.html", context)

def order(request, name):
    global orderform
    if MyUser.objects.filter(username=name).first().type == "sales":
        check_sales = zone_connection.objects.filter(sales_name=name)
        final = dir_connection.objects.filter(zonal_name=check_sales.first().zonal_name)
        orderform = Order.objects.filter(username=final.first().director_name)
    else:
        orderform = Order.objects.filter(username=name)

    return render(request, "authentication/take-order.html", {'orderform': orderform, 'name': name})

def dashboard(request,name):
    """get the type of user by name."""
    if MyUser.objects.filter(username=name).exists():
        if MyUser.objects.filter(username=name).first().type == "sales":
            print("sales")
            return render(request, "authentication/dashboard-s.html", {"name": name})
        elif MyUser.objects.filter(username=name).first().type == "zone":
            sales = zone_connection.objects.filter(zone_name=name)
            print("zone")
            return render(request, "authentication/dashboard-z.html", {"name": name, "sales": sales})
        elif MyUser.objects.filter(username=name).first().type == "director":
            zonal = dir_connection.objects.filter(director_name=name)
            print("director")
            return render(request, "authentication/dashboard-r.html", {"name": name, "zonal": zonal})
    # return render(request, "authentication/dashboard-r.html", {"name": name})

def chose_form(request,name):
    return render(request, "authentication/chose-form.html", {"name": name})

def total_sales(request,name):
    """get the date like this format: 2022-04-15 and return the total sales of that day."""
    if request.method == "POST":
        date = '2022-04-15'
        date = datetime.strptime(date, '%Y-%m-%d').date()
        total_sales = Order.objects.filter(date=date).aggregate(Sum('quantity'))
    char = []
    nam = []
    sum = 0
    filtered_data = []
    filtered = []
    filtered_date =[]
    da = []
    dates = []
    total_sales = zone_connection.objects.filter(zonal_name=name)
    for i in total_sales:
        sale = final_order.objects.filter(username=i.sales_name)
        today = datetime.datetime.today()
        today = today.date()
        last_14_days = today - timedelta(days=14)

        for record in sale:
            #
            # if str(record.date) >= str(last_14_days):
            #     print('yes it is')
                filtered_data.append([record.product_name, record.date, record.username, record.quantity, record.rate])
                filtered_data.append([record.product_name, record.date, record.username, record.quantity, record.rate, record.company])
                dates.append(record.date)

        for i in sale:
            char.append(int(i.rate) )
            nam.append(i.product_name)
            print(int(i.rate)* int(i.quantity), "sum r")
            sum += int(i.rate) * int(i.quantity)
    print(filtered_data, "filtered_data")
    i = 0
    while i < len(filtered_data):
        j = i + 1
        while j < len(filtered_data):

            if filtered_data[i][0] == filtered_data[j][0] and filtered_data[i][1] == filtered_data[j][1]:
                filtered_data[i][3] = int(filtered_data[i][3]) + int(filtered_data[j][3])
                del filtered_data[j]
            else:
                j += 1
                filtered.append(filtered_data[i])

        filtered_data[i].append(int(filtered_data[i][3]) * int(filtered_data[i][4]))
        i += 1

    dates = list(set(dates))
    print(filtered_data, "filtered_data")

    i = 0
    while i < len(filtered_data):
        if filtered_data[i][1] in dates:
            da.append([filtered_data[i][1], filtered_data[i][0], filtered_data[i][-1]])
        i += 1

    lis = []
    i = 0
    numpy = []
    while i < len(da):
        x = i + 1
        while x < len(da):
            if da[i][0] == da[x][0]:
                lis.append([da[i][0], da[i][-1], da[x][-1]])
                numpy.append(da[i][1])
                numpy.append(da[x][1])
                del da[i][1]
                del da[x][1]
                del da[i], da[x-1]
            x += 1

        i += 1

    dat = []
    nam = []
    for i in lis:
        i[0] = str(i[0])
    for i in da:
        i[0] = str(i[0])
        numpy.append(i[1])
        del i[1]
    print(da, 'da')
    print(lis, 'lis')
    final = da + lis
    for i in filtered_data:
        dat.append(i[0])
        nam.append(i[0])

    print(filtered_data, "filtered_data")
    print(numpy, "numpy")
    print(da, "da")
    print(final, 'final')
    print(sum, "sum")
    print(filtered, "filtered")
    # for i in range(len(numpy)):
    #     for j in range(len(final)):
    #         if final[j][0] == numpy[i]:
    # dict = {}
    values = filtered_data
    keys = ['pname', 'date', 'name', 'qty', 'rate', 'total', 'company']
    list_of_dict = [dict(zip(keys, i)) for i in filtered_data ]
    print(list_of_dict, "list_of_dict")


    p_name = ['sales_name','sajkflj','jajvd']
    data = ['umar',  37.8, 80.8, 41.8],['javexx',  43.8, 89.8, 45.8]
    return render(request, "authentication/total_sales.html", {"name": name, "total_sales": total_sales, "p_name": nam, "data": final, "filter": list_of_dict, "sum": sum})

def give_order(request,name):
    global orderform
    f_result = []
    if MyUser.objects.filter(username=name).first().type == "sales":
        check_sales = zone_connection.objects.filter(sales_name=name)
        final = dir_connection.objects.filter(zonal_name=check_sales.first().zonal_name)
        orderform = Order.objects.filter(username=final.first().director_name)
        if request.method == "POST":
            for i in range(1, len(orderform) + 1):
                company = request.POST['company' + str(i)]
                qty = request.POST['qty' + str(i)]
                orderform[i - 1].quantity = qty
                orderform[i - 1].save()
                result = request.POST['result' + str(i)]
                f_result.append(result)
                order = final_order(username=name, product_name=orderform[i - 1].product_name, quantity=qty,
                                    rate=orderform[i - 1].rate, company=company)
                order.save()

    elif MyUser.objects.filter(username=name).first().type == "zone":
        final = dir_connection.objects.filter(zonal_name=name)
        orderform = Order.objects.filter(username=final.first().director_name)
        if request.method == "POST":
            for i in range(1, len(orderform) + 1):
                company = request.POST['company' + str(i)]
                qty = request.POST['qty' + str(i)]
                orderform[i - 1].quantity = qty
                orderform[i - 1].save()
                result = request.POST['result' + str(i)]
                f_result.append(result)
                order = final_order(username=name, product_name=orderform[i - 1].product_name, quantity=qty,
                                    rate=orderform[i - 1].rate, company=company)
                order.save()

    else:
        orderform = Order.objects.filter(username=name)
        if request.method == "POST":
            for i in range(1, len(orderform)+1):
                company = request.POST['company' + str(i)]
                qty = request.POST['qty' + str(i)]
                orderform[i-1].quantity = qty
                orderform[i-1].save()
                result = request.POST['result' + str(i)]
                f_result.append(result)
                order = final_order(username=name, product_name=orderform[i - 1].product_name, quantity=qty,
                                    rate=orderform[i - 1].rate, company=company)
                order.save()

    return render(request, "authentication/give-order.html", {"name": name, "orderform": orderform})

def person_chart(request,name):
    char = []
    sum = 0
    if MyUser.objects.filter(username=name).first().type == "sales":
        # check_sales = zone_connection.objects.filter(sales_name=name)
        # final = dir_connection.objects.filter(zonal_name=check_sales.first().zonal_name)
        # chart = final_order.objects.filter(username=final.first().director_name)
        chart = final_order.objects.filter(username=name)
        print("sales accesed")
        for i in chart:
            char.append(int(i.rate) * int(i.quantity))
        print("char",char)
        for i in range(0, len(char)):
            sum = sum + int(char[i])
        print("sum s", sum)
        return render(request, "authentication/person_chart.html", {"name": name, "chart": chart, "sum": sum})

    elif MyUser.objects.filter(username=name).first().type == "zone":
        print(" zone sales accesed")
        final = dir_connection.objects.filter(zonal_name=name.first().zonal_name)
        chart = final_order.objects.filter(username=final.first().director_name)
        for i in chart:
            char.append(int(i.rate) * int(i.quantity))
        for i in range(0, len(char)):
            sum = sum + char[i]
        print("sum z", sum)
        return render(request, "authentication/person_chart.html", {"name": name, "chart": chart, "sum": sum})

    else:
        print("disdf accesed")
        chart = final_order.objects.filter(username=name)
        for i in chart:
            char.append(int(i.rate) * int(i.quantity))
        print(char,"char")
        for i in range(0, len(char)):
            sum = sum + int(char[i])
        print("sum d", sum)
        print("chart", chart)
        return render(request, "authentication/person_chart.html", {"name": name, "chart": chart, "sum": sum})

# def cart(request, name):
#     global orderform
#     f_result = []
#     if MyUser.objects.filter(username=name).first().type == "sales":
#         check_sales = zone_connection.objects.filter(sales_name=name)
#         final = dir_connection.objects.filter(zonal_name=check_sales.first().zonal_name)
#         orderform = Order.objects.filter(username=final.fiarst().director_name)
#         if request.method == 'POST':
#             print(len(orderform))
#             for i in range(1, len(orderform) + 1):
#                 print("qty" + str(i))
#                 print("qty", request.POST['qty' + str(i)])
#                 qty = request.POST['qty' + str(i)]
#                 # rate = request.POST['rate' + str(i)]
#                 # pname = request.POST['pname' + str(i)]
#                 print("qty", qty)
#                 result = request.POST['result' + str(i)]
#                 f_result.append(result)
#                 order = final_order(username=name, quantity=qty, rate=rate, product_name=pname)
#                 order.save()
#     else:
#         orderform = Order.objects.filter(username=name)
#
#         if request.method == 'POST':
#             print(len(orderform))
#             for i in range(1, len(orderform) + 1):
#                 print("qty" + str(i))
#                 print("qty", request.POST['qty' + str(i)])
#                 qty = request.POST['qty' + str(i)]
#                 # rate = request.POST['rate' + str(i)]
#                 # pname = request.POST['pname' + str(i)]
#                 print("qty", qty)
#                 result = request.POST['result' + str(i)]
#                 f_result.append(result)
#                 order = final_order(username=name, quantity=qty, rate=rate, product_name=pname)
#                 order.save()
#     print("f_result cart", f_result)
#     return render(request, "authentication/cart.html", {'orderform': orderform, 'name': name, 'f_result': f_result})


