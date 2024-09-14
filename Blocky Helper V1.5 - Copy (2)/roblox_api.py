import requests

class RobloxApi:
    def __init__(self, api_key=None, cookie=None):
        self.api_key = api_key
        self.cookie = cookie
        self.session = requests.Session()
        self.authenticated = False

        if cookie:
            self.session.cookies.set('.ROBLOSECURITY', cookie)
            self.authenticated = True

    def _get_headers(self):
        headers = {
            'Content-Type': 'application/json',
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def get_user_info(self, user_id):
        url = f'https://users.roblox.com/v1/users/{user_id}'
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error fetching user info: {e}')
            return None

    def get_user_friends(self, user_id, limit=200):
        url = f'https://friends.roblox.com/v1/users/{user_id}/friends'
        try:
            response = self.session.get(url, headers=self._get_headers(), params={'limit': limit})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error fetching user friends: {e}')
            return None

    def get_group_info(self, group_id):
        url = f'https://groups.roblox.com/v1/groups/{group_id}'
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error fetching group info: {e}')
            return None

    def get_group_members(self, group_id, limit=100):
        url = f'https://groups.roblox.com/v1/groups/{group_id}/users'
        try:
            response = self.session.get(url, headers=self._get_headers(), params={'limit': limit})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error fetching group members: {e}')
            return None

    def authenticate(self):
        print("Direct authentication using username and password is not supported via API.")
        return False

    def check_authentication(self):
        if self.authenticated:
            print("Authenticated using .ROBLOSECURITY cookie.")
            return True
        else:
            print("No authentication cookie provided.")
            return None
    def _update_csrf_token(self):
        url = 'https://auth.roblox.com/v2/logout'
        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 403:
                # The X-CSRF-Token is returned in the headers of a 403 response
                self.session.headers['X-CSRF-TOKEN'] = response.headers['x-csrf-token']
        except requests.RequestException as e:
            print(f'Error updating CSRF token: {e}')

    def get_authenticated_user(self):
        self._update_csrf_token()  # Ensure CSRF token is up to date
        url = 'https://users.roblox.com/v1/users/authenticated'
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error fetching authenticated user info: {e}')
            return None

    def get_user_games(self, user_id, limit=100):
        url = f'https://games.roblox.com/v2/users/{user_id}/games'
        try:
            response = self.session.get(url, headers=self._get_headers(), params={'limit': limit})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error fetching user games: {e}')
            return None

    def get_group_roles(self, group_id):
        url = f'https://groups.roblox.com/v1/groups/{group_id}/roles'
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error fetching group roles: {e}')
            return None

    def get_role_id_by_name(self, group_id, role_name):
        roles = self.get_group_roles(group_id)
        if roles:
            for role in roles.get('roles', []):
                if role['name'].lower() == role_name.lower():
                    return role['id']
        return None
    def get_user_rank_in_group(self, group_id, user_id):
        try:
            url = f'https://groups.roblox.com/v1/groups/{group_id}/users/{user_id}'
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            data = response.json()
            return data.get('role').get('rank')
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        return None
        
    def rank_user(self, group_id, user_id, new_role_id):
        url = f'https://groups.roblox.com/v1/groups/{group_id}/users/{user_id}'
        data = {
            'roleId': new_role_id
        }
        try:
            response = self.session.patch(url, headers=self._get_headers(), json=data)
            response.raise_for_status()  # This will raise an HTTPError if the response was unsuccessful
            if response.status_code == 200:
                return True
            else:
                print(f"Unexpected status code: {response.status_code}")
                return False
        except requests.HTTPError as http_err:
       
            if response.status_code == 403:
                print(f'Error ranking user: 403 Forbidden. This likely means the bot does not have the necessary permissions, or The user is already at the specified new rank  ')
            elif response.status_code == 400:
                print('Error ranking user: 400 Bad Request. Please check the provided data. or the bot is just dumb lol')
            elif response.status_code == 404:
                print('Error ranking user: 404 Not Found. Please check the group and user IDs.')
            elif response.status_code == 503:
                print('Error ranking user: 503 The request could not be satisfied. Roblox is down due to an outage or downtime.')
            else:
                print(f'HTTP error occurred: {http_err}')
            return False
        except requests.RequestException as e:
            print(f'Error ranking user: {e}')
            return False
        
    def exile_user(self, group_id, user_id):
        # Ensure CSRF token is up to date
        self._update_csrf_token()
        headers = self._get_headers()
        headers.update({'X-CSRF-TOKEN': self.session.headers.get('X-CSRF-TOKEN', '')})

        try:
            response = self.session.delete(
                f'https://groups.roblox.com/v1/groups/{group_id}/users/{user_id}',
                headers=headers
            )
            response.raise_for_status()
            print(f"User with ID {user_id} exiled.")
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred while exiling user {user_id}: {http_err}')
            if response.status_code == 403:
                print('Error: Forbidden. The bot may not have the necessary permissions.')
            elif response.status_code == 404:
                print('Error: Not Found. Check the group and user IDs.')
        except requests.RequestException as e:
            print(f"Failed to exile user with ID {user_id}: {e}")

    
    def get_username_by_user_id(self, user_id):
        user_info = self.get_user_info(user_id)
        if user_info:
            return user_info.get('name')
        return None

    def get_user_id_by_username(self, username):
        url = 'https://users.roblox.com/v1/usernames/users'
        data = {
            'usernames': [username]
        }
        try:
            response = self.session.post(url, headers=self._get_headers(), json=data)
            response.raise_for_status()
            results = response.json().get('data')
            if results:
                return results[0].get('id')
            return None
        except requests.RequestException as e:
            print(f'Error fetching user ID: {e}')
            return None
        
