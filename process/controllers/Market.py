from ninja import Router

from orgin.ent.premission import AuthBearer
from orgin.ent.schema import MessageOut
from orgin.ent.utils import response
from process.models import Market
from process.schema import MarketIn , MarketOut 

market_controller = Router(tags=['Market'])


@market_controller.get('market/show/all', auth=AuthBearer(), response={200: MarketOut, 403: MessageOut})
def get_all_markets(request, per_page: int = 12,page: int = 1):
    markets = Market.objects.all()
    return response(200, markets, paginated=True, per_page=per_page, page=page)


@market_controller.post('market', auth=AuthBearer(), response={200: MarketOut, 403: MessageOut})
def market_create(request, payload: MarketIn):
    if request.auth.is_staff:
        try: 
            Market.objects.get(name= payload.name)
            return 403, {'message': 'markets already exists'}
        except Market.DoesNotExist:
            payload = payload.dict()
            products = payload.pop('products')

            market = Market.objects.create(**payload)
            market.save()
            market.products.add(*products)
            return 200, market
        
@market_controller.get('market/show/{pk}', auth=AuthBearer(), response={200: MarketOut, 403: MessageOut})
def get_market(request, pk: str):
    market = Market.objects.get(id=pk)
    return 200, market


@market_controller.put('market/update/{pk}', auth=AuthBearer(), response={200: MarketOut, 403: MessageOut})
def update_market(request, pk: str, payload: MarketIn):
    if request.auth.is_staff:
        try:
            market = Market.objects.get(id=pk)
            market.name = payload.name
            market.address = payload.address
            market.save()
            return 200, market
        except Market.DoesNotExist:
            return 403, {'message': 'Market does not exist'}


@market_controller.delete('market/delete/{pk}', auth=AuthBearer(), response={200: MarketOut, 403: MessageOut})
def delete_market(request, pk: str):
    if request.auth.is_staff:
        try:
            market = Market.objects.get(id=pk)
            market.delete()
            return 200, {'message': 'market deleted successfully'}
        except Market.DoesNotExist:
            return 403, {'message': 'Market does not exist'}



