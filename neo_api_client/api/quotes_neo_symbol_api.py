import urllib.parse
from json import JSONDecodeError


class QuotesAPI(object):

    def __init__(self, api_client):
        self.api_client = api_client
        self.rest_client = api_client.rest_client

    def get_quotes(self, instrument_tokens=None, quote_type=None):
        if not quote_type:
            quote_type = 'all'
        neo_symbol_str = ",".join(f"{item['exchange_segment']}|{item['instrument_token']}" for item in instrument_tokens)
        encoded_neo_symbol_str = urllib.parse.quote(neo_symbol_str)
        header_params = {
            "Authorization": self.api_client.configuration.consumer_key,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        URL = self.api_client.configuration.get_url_details("quotes_neo_symbol")
        URL = URL.format(neo_symbols=encoded_neo_symbol_str, quote_type=quote_type)
        quotes = self.rest_client.request(
            url=URL, method='GET',
            headers=header_params
        )
        try:
            quotes_data = quotes.json()
        except JSONDecodeError:
            return {
                "Error": "Unexpected response format. Expected JSON but received something else."
            }
        return quotes_data