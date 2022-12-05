# from .client_ip_address import get_client_ip_address
# from django.conf import settings
# import requests
#
# def clean(request):
#     secret_key = settings.RECAPTCHA_SECRET_KEY
#
#     # captcha verification
#     data = {
#         'response': request.POST.get('g-recaptcha-response'),
#         'secret': secret_key,
#     }
#     resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
#     result_json = resp.json()
#
#     return result_json.get('success')
