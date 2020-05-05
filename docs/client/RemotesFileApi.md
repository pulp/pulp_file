# pulpcore.client.pulp_file.RemotesFileApi

All URIs are relative to *http://localhost:24817*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create**](RemotesFileApi.md#create) | **POST** /pulp/api/v3/remotes/file/file/ | Create a file remote
[**delete**](RemotesFileApi.md#delete) | **DELETE** {file_remote_href} | Delete a file remote
[**list**](RemotesFileApi.md#list) | **GET** /pulp/api/v3/remotes/file/file/ | List file remotes
[**partial_update**](RemotesFileApi.md#partial_update) | **PATCH** {file_remote_href} | Partially update a file remote
[**read**](RemotesFileApi.md#read) | **GET** {file_remote_href} | Inspect a file remote
[**update**](RemotesFileApi.md#update) | **PUT** {file_remote_href} | Update a file remote


# **create**
> FileFileRemote create(data)

Create a file remote

 FileRemote represents an external source of File Content.  The target url of a FileRemote must contain a file manifest, which contains the metadata for all files at the source.

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
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    data = pulpcore.client.pulp_file.FileFileRemote() # FileFileRemote | 

    try:
        # Create a file remote
        api_response = api_instance.create(data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data** | [**FileFileRemote**](FileFileRemote.md)|  | 

### Return type

[**FileFileRemote**](FileFileRemote.md)

### Authorization

[Basic](../client.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

 [[Back to API list]](../client.md#documentation-for-api-endpoints) [[Back to Model list]](../client.md#documentation-for-models) [[Back to client]](../client.md)

# **delete**
> AsyncOperationResponse delete(file_remote_href)

Delete a file remote

Trigger an asynchronous delete task

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
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | URI of File Remote. e.g.: /pulp/api/v3/remotes/file/file/1/

    try:
        # Delete a file remote
        api_response = api_instance.delete(file_remote_href)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_remote_href** | **str**| URI of File Remote. e.g.: /pulp/api/v3/remotes/file/file/1/ | 

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
> InlineResponse2005 list(ordering=ordering, name=name, name__in=name__in, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__range=pulp_last_updated__range, pulp_last_updated=pulp_last_updated, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)

List file remotes

 FileRemote represents an external source of File Content.  The target url of a FileRemote must contain a file manifest, which contains the metadata for all files at the source.

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
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
name = 'name_example' # str |  (optional)
name__in = 'name__in_example' # str | Filter results where name is in a comma-separated list of values (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | Filter results where pulp_last_updated is less than value (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | Filter results where pulp_last_updated is less than or equal to value (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | Filter results where pulp_last_updated is greater than value (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | Filter results where pulp_last_updated is greater than or equal to value (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | Filter results where pulp_last_updated is between two comma separated values (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | ISO 8601 formatted dates are supported (optional)
limit = 56 # int | Number of results to return per page. (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        # List file remotes
        api_response = api_instance.list(ordering=ordering, name=name, name__in=name__in, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__range=pulp_last_updated__range, pulp_last_updated=pulp_last_updated, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **name** | **str**|  | [optional] 
 **name__in** | **str**| Filter results where name is in a comma-separated list of values | [optional] 
 **pulp_last_updated__lt** | **str**| Filter results where pulp_last_updated is less than value | [optional] 
 **pulp_last_updated__lte** | **str**| Filter results where pulp_last_updated is less than or equal to value | [optional] 
 **pulp_last_updated__gt** | **str**| Filter results where pulp_last_updated is greater than value | [optional] 
 **pulp_last_updated__gte** | **str**| Filter results where pulp_last_updated is greater than or equal to value | [optional] 
 **pulp_last_updated__range** | **str**| Filter results where pulp_last_updated is between two comma separated values | [optional] 
 **pulp_last_updated** | **str**| ISO 8601 formatted dates are supported | [optional] 
 **limit** | **int**| Number of results to return per page. | [optional] 
 **offset** | **int**| The initial index from which to return the results. | [optional] 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

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

# **partial_update**
> AsyncOperationResponse partial_update(file_remote_href, data)

Partially update a file remote

Trigger an asynchronous partial update task

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
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | URI of File Remote. e.g.: /pulp/api/v3/remotes/file/file/1/
data = pulpcore.client.pulp_file.FileFileRemote() # FileFileRemote | 

    try:
        # Partially update a file remote
        api_response = api_instance.partial_update(file_remote_href, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->partial_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_remote_href** | **str**| URI of File Remote. e.g.: /pulp/api/v3/remotes/file/file/1/ | 
 **data** | [**FileFileRemote**](FileFileRemote.md)|  | 

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

# **read**
> FileFileRemote read(file_remote_href, fields=fields, exclude_fields=exclude_fields)

Inspect a file remote

 FileRemote represents an external source of File Content.  The target url of a FileRemote must contain a file manifest, which contains the metadata for all files at the source.

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
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | URI of File Remote. e.g.: /pulp/api/v3/remotes/file/file/1/
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        # Inspect a file remote
        api_response = api_instance.read(file_remote_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_remote_href** | **str**| URI of File Remote. e.g.: /pulp/api/v3/remotes/file/file/1/ | 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**FileFileRemote**](FileFileRemote.md)

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

# **update**
> AsyncOperationResponse update(file_remote_href, data)

Update a file remote

Trigger an asynchronous update task

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
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | URI of File Remote. e.g.: /pulp/api/v3/remotes/file/file/1/
data = pulpcore.client.pulp_file.FileFileRemote() # FileFileRemote | 

    try:
        # Update a file remote
        api_response = api_instance.update(file_remote_href, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_remote_href** | **str**| URI of File Remote. e.g.: /pulp/api/v3/remotes/file/file/1/ | 
 **data** | [**FileFileRemote**](FileFileRemote.md)|  | 

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

