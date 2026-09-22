from shop.models import Product

products = [
    ("Wireless Headphones", "Comfortable wireless headphones with clear sound.", 2499, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80", 20),
    ("Smart Watch", "Fitness tracking, notifications and everyday smart features.", 3299, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80", 15),
    ("Running Shoes", "Lightweight running shoes designed for daily training.", 1899, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80", 25),
    ("Backpack", "Durable everyday backpack for college and work.", 1299, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80", 30),
    ("Mechanical Keyboard", "Compact mechanical keyboard for coding and gaming.", 2799, "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=900&q=80", 12),
    ("Bluetooth Speaker", "Portable speaker with powerful audio for everyday use.", 1599, "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=80", 18),
]

for name, description, price, image_url, stock in products:
    Product.objects.get_or_create(
        name=name,
        defaults=dict(description=description, price=price, image_url=image_url, stock=stock)
    )

print("Sample products added.")
