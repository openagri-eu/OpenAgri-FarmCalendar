from urllib.parse import urljoin
from django.conf import settings

import requests


class AgstackClient:
    """
    A simple client for interacting with the AgStack API.
    """

    def __init__(self):
        self.asset_api_url = settings.AGSTACK_ASSET_REGISTY_API_URL
        self.user_api_url = settings.AGSTACK_USER_REGISTY_API_URL
        self.access_token = settings.AGSTACK_ACCESS_TOKEN
        self.refresh_token = settings.AGSTACK_REFRESH_TOKEN
        self.refresh_token_url = urljoin(self.user_api_url, settings.AGSTACK_ENDPOINTS['refresh_token'])
        self.register_field_url = urljoin(self.asset_api_url, settings.AGSTACK_ENDPOINTS['register_field_boundary'])

    def _refresh_access_token(self):
        """Refresh the access token using the refresh token as a cookie"""

        response = requests.get(
            self.refresh_token_url,
            cookies={"refresh_token_cookie": self.refresh_token}
        )
        self.access_token = response.json()["access_token"]

    def register_field_boundary(self, wkt_geometry, threshold=95, s2_index=(8, 13)):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-FROM-ASSET-REGISTRY": "True",
            "Content-Type": "application/json"
        }

        data = {
            "wkt": wkt_geometry,
        }

        endpoint_url = self.register_field_url
        resp = requests.post(endpoint_url, json=data, headers=headers)
        # If token expired, refresh and retry once
        if resp.status_code == 401 or 'invalid token' in resp.json().get('message', '').lower():
            self._refresh_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            resp = requests.post(endpoint_url, json=data, headers=headers)

        geo_id = None
        try:
            result = resp.json()
            if 'Geo Id' in result:
                geo_id = result['Geo Id']
            elif 'matched geo ids' in result:
                geo_id = result['matched geo ids'][0]
            else:
                raise ValueError("Invalid response from AgStack API")
        except Exception as e:
            raise ValueError("Invalid response from AgStack API")
        return geo_id


if __name__ == '__main__':
    client = AgstackClient()
    wkt_geometry = "POLYGON((5.714800882907841 50.83967331197391,5.714729694830028 50.839206943235155,5.716022320453463 50.839169065366434,5.715939892152838 50.83967094463168,5.714800882907841 50.83967331197391))"
    print(client.register_field_boundary(wkt_geometry))
