from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plot, Item, InventoryItem, Points
from django.contrib import messages
import ctypes
import datetime
from django.utils import timezone


def home(request):
    if request.user.is_authenticated:
        plots = Plot.objects.all().order_by('id')
        plots = plots.filter(user_name=request.user.id)
        if not plots:
            for i in range(9):
                new_plot = Plot.objects.create(user_name_id=request.user.id)
                new_plot.save()
        Points.objects.get_or_create(user_name_id=request.user.id, defaults={'points_total': 500})

        watered_countdown(request)
        growth_countdown(request)
    context = {}
    return render(request, 'farm/home.html', context)


@login_required
def plot(request):
    plots = Plot.objects.all().order_by('id').filter(user_name=request.user.id)
    items = InventoryItem.objects.all().order_by('item__item_name').filter(user_name=request.user.id,
                                                                           item__item_type='Seeds')
    watered_countdown(request)
    growth_countdown(request)
    return render(request, 'farm/plot.html', {'plots': plots, 'items': items})


@login_required
def plant(request, plant_type):
    plots = Plot.objects.all().order_by('id').filter(user_name=request.user.id)
    items = InventoryItem.objects.all().order_by('item__item_name').filter(user_name=request.user.id,
                                                                           item__item_type='Seeds')
    watered_countdown(request)
    growth_countdown(request)
    return render(request, 'farm/plant.html', {'plots': plots, 'plant_type': plant_type, 'items': items})


@login_required
def confirmplant(request, id, plant_type):
    watered_countdown(request)
    growth_countdown(request)
    plot_object = Plot.objects.get(id=id)
    try:
        item_object = InventoryItem.objects.get(user_name=request.user.id, item__plant_type=plant_type, item__item_type='Seeds')
        if plot_object.plot_growth == 0:
            plot_object.plot_growth = 1
            plot_object.plot_plant = plant_type
            plot_object.plot_image = f'images/plots/{plant_type}_seed.png'
            plot_object.growth_time = timezone.now() + datetime.timedelta(minutes=2)
            plot_object.save()
            newquantity = item_object.item_quantity - 1
            if newquantity == 0:
                item_object.delete()
            else:
                item_object.item_quantity = newquantity
                item_object.save()
            messages.success(request, f'{plant_type} planted successfully!')
            return redirect('plot')
        else:
            messages.error(request, f'Plot already has a plant!')
    except InventoryItem.DoesNotExist:
        messages.error(request, f'No {plant_type} seeds!')
        return redirect('plot')
    plots = Plot.objects.all().order_by('id').filter(user_name=request.user.id)
    return render(request, 'farm/plant.html', {'plots': plots, 'plant_type': plant_type})


def growth_countdown(request):
    plots = Plot.objects.all().order_by('id').filter(user_name=request.user.id)
    for plot_object in plots:
        if 3 > plot_object.plot_growth > 0 and plot_object.growth_time <= timezone.now():
            plot_object.plot_growth += 1
            if plot_object.plot_growth == 2:
                plot_object.plot_image = f'images/plots/{plot_object.plot_plant}_seedling.png'
                plot_object.growth_time += datetime.timedelta(minutes=2)
            elif plot_object.plot_growth == 3:
                plot_object.plot_image = f'images/plots/{plot_object.plot_plant}_harvest.png'
            plot_object.save()


@login_required
def harvest(request, id):
    watered_countdown(request)
    growth_countdown(request)
    plot_object = Plot.objects.get(id=id)
    if plot_object.plot_growth == 3:
        item_type = Item.objects.get(plant_type=plot_object.plot_plant, item_type='Harvests')
        item, created = InventoryItem.objects.get_or_create(user_name_id=request.user.id, item_id=item_type.id, defaults={'item_quantity': 1})
        if not created:
            newquantity = item.item_quantity + 1
            item.item_quantity = newquantity
            item.save()
        plot_object.plot_growth = 0
        plot_object.plot_plant = 'None'
        plot_object.plot_watered = False
        plot_object.plot_image = 'images/plots/dirt.png'
        plot_object.save()
        messages.success(request, f'Harvested {item.item.plant_type}!')
        return redirect('plot')
    else:
        messages.error(request, f'Plot is not ready to harvest!')
        return redirect('plot')


@login_required
def water(request, id):
    watered_countdown(request)
    growth_countdown(request)
    plot_object = Plot.objects.get(id=id)
    if not plot_object.plot_watered:
        plot_object.plot_watered = True
        plot_object.water_time = timezone.now() + datetime.timedelta(minutes=1)
        plot_object.growth_time -= datetime.timedelta(seconds=30)
        plot_object.save()
        messages.success(request, f'Plot watered successfully!')
        return redirect('plot')
    else:
        messages.error(request, f'Plot already watered.')
        return redirect('plot')


def watered_countdown(request):
    plots = Plot.objects.all().order_by('id').filter(user_name=request.user.id)
    for plot_object in plots:
        if plot_object.plot_watered and plot_object.water_time <= timezone.now():
            plot_object.plot_watered = False
            plot_object.save()


@login_required
def inventory(request):
    watered_countdown(request)
    growth_countdown(request)
    item_object = InventoryItem.objects.all().order_by('item__item_name').filter(user_name=request.user.id)
    return render(request, 'farm/inventory.html', {'inventory': item_object})


@login_required
def shop(request):
    watered_countdown(request)
    growth_countdown(request)
    items_to_buy = Item.objects.all().order_by('item_cost').filter(item_type='Seeds')
    points = Points.objects.get(user_name=request.user.id)
    items_to_sell = InventoryItem.objects.all().order_by('item__item_cost').filter(user_name=request.user.id, item__item_type='Harvests')
    return render(request, 'farm/shop.html', {'points': points, 'inventory': items_to_sell, 'stock': items_to_buy})


@login_required
def buy(request, id):
    watered_countdown(request)
    growth_countdown(request)
    points = Points.objects.get(user_name=request.user.id)
    item = Item.objects.get(id=id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cost = (quantity * item.item_cost)
        newpoints = points.points_total - cost
        results = ctypes.windll.user32.MessageBoxW(0, f"Are you sure you want to buy {quantity} {item.item_name} "
                                                      f"for {cost} points?", "Are you sure?", 0x1024)
        if results == 6:
            if newpoints < 0:
                messages.error(request, f'Not enough points!')
            else:
                item, created = InventoryItem.objects.get_or_create(user_name_id=request.user.id, item_id=id,
                                                                    defaults={'item_quantity': quantity})
                if not created:
                    item.item_quantity += quantity
                    item.save()
                points.points_total = newpoints
                points.save()
                messages.success(request, f'Purchase successful! You now have {points.points_total} points.')
                return redirect('shop')
        else:
            return redirect('shop')

    return render(request, 'farm/buy.html', {'item': item, 'points': points})


@login_required
def sell(request, id):
    watered_countdown(request)
    growth_countdown(request)
    points = Points.objects.get(user_name=request.user.id)
    item = InventoryItem.objects.get(id=id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        newquantity = item.item_quantity - quantity
        cost = (quantity * item.item.item_cost)
        newpoints = cost + points.points_total
        results = ctypes.windll.user32.MessageBoxW(0, f"Are you sure you want to sell {quantity} {item.item.item_name} "
                                                      f"for {cost} points?", "Are you sure?", 0x1024)
        if results == 6:
            if newquantity == 0:
                item.delete()
                points.points_total = newpoints
                points.save()
                messages.success(request, f'Successful sale! You now have {points.points_total} points.')
                return redirect('shop')
            elif newquantity < 0:
                messages.error(request, f'Not enough of that item!')
            elif newquantity > 0:
                item.item_quantity = newquantity
                item.save()
                points.points_total = newpoints
                points.save()
                messages.success(request, f'Successful sale! You now have {points.points_total} points.')
                return redirect('shop')
        else:
            return redirect('shop')

    return render(request, 'farm/sell.html', {'item': item, 'amount': item.item_quantity})
