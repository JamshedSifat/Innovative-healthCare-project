from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Accessory, CartItem, Bill, BillItem


# View to display all products
def products(request):
    """Show all available products"""
    # Get all products that have stock
    products = Accessory.objects.filter(p_count__gt=0)

    context = {
        'products': products
    }
    return render(request, 'accessories/products.html', context)


# View to search products
def product_search(request):
    """Search products by name, description, or vendor"""
    query = request.GET.get('q', '')  # Get search query from URL
    products = Accessory.objects.filter(p_count__gt=0)  # Start with all in-stock products

    if query:  # If user entered a search term
        products = products.filter(
            Q(p_name__icontains=query) |  # Search in product name
            Q(p_description__icontains=query) |  # Search in description
            Q(v_name__icontains=query)  # Search in vendor name
        )

    context = {
        'products': products,
        'query': query
    }
    return render(request, 'accessories/products.html', context)


# View to add products to cart (requires login)
@login_required
def add_to_cart(request, product_id):
    """Add a product to user's shopping cart"""
    if request.method == 'POST':
        # Get the product or show 404 if not found
        product = get_object_or_404(Accessory, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # Check if we have enough stock
        if quantity > product.p_count:
            messages.error(request, f"Sorry! Only {product.p_count} items available.")
            return redirect('accessories:products')

        # Try to get existing cart item or create new one
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            accessory=product,
            defaults={'quantity': quantity}
        )

        if not created:  # Item already in cart
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.p_count:
                messages.error(request, f"Cannot add {quantity} more. Only {product.p_count} available.")
                return redirect('accessories:products')
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f"Updated {product.p_name} quantity in cart.")
        else:  # New item added to cart
            messages.success(request, f"Added {product.p_name} to cart.")

    return redirect('accessories:products')


# View to display user's cart
@login_required
def cart(request):
    """Show user's shopping cart"""
    # Get all cart items for current user
    cart_items = CartItem.objects.filter(user=request.user).select_related('accessory')

    # Calculate total cost
    total_cost = 0
    for item in cart_items:
        total_cost += item.total_cost

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost
    }
    return render(request, 'accessories/cart.html', context)


# View to update cart item quantity
@login_required
def update_cart(request, product_id):
    """Update quantity of item in cart"""
    if request.method == 'POST':
        # Get cart item or show 404
        cart_item = get_object_or_404(CartItem, user=request.user, accessory_id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # Check if enough stock available
        if quantity > cart_item.accessory.p_count:
            messages.error(request, f"Only {cart_item.accessory.p_count} items available.")
            return redirect('accessories:cart')

        # Update quantity
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated successfully.")

    return redirect('accessories:cart')


# View to remove item from cart
@login_required
def remove_from_cart(request, product_id):
    """Remove item from shopping cart"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, user=request.user, accessory_id=product_id)
        product_name = cart_item.accessory.p_name
        cart_item.delete()
        messages.success(request, f"Removed {product_name} from cart.")

    return redirect('accessories:cart')


# View to process checkout
@login_required
def checkout(request):
    """Process checkout and create order"""
    # Get all cart items for user
    cart_items = CartItem.objects.filter(user=request.user).select_related('accessory')

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('accessories:products')

    # Create new bill/order
    bill = Bill.objects.create(customer=request.user)

    # Process each cart item
    for cart_item in cart_items:
        # Check if enough stock available
        if cart_item.quantity > cart_item.accessory.p_count:
            messages.error(request, f"Sorry! Not enough stock for {cart_item.accessory.p_name}")
            bill.delete()  # Cancel the order
            return redirect('accessories:cart')

        # Create bill item
        BillItem.objects.create(
            bill=bill,
            accessory=cart_item.accessory,
            quantity=cart_item.quantity,
            unit_price=cart_item.accessory.p_cost,
            total_cost=cart_item.total_cost
        )

        # Reduce stock quantity
        cart_item.accessory.p_count -= cart_item.quantity
        cart_item.accessory.save()

    # Clear user's cart
    cart_items.delete()

    messages.success(request, f"Order placed successfully! Your Order ID: {bill.id}")
    return render(request, 'accessories/checkout.html', {'bill': bill})