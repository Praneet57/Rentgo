from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Asset, Rental
from .forms import AssetForm
from django.utils import timezone

def home(request):
    return render(request, 'home.html')


def register_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            # Optional: set the owner wallet from session or user if needed
            asset.owner_wallet = request.POST.get('owner_wallet', '')
            asset.save()
            return redirect('assets_list')
    else:
        form = AssetForm()
    
    return render(request, 'register_asset.html', {'form': form})


def assets_list(request):
    assets = Asset.objects.all()
    return render(request, 'assets_list.html', {'assets': assets})


def delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    asset.delete()
    return redirect('assets_list')

@login_required
def rent_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        customer_contact = request.POST['customer_contact']
        customer_proof = request.FILES.get('customer_proof')

        # Save rental info
        rental = Rental.objects.create(
            asset=asset,
            customer=request.user,
            start_date=start_date,
            end_date=end_date,
            customer_contact=customer_contact,
            customer_proof=customer_proof
        )

        return redirect('assets_list')

    return render(request, 'rent_asset.html', {'asset': asset})

@login_required
def user_dashboard(request):
    # Show rentals for the logged-in user
    rentals = Rental.objects.filter(customer=request.user)
    return render(request, 'user_dashboard.html', {'rentals': rentals})
