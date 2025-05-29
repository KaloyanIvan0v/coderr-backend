from core_app.models import Offer, OfferDetails, OfferFeatures
from django.utils import timezone


def create_offer(test_case):
    return Offer.objects.create(
        user=test_case.business_user,
        title="Multipaket",
        image=None,
        description="Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        min_price=100.00,
        min_delivery_time=5,
    )


def create_offer_detail(offer):
    offer_detail = OfferDetails.objects.create(
        id=1,
        offer=offer,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        offer_type="basic"
    )
    OfferFeatures.objects.create(
        offer_detail=offer_detail, feature="Logo Design")
    OfferFeatures.objects.create(
        offer_detail=offer_detail, feature="Visitenkarten")
    return offer_detail


OFFER_DATA = {
    "title": "Multipaket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "min_price": 100.00,
    "min_delivery_time": 5,
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
        },
        {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
        }
    ]
}


OFFER_DATA_CREATE = {
    "title": "Multipaket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "min_price": 100.00,
    "min_delivery_time": 5,
}


OFFER_DATA_CREATE_DETAIL = {
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
        },
        {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
        }
    ]
}
