# RemotesFileApi

All URIs are relative to *http://localhost:24817*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create**](RemotesFileApi.md#create) | **POST** /pulp/api/v3/remotes/file/file/ | 
[**delete**](RemotesFileApi.md#delete) | **DELETE** {file_remote_href} | 
[**list**](RemotesFileApi.md#list) | **GET** /pulp/api/v3/remotes/file/file/ | 
[**partial_update**](RemotesFileApi.md#partial_update) | **PATCH** {file_remote_href} | 
[**read**](RemotesFileApi.md#read) | **GET** {file_remote_href} | 
[**update**](RemotesFileApi.md#update) | **PUT** {file_remote_href} | 


# **create**
> FileFileRemoteResponse create(file_file_remote)



<!-- User-facing documentation, rendered as html--> FileRemote represents an external source of <a href=\"#operation/content_file_files_list\">File Content</a>.  The target url of a FileRemote must contain a file manifest, which contains the metadata for all files at the source.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_file_remote = pulpcore.client.pulp_file.FileFileRemote() # FileFileRemote | 

    try:
        api_response = api_instance.create(file_file_remote)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->create: %s\n" % e)
```

* Api Key Authentication (cookieAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_file_remote = pulpcore.client.pulp_file.FileFileRemote() # FileFileRemote | 

    try:
        api_response = api_instance.create(file_file_remote)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_file_remote** | [**FileFileRemote**](FileFileRemote.md)|  | 

### Return type

[**FileFileRemoteResponse**](FileFileRemoteResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete**
> AsyncOperationResponse delete(file_remote_href, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)



Trigger an asynchronous delete task

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | 
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | pulp_last_updated (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | pulp_last_updated__gt (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | pulp_last_updated__gte (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | pulp_last_updated__lt (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | pulp_last_updated__lte (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | pulp_last_updated__range (optional)

    try:
        api_response = api_instance.delete(file_remote_href, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->delete: %s\n" % e)
```

* Api Key Authentication (cookieAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | 
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | pulp_last_updated (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | pulp_last_updated__gt (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | pulp_last_updated__gte (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | pulp_last_updated__lt (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | pulp_last_updated__lte (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | pulp_last_updated__range (optional)

    try:
        api_response = api_instance.delete(file_remote_href, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_remote_href** | **str**|  | 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **pulp_last_updated** | **str**| pulp_last_updated | [optional] 
 **pulp_last_updated__gt** | **str**| pulp_last_updated__gt | [optional] 
 **pulp_last_updated__gte** | **str**| pulp_last_updated__gte | [optional] 
 **pulp_last_updated__lt** | **str**| pulp_last_updated__lt | [optional] 
 **pulp_last_updated__lte** | **str**| pulp_last_updated__lte | [optional] 
 **pulp_last_updated__range** | **str**| pulp_last_updated__range | [optional] 

### Return type

[**AsyncOperationResponse**](AsyncOperationResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list**
> InlineResponse2005 list(limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range, fields=fields, exclude_fields=exclude_fields)



<!-- User-facing documentation, rendered as html--> FileRemote represents an external source of <a href=\"#operation/content_file_files_list\">File Content</a>.  The target url of a FileRemote must contain a file manifest, which contains the metadata for all files at the source.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    limit = 56 # int | Number of results to return per page. (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | pulp_last_updated (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | pulp_last_updated__gt (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | pulp_last_updated__gte (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | pulp_last_updated__lt (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | pulp_last_updated__lte (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | pulp_last_updated__range (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.list(limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->list: %s\n" % e)
```

* Api Key Authentication (cookieAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    limit = 56 # int | Number of results to return per page. (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | pulp_last_updated (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | pulp_last_updated__gt (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | pulp_last_updated__gte (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | pulp_last_updated__lt (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | pulp_last_updated__lte (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | pulp_last_updated__range (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.list(limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Number of results to return per page. | [optional] 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **offset** | **int**| The initial index from which to return the results. | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **pulp_last_updated** | **str**| pulp_last_updated | [optional] 
 **pulp_last_updated__gt** | **str**| pulp_last_updated__gt | [optional] 
 **pulp_last_updated__gte** | **str**| pulp_last_updated__gte | [optional] 
 **pulp_last_updated__lt** | **str**| pulp_last_updated__lt | [optional] 
 **pulp_last_updated__lte** | **str**| pulp_last_updated__lte | [optional] 
 **pulp_last_updated__range** | **str**| pulp_last_updated__range | [optional] 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **partial_update**
> AsyncOperationResponse partial_update(file_remote_href, patchedfile_file_remote, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)



Trigger an asynchronous partial update task

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | 
patchedfile_file_remote = pulpcore.client.pulp_file.PatchedfileFileRemote() # PatchedfileFileRemote | 
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | pulp_last_updated (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | pulp_last_updated__gt (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | pulp_last_updated__gte (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | pulp_last_updated__lt (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | pulp_last_updated__lte (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | pulp_last_updated__range (optional)

    try:
        api_response = api_instance.partial_update(file_remote_href, patchedfile_file_remote, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->partial_update: %s\n" % e)
```

* Api Key Authentication (cookieAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | 
patchedfile_file_remote = pulpcore.client.pulp_file.PatchedfileFileRemote() # PatchedfileFileRemote | 
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | pulp_last_updated (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | pulp_last_updated__gt (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | pulp_last_updated__gte (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | pulp_last_updated__lt (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | pulp_last_updated__lte (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | pulp_last_updated__range (optional)

    try:
        api_response = api_instance.partial_update(file_remote_href, patchedfile_file_remote, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->partial_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_remote_href** | **str**|  | 
 **patchedfile_file_remote** | [**PatchedfileFileRemote**](PatchedfileFileRemote.md)|  | 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **pulp_last_updated** | **str**| pulp_last_updated | [optional] 
 **pulp_last_updated__gt** | **str**| pulp_last_updated__gt | [optional] 
 **pulp_last_updated__gte** | **str**| pulp_last_updated__gte | [optional] 
 **pulp_last_updated__lt** | **str**| pulp_last_updated__lt | [optional] 
 **pulp_last_updated__lte** | **str**| pulp_last_updated__lte | [optional] 
 **pulp_last_updated__range** | **str**| pulp_last_updated__range | [optional] 

### Return type

[**AsyncOperationResponse**](AsyncOperationResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> FileFileRemoteResponse read(file_remote_href, fields=fields, exclude_fields=exclude_fields)



<!-- User-facing documentation, rendered as html--> FileRemote represents an external source of <a href=\"#operation/content_file_files_list\">File Content</a>.  The target url of a FileRemote must contain a file manifest, which contains the metadata for all files at the source.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | 
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.read(file_remote_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->read: %s\n" % e)
```

* Api Key Authentication (cookieAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | 
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.read(file_remote_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_remote_href** | **str**|  | 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**FileFileRemoteResponse**](FileFileRemoteResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> AsyncOperationResponse update(file_remote_href, file_file_remote, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)



Trigger an asynchronous update task

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | 
file_file_remote = pulpcore.client.pulp_file.FileFileRemote() # FileFileRemote | 
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | pulp_last_updated (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | pulp_last_updated__gt (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | pulp_last_updated__gte (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | pulp_last_updated__lt (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | pulp_last_updated__lte (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | pulp_last_updated__range (optional)

    try:
        api_response = api_instance.update(file_remote_href, file_file_remote, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->update: %s\n" % e)
```

* Api Key Authentication (cookieAuth):
```python
from __future__ import print_function
import time
import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:24817
# See configuration.py for a list of all supported configuration parameters.
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = pulpcore.client.pulp_file.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure API key authorization: cookieAuth
configuration = pulpcore.client.pulp_file.Configuration(
    host = "http://localhost:24817",
    api_key = {
        'Session': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Session'] = 'Bearer'

# Enter a context with an instance of the API client
with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulpcore.client.pulp_file.RemotesFileApi(api_client)
    file_remote_href = 'file_remote_href_example' # str | 
file_file_remote = pulpcore.client.pulp_file.FileFileRemote() # FileFileRemote | 
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_last_updated = 'pulp_last_updated_example' # str | pulp_last_updated (optional)
pulp_last_updated__gt = 'pulp_last_updated__gt_example' # str | pulp_last_updated__gt (optional)
pulp_last_updated__gte = 'pulp_last_updated__gte_example' # str | pulp_last_updated__gte (optional)
pulp_last_updated__lt = 'pulp_last_updated__lt_example' # str | pulp_last_updated__lt (optional)
pulp_last_updated__lte = 'pulp_last_updated__lte_example' # str | pulp_last_updated__lte (optional)
pulp_last_updated__range = 'pulp_last_updated__range_example' # str | pulp_last_updated__range (optional)

    try:
        api_response = api_instance.update(file_remote_href, file_file_remote, name=name, name__in=name__in, ordering=ordering, pulp_last_updated=pulp_last_updated, pulp_last_updated__gt=pulp_last_updated__gt, pulp_last_updated__gte=pulp_last_updated__gte, pulp_last_updated__lt=pulp_last_updated__lt, pulp_last_updated__lte=pulp_last_updated__lte, pulp_last_updated__range=pulp_last_updated__range)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RemotesFileApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_remote_href** | **str**|  | 
 **file_file_remote** | [**FileFileRemote**](FileFileRemote.md)|  | 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **pulp_last_updated** | **str**| pulp_last_updated | [optional] 
 **pulp_last_updated__gt** | **str**| pulp_last_updated__gt | [optional] 
 **pulp_last_updated__gte** | **str**| pulp_last_updated__gte | [optional] 
 **pulp_last_updated__lt** | **str**| pulp_last_updated__lt | [optional] 
 **pulp_last_updated__lte** | **str**| pulp_last_updated__lte | [optional] 
 **pulp_last_updated__range** | **str**| pulp_last_updated__range | [optional] 

### Return type

[**AsyncOperationResponse**](AsyncOperationResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

