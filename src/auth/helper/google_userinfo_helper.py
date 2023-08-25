from googleapiclient.discovery import build


def get_userinfo(credentials):
    user_info_service = build(serviceName='oauth2', version='v2', credentials=credentials)
    return user_info_service.userinfo().get().execute()     # pylint: disable=E1101
