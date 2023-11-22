import requests
import json
import socket
from src.downloader.Exceptions import ClientException,  ApiException, AuthException, ConfigException, ServerException


class RequestService:
    def __init__(self, moduleOptions, apiSession):
        """
        Initializes the RequestSender object.

        Args:
            moduleOptions (dict): A dictionary containing the module options.
            apiSession (dict): A dictionary containing the API session information.
                If not provided, it will default to {'apiKey': None, 'contactId': 0}.
        """
        self.apiSession = apiSession
        if not apiSession:
            self.apiSession = {'apiKey': None, 'contactId': 0}
        self.moduleOptions = moduleOptions
    
    def authenticate(self):
            """
            Authenticates the user with the provided credentials.

            Returns:
                bool: True if authentication is successful, False otherwise.
            """
            catalog = 'EE'
            if self.moduleOptions.getEndpoint().find('hddsexplorer') != -1:
                catalog = 'HDDS'

            parameters = {
                'username' : self.moduleOptions.getUsername(),
                'token' : self.moduleOptions.getToken(),
                'authType' : 'EROS',
                'catalogId' : catalog
            }
            
            # contactId = 0
            # if (self.identity):
            #     contactId = self.identity.getContactId()
            #     parameters.update({'userContext' : {'contactId' : contactId,
            #                                        'ipAddress' : self.ipManager.getClientIpAddress()}})

            try:           
                response = self.dispatchRequest('login-token', parameters, raw=True)
                self.apiSession.update({'apiKey': response['data']})
                return True
            except Exception as ex:
                print("[Exception]", ex)
                return False
    
    def dispatchRequest(self, reqRoute, requestParameters=None, enforceLogin=False, raw=False) -> dict:
        """
        Sends a request to the specified route and returns the response.

        Args:
            reqRoute (str): The route to send the request to.
            requestParameters (dict, optional): The parameters to include in the request. Defaults to None.
            enforceLogin (bool, optional): Whether to enforce login for the request. Defaults to False.
            raw (bool, optional): Whether to return the raw response or convert it to a dictionary. Defaults to False.

        Raises:
            ClientException: If login is required and authentication fails.

        Returns:
            dict: The response from the request.
        """
        if reqRoute != 'login-token' and (enforceLogin == True and self.apiSession['apiKey'] == None):    
            authResult = self.authenticate()

            if authResult == False:
                raise ClientException('Login was required for this method and authenticated failed')

        url = self.moduleOptions.getEndpoint() + reqRoute

        headers = None
        if self.apiSession['apiKey'] != None:
            headers = {'X-Auth-Token': self.apiSession['apiKey']}

        payload = {}

        if requestParameters != None:   
            payload = json.dumps(requestParameters)

        response = requests.post(url, payload, headers=headers, timeout=self.moduleOptions.getTimeout())
        return self.convertResponse(response, raw)
    
    def convertResponse(self, response, raw) -> dict:
            """
            Converts the response from the API into a dictionary.

            Args:
                response (Response): The response object from the API.
                raw (bool): Flag indicating whether to return the raw response or just the data.

            Returns:
                dict: The converted response as a dictionary.

            Raises:
                ClientException: If unable to parse JSON response or if the response is empty.
                ApiException: If errorCode, errorMessage, data, requestId, or version is missing from the server response.
            """
            result = json.loads(response.text)
            if result == None:
                raise ClientException('Unable to parse JSON response from API')

            if result == None:
                raise ClientException('Empty response from API')

            if 'errorCode' not in result:
                raise ApiException('errorCode is missing from server response')

            if 'errorMessage' not in result:
                raise ApiException('errorMessage is missing from server response')

            if 'data' not in result:
                raise ApiException('data is missing from server response')

            if 'requestId' not in result:
                raise ApiException('requestId is missing from server response')

            if 'version' not in result:
                raise ApiException('version is missing from server response')

            if result['errorCode'] != None:
                raise ClientException(result['errorCode']+": "+ result['errorMessage'])
            if raw:
                return result
            else:
                return result['data']
    
    def getApiKey(self):
        """
        Returns the API key associated with the current session.

        Returns:
            str: The API key.
        """
        return self.apiSession['apiKey']

    def setApiKey(self, apiKey):    
        """
        Set the API key for the request sender.

        Parameters:
        apiKey (str): The API key to be set.

        Returns:
        None
        """
        self.apiSession.update({'apiKey' : apiKey})
    
    def getEndpoint(self):
        """
        Returns the endpoint of the request sender.
        """
        return self.moduleOptions.getEndpoint()
    
    def logout(self):    
            """
            Logs out the user by dispatching a 'logout' request and resetting the API session.

            Returns:
                bool: True if the user is successfully logged out, False otherwise.
            """
            try:
                # self.dispatchRequest('logout')
                if self.apiSession['apiKey'] == None:
                    return True    
                self.dispatchRequest('logout', None)
                self.apiSession['apiKey'] = None
                # self.apiSession['contactId'] = 0
                return True
            except: 
                return False
    
class ModuleOptionsInterface:
    """
    Haven't implemented this yet.
    Interface for module options.
    """

    def getEndpoint() -> str:
        """Get the endpoint URL."""
        pass
    
    def getToken() -> str:
        """Get the authentication token."""
        pass
    
    def getTimeout() -> int:
        """Get the timeout value."""
        pass
    
    def getUsername() -> str:
        """Get the username."""
        pass

class ModuleOptions(ModuleOptionsInterface):
    username = None
    token = None
    timeOut = None
    endPoint = None
    
    def __init__(self, username, token, timeout=100):
        """
        Initializes the RequestSender object.

        Args:
            username (str): The username for authentication.
            token (str): The token for authentication.
            timeout (int, optional): The timeout value in seconds. Defaults to 100.
        """
        config = {
            'timeout'    : timeout,
            'username'   : username,
            'token'   : token,
            'endpoint'   : 'https://m2m.cr.usgs.gov/api/api/json/stable/',
        }
        
        self.setUsername(config)
        self.setToken(config)
        self.setTimeout(config)
        self.setEndpoint(config)

    def getUsername(self):
       return self.username
    
    def getToken(self):    
       return self.token

    def getTimeout(self):       
       return self.timeout

    def getEndpoint(self):
       return self.endpoint

    def setUsername(self, config): 
       self.username = config["username"]
    
    def setToken(self, config): 
        self.token = config["token"]
  
    def setTimeout(self, config):  
        self.timeout = config["timeout"]   
    
    def setEndpoint(self, config):
        self.endpoint = config["endpoint"]
        

