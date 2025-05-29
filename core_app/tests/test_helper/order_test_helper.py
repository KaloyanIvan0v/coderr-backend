from core_app.models import Order, OrderFeatures


ORDER_DATA = {
    "id": 1,
    "title": "Logo Design",
    "revisions": 3,
    "delivery_time_in_days": 5,
    "price": 150,
    "features": [
        "Logo Design",
        "Visitenkarten"
    ],
    "offer_type": "basic",
    "status": "in_progress",
    "created_at": "2024-09-29T10:00:00Z",
    "updated_at": "2024-09-30T12:00:00Z"
}


def create_order(test_case, user, business_user):
    order_data = ORDER_DATA.copy()
    features = order_data.pop('features', [])

    order = Order.objects.create(
        customer_user=user,
        business_user=business_user,
        **order_data)

    for feature in features:
        OrderFeatures.objects.create(
            order=order,
            feature=feature)

    return order
