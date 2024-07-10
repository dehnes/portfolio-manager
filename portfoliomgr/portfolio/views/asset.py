import logging

from django.shortcuts import render

from ..market import get_market_price
from ..models.asset import Asset
from ..models.batch import Batch
from ..models.batch_position import BatchPosition
from .utils.context import get_sidebar_context

logger = logging.getLogger(__name__)


def asset(request, id):
    context = {}
    context["sidebar"] = get_sidebar_context()
    asset = Asset.objects.filter(id=id)[0]
    batches = Batch.objects.filter(fk_asset=asset)
    market_price = get_market_price(asset.fk_security.ticker_symbol)
    asset.fk_security.market_price = market_price
    for batch in batches:
        batch.positions = BatchPosition.objects.filter(fk_batch=batch)
        for pos in batch.positions:
            pos.value = float(pos.quantity) * float(market_price)
    context["asset"] = asset
    context["batches"] = batches

    return render(request, "portfolio/asset.html", context)
