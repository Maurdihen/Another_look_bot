import webbrowser
import wsgiref.simple_server
from datetime import datetime

from google_auth_oauthlib.flow import _RedirectWSGIApp, _WSGIRequestHandler, InstalledAppFlow


def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')

    now = datetime.now()

    if date_obj.date() == now.date():
        date_obj = date_obj.replace(hour=now.hour, minute=now.minute, second=now.second)
    else:
        date_obj = date_obj.replace(hour=0, minute=0, second=0)

    iso_format = date_obj.isoformat()

    return iso_format


url = None

data = {
    "bind_addr": None,
    "host": "localhost",
    "port": 0,
    "redirect_uri_trailing_slash": True,
    "timeout_seconds": None,
    "open_browser": True,
    "authorization_prompt_message": "Please visit this URL to authorize this application: {url}",
    "success_message": "The authentication flow has completed. You may close this window.",
}


def create_auth_link(credentials_file_path, data):
    bind_addr = data.get('bind_addr')
    host = data.get('host')
    port = data.get('port')
    redirect_uri_trailing_slash = data.get('redirect_uri_trailing_slash')
    success_message = data.get('success_message')

    flow = InstalledAppFlow.from_client_secrets_file(credentials_file_path,
                                                     ["https://www.googleapis.com/auth/calendar"])

    wsgi_app = _RedirectWSGIApp(success_message)
    wsgiref.simple_server.WSGIServer.allow_reuse_address = False
    local_server = wsgiref.simple_server.make_server(
        bind_addr or host, port, wsgi_app, handler_class=_WSGIRequestHandler
    )
    redirect_uri_format = (
        "http://{}:{}/" if redirect_uri_trailing_slash else "http://{}:{}"
    )
    flow.redirect_uri = redirect_uri_format.format(host, local_server.server_port)
    auth_url, _ = flow.authorization_url(access_type="offline")

    return auth_url, flow, local_server, wsgi_app


def run_server(auth_url, flow, local_server, wsgi_app, data):
    open_browser = data.get('open_browser')
    authorization_prompt_message = data.get('authorization_prompt_message')
    timeout_seconds = data.get('timeout_seconds')

    if open_browser:
        webbrowser.open(auth_url, new=1, autoraise=True)

    if authorization_prompt_message:
        print(authorization_prompt_message.format(url=auth_url))

    local_server.timeout = timeout_seconds
    local_server.handle_request()

    authorization_response = wsgi_app.last_request_uri.replace("http", "https")
    flow.fetch_token(authorization_response=authorization_response)
    local_server.server_close()

    return flow.credentials


if __name__ == "__main__":
    auth_url, flow, local_server, wsgi_app = create_auth_link("./calendar_api/credentials.json")

    print(run_server(auth_url, flow, local_server, wsgi_app))
