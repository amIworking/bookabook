from rest_framework.exceptions import APIException


class AccountAlreadyActivated(APIException):
    status_code = 400
    default_detail = "Your account already has been activated"
    default_code = "account_already_activated"


class AccountDoesNotExist(APIException):
    status_code = 404
    default_detail = "This account does not exist"
    default_code = "account_does_not_exist"


class TokenIsInvalidOrGotInspired(APIException):
    status_code = 400
    default_detail = ("Your verify token got inspired "
                      "or you're trying to send an invalid one")
    default_code = "token_is_invalid_or_got_inspired"
