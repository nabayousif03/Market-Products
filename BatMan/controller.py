from ninja import Router
from http import HTTPStatus
from django.contrib.auth import authenticate
from orgin.ent.premission import create_token, AuthBearer
from orgin.ent.schema import MessageOut
from orgin.ent.utils import response
from process.models import Products
from Distributors.models import Distributors
from .models import EmailAccount
from .schema import AccountSignupOut, AccountSignupIn, AccountSigninOut,\
    AccountSigninIn, AccountOut, AccountUpdateIn, PasswordChangeIn
from django.shortcuts import get_object_or_404

auth_controller = Router(tags=['Auth'])


@auth_controller.post('/signup', response={200: AccountSignupOut, 403: MessageOut, 500: MessageOut})
def register(request, payload: AccountSignupIn):
    _id = None
    if payload.password1 != payload.password2:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords does not match!'})

    try:
        EmailAccount.objects.get(email=payload.email)
        return response(403,
                        {'message': 'Forbidden, email is already registered'})
    except EmailAccount.DoesNotExist:
        user = EmailAccount.objects.create_user(first_name=payload.first_name, last_name=payload.last_name,
                                                email=payload.email, password=payload.password1)
        user.save()
        if user:
            if not payload.account_type:
                Distributor = Distributors.objects.create(user=user)
                Distributor.save()
                _id = Distributor.id
            elif payload.account_type:
                if payload.account_type == 'Distributor':
                    Distributor = Distributors.objects.create(user=user)
                    Distributor.save()
                    _id = Distributor.id
                elif payload.account_type == 'Product':
                    product = Products.objects.create(user=user)
                    product.save()
                    _id = product.id
                
            token = create_token(user.id)
            return response(HTTPStatus.OK, {
                'profile': user,
                'token': token,
                'profile_id': _id
            })
        else:
            return response(HTTPStatus.INTERNAL_SERVER_ERROR, {'message': 'An error occurred, please try again.'})



@auth_controller.post('/signin', response={200: AccountSigninOut, 404: MessageOut})
def login(request, payload: AccountSigninIn):
    profile_id = None

    user = authenticate(email=payload.email, password=payload.password)
    if user is not None:
        if user.account_type == 'Distributor':
            Distributor = Distributors.objects.get(user=user)
            profile_id = Distributor.id
        elif user.account_type == 'Distributor':
            Distributor = Distributors.objects.get(user=user)
            profile_id = Distributor.id
        return response(HTTPStatus.OK, {
            'profile': user,
            'token': create_token(user.id),
            'profile_id': profile_id
        })
    return response(HTTPStatus.NOT_FOUND, {'message': 'User not found'})


@auth_controller.get('/me',
                     auth=AuthBearer(),
                     response={200: AccountOut, 400: MessageOut})
def me(request):
    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})
    return response(HTTPStatus.OK, user)


@auth_controller.put('/me',
                     auth=AuthBearer(),
                     response={200: AccountOut, 400: MessageOut})
def update_me(request, user_in: AccountUpdateIn):
    EmailAccount.objects.filter(id=request.auth.id).update(**user_in.dict())
    user = get_object_or_404(EmailAccount, id=request.auth.id)
    if not user:
        return response(HTTPStatus.BAD_REQUEST, data={'message': 'something went wrong'})
    return response(HTTPStatus.OK, user)


@auth_controller.post('/change-password',
                      auth=AuthBearer(),
                      response={200: MessageOut, 400: MessageOut})
def change_password(request, payload: PasswordChangeIn):
    if payload.new_password1 != payload.new_password2:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords do not match!'})

    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})

    user_update = authenticate(email=user.email, password=payload.old_password)

    if user_update is not None:
        user_update.set_password(payload.new_password1)
        user_update.save()
        return response(HTTPStatus.OK, {'message': 'password updated'})

    return response(HTTPStatus.BAD_REQUEST, {'message': 'something went wrong, please try again later'})