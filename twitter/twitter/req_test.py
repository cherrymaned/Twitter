import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# This is the 2.11 Requests cipher string, containing 3DES.
CIPHERS = (
    'ECDHE-RSA-AES256-GCM-SHA384'
)
headers = {'authority': 'twitter.com',
'method': 'GET',
'path': '/i/api/graphql/wsgiAScXAATH6OItSwqdZA/ListSubscribers?variables=%7B%22listId%22%3A%2234683112%22%2C%22count%22%3A20%2C%22cursor%22%3A%221666557371470596496%7C1539376863988678590%22%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%7D&features=%7B%22dont_mention_me_view_api_enabled%22%3Atrue%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_uc_gql_enabled%22%3Afalse%2C%22vibe_tweet_context_enabled%22%3Afalse%2C%22responsive_web_edit_tweet_api_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D',
'scheme': 'https',
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
'content-type': 'application/json',
'cookie': 'kdt=FDoxAx0ALY6rng8gBjxVuuAjm2hoLbQN9hdBwRSX; des_opt_in=Y; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A165462436114002252; guest_id_marketing=v1%3A165462436114002252; personalization_id="v1_gIw7/uGV3A79WzQNGSb0Yw=="; guest_id=v1%3A165462491487486291; ads_prefs="HBERAAA="; g_state={"i_l":1,"i_p":1654633096778}; auth_token=6e66b4e8263d9d9c7de6ac9f69f424532e3cea5d; ct0=4dc21af767197dc4fafda8fc702b5f51bbe1d423075de323ce106ed36ecf5a1dde5d4401eaca77d69b4e7d28bae7bc7f87065eb89491d0ac5a361f6b6eafe56056a0e86d803c760b63c766d7099ae01f; twid=u%3D1534236395102949376; dnt=1; mbox=PC#5937d99358e44372888e300828cbbad4.34_0#1718833881|session#4536004dca1e4802a07252ab59701aab#1655590941; external_referer=padhuUp37zhVBrP7koDaKNSjNjxAM0292FB6Go%2BR8EYJ%2FHrUctSkqA%3D%3D|0|8e8t2xd8A2w%3D; lang=en',
'referer': 'https://twitter.com/i/lists/34683112/followers',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Opera GX";v="87"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.58',
'x-csrf-token': '4dc21af767197dc4fafda8fc702b5f51bbe1d423075de323ce106ed36ecf5a1dde5d4401eaca77d69b4e7d28bae7bc7f87065eb89491d0ac5a361f6b6eafe56056a0e86d803c760b63c766d7099ae01f',
'x-twitter-active-user': 'yes',
'x-twitter-auth-type': 'OAuth2Session',
'x-twitter-client-language': 'en',
}

class DESAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)

s = requests.Session()
url = 'https://twitter.com/i/api/graphql/wsgiAScXAATH6OItSwqdZA/ListSubscribers?variables={"listId":"76158304","count":12,"cursor":"1445138571803010559|1539386114865889178","withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}&features={"dont_mention_me_view_api_enabled":true,"interactive_text_enabled":true,"responsive_web_uc_gql_enabled":false,"vibe_tweet_context_enabled":false,"responsive_web_edit_tweet_api_enabled":false,"standardized_nudges_misinfo":false,"responsive_web_enhance_cards_enabled":false}'
s.mount(url, DESAdapter())
r = s.get(url, headers = headers)
print(r)