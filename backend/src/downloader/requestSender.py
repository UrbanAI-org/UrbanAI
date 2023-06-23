import requests
import json
import socket
from src.downloader.Exceptions import ClientException,  ApiException, AuthException, ConfigException, ServerException


class RequestService:
    def __init__(self, moduleOptions, apiSession):
        self.apiSession = apiSession
        if not apiSession:
            self.apiSession = {'apiKey' : None, 'contactId' : 0}
        self.moduleOptions =  moduleOptions
    
    def authenticate(self):
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
    
    def dispatchRequest(self, reqRoute, requestParameters = None, enforceLogin = False, raw=False) -> dict:
        if reqRoute != 'login-token' and (enforceLogin == True and self.apiSession['apiKey'] == None):    
            # print(reqRoute != 'login-token', (enforceLogin == True and self.apiSession['apiKey'] == None), (self.apiSession['contactId'] == None or self.apiSession['contactId'] == 0))
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
           
        response = requests.post(url, payload, headers = headers, timeout = self.moduleOptions.getTimeout())
        # print(response.text)
        return self.convertResponse(response, raw)
    
    def convertResponse(self, response, raw) -> dict:    
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
        return self.apiSession['apiKey']    

    def setApiKey(self, apiKey):    
        self.apiSession.update({'apiKey' : apiKey})
    
    def getEndpoint(self):
        return self.moduleOptions.getEndpoint()
    
    def logout(self):    
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
    def getEndpoint() -> str:
        pass
    
    def getToken() -> str:
        pass
    
    def getTimeout() -> int:
        pass
    
    def getUsername() -> str:
        pass

class ModuleOptions(ModuleOptionsInterface):
    username = None
    token = None
    timeOut = None
    endPoint = None
    
    def __init__(self, username, token, timeout=100):        
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
        











# import base64

# class Endpoint:
#     ENDPOINT = None
#     apiSessionId = None
#     apiKey = None
#     baseUrl = None
#     permission = '*'
#     inputParams = []
#     label = ''
#     requestId = None
#     summary = ''
#     config = None
#     authService = None
#     logger = None
#     userContext = None
    
#     def __init__(self, apiKey, config, authService, logger, baseUrl):            
#         self.apiKey = apiKey
#         self.authService = authService
#         self.baseUrl = baseUrl
#         self.config = config
#         self.logger = logger 

#     def getApiKey(self):    
#         return self.apiKey

#     def getBaseUrl(self):    
#         return self.baseUrl
    
#     def addInputParam(self, param):
#         param.setParameterList(self.config['api']['parameterTypes'])

#         self.inputParams[param.getKey()] = param
    
#     def getInputParameter(self, paramKey):    
#         return self.inputParams[paramKey]    
    
#     def getInputParameters(self):    
#         return self.inputParams
    
#     def getPermissionListForRoles(self, identityRoles):
#         roles = []
#         for role in identityRoles:
#             roles.append(role) if type(role) == str else roles.append(role.getName())
			
#         permissions = []
#         if 'Developer' in roles:
#             self.addToPermissions('application', permissions)
#             self.addToPermissions('bma', permissions)
#             self.addToPermissions('dds', permissions)
#             self.addToPermissions('developer', permissions)
#             self.addToPermissions('download', permissions)
#             self.addToPermissions('order', permissions)
#             self.addToPermissions('tram', permissions)
#         else:
#             if 'M2M_APP' in roles:
#                 self.addToPermissions('application', permissions)
#                 self.addToPermissions('download', permissions)
#                 self.addToPermissions('order', permissions)

#             if 'M2M_DDS' in roles:
#                 self.addToPermissions('application', permissions)
#                 self.addToPermissions('dds', permissions)
#                 self.addToPermissions('download', permissions)

#             if 'MACHINE' in roles:
#                 self.addToPermissions('download', permissions)
#                 self.addToPermissions('order', permissions)
            

#             if 'M2M_TRAM' in roles:
#                 self.addToPermissions('application', permissions)
#                 self.addToPermissions('order', permissions)
#                 self.addToPermissions('tram', permissions)
          

#             if 'BULKMEDIAA' in roles:
#                 self.addToPermissions('application', permissions)
#                 self.addToPermissions('bma', permissions)
#                 self.addToPermissions('download', permissions)
#         return permissions

#     def addToPermissions(self, permission, permissions):
#         if permission not in permissions:
#             permissions.append(permission)

#     def hasAccess(self):    
#         contactId = None

#         #If globally available, just return
#         if self.permission == '*':
#             return True

#         if self.apiKey != None:
#             if self.authService.hasIdentity():
#                 contactId = self.authService.getIdentity().getContactId()

#                 #If only user restricted then we don't need to continue
#                 if self.permission == '@':
#                     return True

#                 permissions = self.getPermissionListForRoles(self.authService.getIdentity().getRoles())
#             else:
#                 #Wildcard access not granted and there isn't a user so access cannot be possible
#                 return False
            
#         else:
#             apiKey = json.loads(base64.decodestring(self.apiKey))
#             contactId = apiKey['cid']
#             permissions = apiKey['p']

#             #If we have an apiKey then we know we have a user
#             if self.permission == '@':
#                 return True            

#         #Developer can access all - so check first
#         if 'developer' in permissions:
#             return True        

#         #Developer can access all - so check first
#         #This could be condensed but leaving long-form for readability
#         if self.permission == 'application' and 'application' in permissions:
#             return True
#         elif self.permission == 'tram' and 'tram' in permissions:
#             return True
#         elif self.permission == 'dds' and 'dds' in permissions:
#             return True
#         elif self.permission == 'download' and 'download' in permissions:
#             return True
#         elif self.permission == 'order' and 'order' in permissions:
#             return True        

#         self.logger.notice("User", contactId, "denied access to " + self.getEndpoint() + " with permission " + self.permission + " - permissions = " + ','.join(permissions))
#         return False    

#     #Default - if a method isn't available yet it may remain null
#     def runStable(self):    
#         return None    
    
#     #Default is to run stable if not defined
#     def runExperimental(self):    
#         return self.runStable()
    
    
#     #Default is to run experiemental if not defined
#     def runDevelopment(self):    
#         return self.runExperimental()
    
#     #Parse the payload and load the appropriate inputParam fields
#     def setInput(self, payload):    
#         for param in self.inputParams:
#             value = None
#             key = param.getKey()
            
#             if key in payload.keys():
#                 value = payload[key]
            
#             #Data filtering, validation and required check is done within setValue
#             param.setValue(value)

#     def setPermission(self, permission):
#         self.permission = permission
    
#     def getPermission(self):    
#         return self.permission
    
#     def getLabel(self):
#         return self.label
    
#     def setLabel(self, label):
#         self.label = label    
    
#     def getEndpoint(self):
#         return self.ENDPOINT
    
#     def getSummary(self):    
#         return self.summary
    
#     def setSummary(self, summary):
#         self.summary = summary
   
#     def getRequestId(self):
#         return self.requestId
    
#     def setRequestId(self, requestId):    
#         self.requestId = requestId
    
#     def getUserContext(self):    
#         return self.userContext
   
#     def setUserContext(self, userContext):   
#         self.userContext = userContext

#     def getApiSessionId(self):    
#         return self.apiSessionId
    
#     def setApiSessionId(self, apiSessionId):    
#         self.apiSessionId = apiSessionId 
        
# # scene-search method
# class Search(Endpoint):
#     ENDPOINT = 'scene-search'

#     permission = '@'
#     label = 'Scene Search'
#     summary = 'Scene Search'
    
#     def runStable(self):    
#         # get user's contactId and ipAddress
#         userContext = self.getUserContext()

#         metadataType = self.getInputParameter('metadataType').getValue()
#         if metadataType not in ['full', 'summary', None]:
#             raise ApiException('INPUT_PARAMETER_INVALID', 'Invalid metadata type used')
#         elif metadataType == 'summary':
#             metadataType = 'res_sum'

#         sceneFilter = self.getInputParameter('sceneFilter').getValue()
#         datasetName = self.getInputParameter('datasetName').getValue()
#         if self.getInputParameter('maxResults').getValue():
#             maxResults = self.getInputParameter('maxResults').getValue()
#         else:            
#             maxResults = 100
        
#         if self.getInputParameter('startingNumber').getValue():
#             startingNumber = self.getInputParameter('startingNumber').getValue()
#         else:            
#             startingNumber = 1

#         sortField = self.getInputParameter('sortField').getValue()
#         if sortField == None:
#             sortField = 'acquisitionDate'
#         elif sortField not in ['acquisitionDate', 'displayId', 'entityId', 'modifiedDate']:
#             raise ApiException('INPUT_PARAMETER_INVALID', 'Invalid sortField used')

#         sortDirection = self.getInputParameter('sortDirection').getValue()
#         if sortDirection != None:
#             sortDirection = 'DESC'
#         elif sortDirection.upper() not in ['ASC', 'DESC']:
#             raise ApiException('INPUT_PARAMETER_INVALID', 'Invalid sortDirection used')

#         if maxResults != None:
#             maxResults = 100

#         if startingNumber != None:
#             startingNumber = 1

#         compareListName = self.getInputParameter('compareListName').getValue()
#         bulkListName = self.getInputParameter('bulkListName').getValue()
#         orderListName = self.getInputParameter('orderListName').getValue()
#         excludeListName = self.getInputParameter('excludeListName').getValue()

#         results = []
#         totalHits = 0

#         try:
#             datasetName = datasetName.lower()
            
#             #DatasetRepository is used to retrieve datasets from the database
#             datasetRepository = DatasetRepository(compareListName, bulkListName, orderListName, excludeListName)
#             dataset = datasetRepository.fetchRecord(datasetName, 'dataset_alias')
#             #DatasetAccessManager is used to check user's restrictions and permissions to access datasets
#             datasetAccessManager = DatasetAccessManager(userContext['user_contact_id'], self.config['internalIps'])
#             allowedRestrictions = datasetAccessManager.getAllowedRestrictions()

#             #Check dataset access
#             datasetAccessManager.isAllowed(datasetName)

#             results = datasetRepository.searchDataset(userContext['user_contact_id'], datasetName, sceneFilter, maxResults, startingNumber, metadataType, allowedRestrictions, sortField, sortDirection, includeNullMetadataValues)
#             totalHits = datasetRepository.searchHits(userContext['user_contact_id'], datasetName, sceneFilter)
#         except Exception as e: 
#             raise ApiException('SEARCH_ERROR', 'Unable to execute search request')        

#         if len(results) == 0:
#             startingNumber = 0
#             nextRecord = 0
#         else:
#             if startingNumber + len(results) < totalHits:
#                 nextRecord = startingNumber + len(results)
#             else:
#                 #We've reached the end of the results
#                 nextRecord = totalHits
            
#         numExcluded = 0
#         try:
#             #SceneListRepository is used to retrieve scene lists from the database
#             sceneListRepository = SceneListRepository()
#             numExcluded = sceneListRepository.getSceneCount(userContext['user_contact_id'], excludeListName, dataset.getDatasetId())
#         except Exception as e:
#             print("Unable to get excluded scene count:" + str(e))

#         return {
#             'numExcluded' : numExcluded,
#             'startingNumber' : startingNumber,
#             'totalHits' : totalHits,
#             'recordsReturned' : len(results),
#             'nextRecord' : nextRecord,
#             'results' : results
#         }
    
#     def runExperimental(self):    
#         return self.runStable()
    
#     def runDevelopment(self):    
#         return self.runExperimental()



