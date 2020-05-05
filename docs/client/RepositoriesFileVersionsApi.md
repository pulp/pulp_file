# pulpcore.client.pulp_file.RepositoriesFileVersionsApi

All URIs are relative to *http://localhost:24817*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete**](RepositoriesFileVersionsApi.md#delete) | **DELETE** {file_repository_version_href} | Delete a repository version
[**list**](RepositoriesFileVersionsApi.md#list) | **GET** {file_repository_href}versions/ | List repository versions
[**read**](RepositoriesFileVersionsApi.md#read) | **GET** {file_repository_version_href} | Inspect a repository version
[**repair**](RepositoriesFileVersionsApi.md#repair) | **POST** {file_repository_version_href}repair/ | 


# **delete**
> AsyncOperationResponse delete(file_repository_version_href)

Delete a repository version

Trigger an asynchronous task to delete a repositroy version.

### Example

* Basic Authentication (Basic):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
configuration = pulpcore.client.pulp_file.Configuration()
# Configure HTTP basic authorization: Basic
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost:24817
configuration.host = "http://localhost:24817"
# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | URI of Repository Version. e.g.: /pulp/api/v3/repositories/file/file/1/versions/1/

    try:
        # Delete a repository version
        api_response = api_instance.delete(file_repository_version_href)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_repository_version_href** | **str**| URI of Repository Version. e.g.: /pulp/api/v3/repositories/file/file/1/versions/1/ | 

### Return type

[**AsyncOperationResponse**](AsyncOperationResponse.md)

### Authorization

[Basic](../client.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** |  |  -  |

 [[Back to API list]](../client.md#documentation-for-api-endpoints) [[Back to Model list]](../client.md#documentation-for-models) [[Back to client]](../client.md)

# **list**
> InlineResponse2007 list(file_repository_href, ordering=ordering, number=number, number__lt=number__lt, number__lte=number__lte, number__gt=number__gt, number__gte=number__gte, number__range=number__range, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__range=pulp_created__range, content=content, pulp_created=pulp_created, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)

List repository versions

 FileRepositoryVersion represents a single file repository version.

### Example

* Basic Authentication (Basic):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
configuration = pulpcore.client.pulp_file.Configuration()
# Configure HTTP basic authorization: Basic
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost:24817
configuration.host = "http://localhost:24817"
# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_href = 'file_repository_href_example' # str | URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
number = 3.4 # float |  (optional)
number__lt = 3.4 # float | Filter results where number is less than value (optional)
number__lte = 3.4 # float | Filter results where number is less than or equal to value (optional)
number__gt = 3.4 # float | Filter results where number is greater than value (optional)
number__gte = 3.4 # float | Filter results where number is greater than or equal to value (optional)
number__range = 3.4 # float | Filter results where number is between two comma separated values (optional)
pulp_created__lt = 'pulp_created__lt_example' # str | Filter results where pulp_created is less than value (optional)
pulp_created__lte = 'pulp_created__lte_example' # str | Filter results where pulp_created is less than or equal to value (optional)
pulp_created__gt = 'pulp_created__gt_example' # str | Filter results where pulp_created is greater than value (optional)
pulp_created__gte = 'pulp_created__gte_example' # str | Filter results where pulp_created is greater than or equal to value (optional)
pulp_created__range = 'pulp_created__range_example' # str | Filter results where pulp_created is between two comma separated values (optional)
content = 'content_example' # str | Content Unit referenced by HREF (optional)
pulp_created = 'pulp_created_example' # str | ISO 8601 formatted dates are supported (optional)
limit = 56 # int | Number of results to return per page. (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        # List repository versions
        api_response = api_instance.list(file_repository_href, ordering=ordering, number=number, number__lt=number__lt, number__lte=number__lte, number__gt=number__gt, number__gte=number__gte, number__range=number__range, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__range=pulp_created__range, content=content, pulp_created=pulp_created, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_repository_href** | **str**| URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/ | 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **number** | **float**|  | [optional] 
 **number__lt** | **float**| Filter results where number is less than value | [optional] 
 **number__lte** | **float**| Filter results where number is less than or equal to value | [optional] 
 **number__gt** | **float**| Filter results where number is greater than value | [optional] 
 **number__gte** | **float**| Filter results where number is greater than or equal to value | [optional] 
 **number__range** | **float**| Filter results where number is between two comma separated values | [optional] 
 **pulp_created__lt** | **str**| Filter results where pulp_created is less than value | [optional] 
 **pulp_created__lte** | **str**| Filter results where pulp_created is less than or equal to value | [optional] 
 **pulp_created__gt** | **str**| Filter results where pulp_created is greater than value | [optional] 
 **pulp_created__gte** | **str**| Filter results where pulp_created is greater than or equal to value | [optional] 
 **pulp_created__range** | **str**| Filter results where pulp_created is between two comma separated values | [optional] 
 **content** | **str**| Content Unit referenced by HREF | [optional] 
 **pulp_created** | **str**| ISO 8601 formatted dates are supported | [optional] 
 **limit** | **int**| Number of results to return per page. | [optional] 
 **offset** | **int**| The initial index from which to return the results. | [optional] 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**InlineResponse2007**](InlineResponse2007.md)

### Authorization

[Basic](../client.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

 [[Back to API list]](../client.md#documentation-for-api-endpoints) [[Back to Model list]](../client.md#documentation-for-models) [[Back to client]](../client.md)

# **read**
> RepositoryVersion read(file_repository_version_href, fields=fields, exclude_fields=exclude_fields)

Inspect a repository version

 FileRepositoryVersion represents a single file repository version.

### Example

* Basic Authentication (Basic):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
configuration = pulpcore.client.pulp_file.Configuration()
# Configure HTTP basic authorization: Basic
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost:24817
configuration.host = "http://localhost:24817"
# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | URI of Repository Version. e.g.: /pulp/api/v3/repositories/file/file/1/versions/1/
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        # Inspect a repository version
        api_response = api_instance.read(file_repository_version_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_repository_version_href** | **str**| URI of Repository Version. e.g.: /pulp/api/v3/repositories/file/file/1/versions/1/ | 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**RepositoryVersion**](RepositoryVersion.md)

### Authorization

[Basic](../client.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

 [[Back to API list]](../client.md#documentation-for-api-endpoints) [[Back to Model list]](../client.md#documentation-for-models) [[Back to client]](../client.md)

# **repair**
> AsyncOperationResponse repair(file_repository_version_href, data)



Trigger an asynchronous task to repair a repositroy version.

### Example

* Basic Authentication (Basic):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
configuration = pulpcore.client.pulp_file.Configuration()
# Configure HTTP basic authorization: Basic
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost:24817
configuration.host = "http://localhost:24817"
# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | URI of Repository Version. e.g.: /pulp/api/v3/repositories/file/file/1/versions/1/
data = pulpcore.client.pulp_file.RepositoryVersion() # RepositoryVersion | 

    try:
        api_response = api_instance.repair(file_repository_version_href, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->repair: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_repository_version_href** | **str**| URI of Repository Version. e.g.: /pulp/api/v3/repositories/file/file/1/versions/1/ | 
 **data** | [**RepositoryVersion**](RepositoryVersion.md)|  | 

### Return type

[**AsyncOperationResponse**](AsyncOperationResponse.md)

### Authorization

[Basic](../client.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** |  |  -  |

 [[Back to API list]](../client.md#documentation-for-api-endpoints) [[Back to Model list]](../client.md#documentation-for-models) [[Back to client]](../client.md)

