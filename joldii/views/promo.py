from __future__ import unicode_literals

from django.http import HttpResponse
from django.views import View

from joldii.constants import consts

from joldii.models import SessionModel
from joldii.models import VehicleClassModel
from joldii.models import UserPromoModel
from joldii.models import PromoModel

from joldii.responses.response_update_location import UpdateLocationResponse
from joldii.responses import common_response


class AddPromo(View):
    @staticmethod
    def post(request):

        try:
            name = request.POST[consts.PARAM_PROMO_CODE]
            vehicle_type = request.POST[consts.PARAM_VEHICLE_TYPE]
            maximum_number_of_discount = request.POST[consts.PARAM_PROMO_NUMBER_OF_RIDE]
            discount = request.POST[consts.PARAM_PROMO_AMOUNT_OF_DISCOUNT]

            if PromoModel.objects.filter(vehicle_type=VehicleClassModel.objects.get(pk=vehicle_type)).exists():
                response = common_response.CommonResponse(success=False,
                                                          reason='Promo Ongoing Already',
                                                          error_code=consts.ERROR_ONGOING_PROMO)
                return HttpResponse(response.respond(), content_type="application/json")
            else:
                new_promo = PromoModel(name=name,
                                       vehicle_type=VehicleClassModel.objects.get(pk=vehicle_type),
                                       maximum_number_of_discount=maximum_number_of_discount,
                                       discount=discount)
                new_promo.save()
                response = common_response.CommonResponse(success=True,
                                                          reason='New Promo Added',
                                                          error_code=consts.ERROR_NONE)
                return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")


class RedeemPromo(View):
    @staticmethod
    def post(request):

        try:
            if PromoModel.objects.filter(name=request.POST[consts.PARAM_PROMO_CODE]).exists():
                sess_id = request.POST[consts.PARAM_SESSION_ID]
                user = SessionModel.get_user_by_session(sess_id)
                selected_promo = PromoModel.objects.get(name=request.POST[consts.PARAM_PROMO_CODE])
                if UserPromoModel.objects.filter(user=user, promo=selected_promo).exists():
                    response = common_response.CommonResponse(success=False,
                                                              reason='Promo Code Already Used',
                                                              error_code=consts.ERROR_USED_PROMO)
                    return HttpResponse(response.respond(), content_type="application/json")
                else:
                    new_user_promo = UserPromoModel(user=user,
                                                    promo=selected_promo,
                                                    remaining_ride=selected_promo.maximum_number_of_discount)
                    new_user_promo.save()
                    response = common_response.CommonResponse(success=True,
                                                              reason='Promo Successfully Added',
                                                              error_code=consts.ERROR_NONE)
                    return HttpResponse(response.respond(), content_type="application/json")
            else:
                response = common_response.CommonResponse(success=False,
                                                          reason='Incorrect Promo',
                                                          error_code=consts.ERROR_INCORRECT_PROMO)
                return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")
