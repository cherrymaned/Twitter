import scrapy
from twitter.items import Profile
import json
import requests
urls = [
    'https://twitter.com/cnnbrk',
    ]
    
headers = {
'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
'x-csrf-token': '4dc21af767197dc4fafda8fc702b5f51bbe1d423075de323ce106ed36ecf5a1dde5d4401eaca77d69b4e7d28bae7bc7f87065eb89491d0ac5a361f6b6eafe56056a0e86d803c760b63c766d7099ae01f',
}

cookies = {
"kdt": "FDoxAx0ALY6rng8gBjxVuuAjm2hoLbQN9hdBwRSX",
"des_opt_in": "Y",
"d_prefs": "MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw",
"guest_id_ads": "v1%3A165462436114002252",
"guest_id_marketing": "v1%3A165462436114002252",
"personalization_id": "\"v1_gIw7/uGV3A79WzQNGSb0Yw==\"",
"guest_id": "v1%3A165462491487486291",
"at_check": "true",
"ads_prefs": "\"HBERAAA=\"",
"_twitter_sess": "BAh7ECIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADofbGFzdF9wYXNzd29yZF9jb25maXJtYXRpb24i%250AFTE2NTQ2MjU1MjQ3MzMwMDA6HnBhc3N3b3JkX2NvbmZpcm1hdGlvbl91aWQi%250AGDE1MzQyMzYzOTUxMDI5NDkzNzY6B2lkIiVkMGJlMDM0NGEwMWY0NTkyNDcw%250AZmFhMGU0MzZhNmM2ZDoPY3JlYXRlZF9hdGwrCCqHYj%252BBAToMY3NyZl9pZCIl%250AY2RiZWRhNDdhMTVjMDdhOThjYzVmMmE3YzBlM2YzYTg6CXVzZXJsKwkDQFba%250AzI8zFDoIcHJzaQw6CHBydWwrCQNAVtrMjzMUOghwcmwiK1g4Y1FJUmdaWUk5%250AV2xnN2ExeHdaSXlhb3BBZXBLVE51TzlqVGJWOghwcmFpBg%253D%253D--e5dac817ee13331b401272166c1a9ec9d90f7d0a",
"g_state": "{\"i_l\":1,\"i_p\":1654633096778}",
"auth_token": "6e66b4e8263d9d9c7de6ac9f69f424532e3cea5d",
"ct0": "4dc21af767197dc4fafda8fc702b5f51bbe1d423075de323ce106ed36ecf5a1dde5d4401eaca77d69b4e7d28bae7bc7f87065eb89491d0ac5a361f6b6eafe56056a0e86d803c760b63c766d7099ae01f",
"twid": "u%3D1534236395102949376",
"lang": "en",
"dnt": "1",
"mbox": "PC#5937d99358e44372888e300828cbbad4.34_0#1718833881|session#4536004dca1e4802a07252ab59701aab#1655590941",
"external_referer": "padhuUp37zhVBrP7koDaKNSjNjxAM0292FB6Go%2BR8EYJ%2FHrUctSkqA%3D%3D|0|8e8t2xd8A2w%3D"
}

class ListingsSpider(scrapy.Spider):
    name = 'listings'
    allowed_domains = ['twitter.com']
    
    def start_requests(self):

        for url in urls:
            profile = Profile()
            short_name = url.split('/')[-1]
            profile['source'] = 'https://twitter.com/'+short_name
            yield scrapy.Request(
                url = 'https://twitter.com/i/api/graphql/mCbpQvZAw6zu_4PvuAUVVQ/UserByScreenName'
                +'?variables={"screen_name":"'+short_name+'","withSafetyModeUserFields":true,"withSuperFollowsUserFields":true}', 
                method = 'GET',
                headers = headers,
                cookies = cookies,
                meta = {'item': profile},
                callback = self.get_id, 
                )

    def get_id(self, response):
        profile = response.meta['item']
        
        id_ = json.loads(response.text)['data']['user']['result']['rest_id']

        yield scrapy.Request(
                url = 'https://twitter.com/i/api/graphql/BsFasY6imwe0bVCJLIDyYQ/CombinedLists'
                +'?variables=%7B%22userId%22%3A%22'+id_+'%22%2C%22count%22%3A100%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%7D&features=%7B%22dont_mention_me_view_api_enabled%22%3Atrue%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_uc_gql_enabled%22%3Afalse%2C%22vibe_tweet_context_enabled%22%3Afalse%2C%22responsive_web_edit_tweet_api_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D', 
                method = 'GET',
                headers = headers,
                cookies = cookies,
                meta = {'item': profile},
                callback = self.get_listings, 
                )
    
    def get_listings(self, response):
        profile = response.meta['item']

        profile['lists'] = []
        
        lists = [entry['entryId'][5:] for entry in json.loads(response.text)['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][:-2]]
        
        for listing in lists:
                yield scrapy.Request(
                                url = 'https://twitter.com/i/api/graphql/BpXQqi3VImT8bR7pAf26rg/ListByRestId?variables={"listId":"'+listing+'","withSuperFollowsUserFields":true}',
                                method = 'GET',
                                headers = headers,
                                cookies = cookies,
                                meta = {'item': profile, 'listing': listing, 'lists_count': len(lists)},
                                callback = self.get_listing_followers_count, 
                                )
    

    def get_listing_followers_count(self, response):
        profile = response.meta['item']
        lists_count = response.meta['lists_count']
        listing = response.meta['listing']
        listing_count = json.loads(response.text)['data']['list']['member_count']
        url = 'https://twitter.com/i/api/graphql/bs1ZNl4FXKtG4qbd6a79Sw/ListMembers'
        url += '?variables={"listId":"'+str(listing)
        url += '","count":'+str(min(listing_count, 100))+',"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}&features={"dont_mention_me_view_api_enabled":true,"interactive_text_enabled":true,"responsive_web_uc_gql_enabled":false,"vibe_tweet_context_enabled":false,"responsive_web_edit_tweet_api_enabled":false,"standardized_nudges_misinfo":false,"responsive_web_enhance_cards_enabled":false}'
        yield scrapy.Request(
                            url = url,
                            method = 'GET',
                            headers = headers,
                            cookies = cookies,
                            meta = {'item': profile, 'listing': listing, 'lists_count': lists_count, 'listing_count': listing_count, 'accounts': []},
                            callback = self.get_listing_followers, 
                            )
        
    def get_listing_followers(self, response):
        profile = response.meta['item']
        lists_count = response.meta['lists_count']
        listing = response.meta['listing']
        listing_count = response.meta['listing_count']
        accounts = response.meta['accounts']
        listing_count-=min(listing_count, 100)

        if len(accounts)==0:
            entries = json.loads(response.text)['data']['list']['members_timeline']['timeline']['instructions'][-1]['entries']
        else:
            entries = json.loads(response.text)['data']['list']['members_timeline']['timeline']['instructions'][-1]['entries']
    
        for entire in entries[:-2]:
            try:
                accounts.append('twitter.com/'+entire['content']['itemContent']['user_results']['result']['legacy']['screen_name'])
            except:
                accounts.append(None)
        if listing_count!=0:
            cursor = (entries[-2]['content']['value']).replace('|', '%7C')
            url = 'https://twitter.com/i/api/graphql/bs1ZNl4FXKtG4qbd6a79Sw/ListMembers?'
            url += 'variables={"listId":"'+str(listing)+'","count":'+str(min(listing_count, 100))+',"cursor":"'+cursor+'",'
            url += '"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}&features={"dont_mention_me_view_api_enabled":true,"interactive_text_enabled":true,"responsive_web_uc_gql_enabled":false,"vibe_tweet_context_enabled":false,"responsive_web_edit_tweet_api_enabled":false,"standardized_nudges_misinfo":false,"responsive_web_enhance_cards_enabled":false}'
            yield scrapy.Request(
                            url = url,
                            method = 'GET',
                            headers = headers,
                            cookies = cookies,
                            meta = {'item': profile, 'listing': listing, 'lists_count': lists_count, 'listing_count': listing_count, 'accounts': accounts},
                            callback = self.get_listing_followers,
                            )
        else:
            profile['lists'].append({'members': accounts, 'source': 'twitter.com/i/lists/'+listing})
            #profile['lists']['']
        if len(profile['lists'])==lists_count:
            yield profile