# DistributionsFileApi

All URIs are relative to *http://localhost:24817*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create**](DistributionsFileApi.md#create) | **POST** /pulp/api/v3/distributions/file/file/ | 
[**delete**](DistributionsFileApi.md#delete) | **DELETE** {file_distribution_href} | 
[**list**](DistributionsFileApi.md#list) | **GET** /pulp/api/v3/distributions/file/file/ | 
[**partial_update**](DistributionsFileApi.md#partial_update) | **PATCH** {file_distribution_href} | 
[**read**](DistributionsFileApi.md#read) | **GET** {file_distribution_href} | 
[**update**](DistributionsFileApi.md#update) | **PUT** {file_distribution_href} | 


# **create**
> AsyncOperationResponse create(file_file_distribution)



Trigger an asynchronous create task

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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_file_distribution = pulpcore.client.pulp_file.FileFileDistribution() # FileFileDistribution | 

    try:
        api_response = api_instance.create(file_file_distribution)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->create: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_file_distribution = pulpcore.client.pulp_file.FileFileDistribution() # FileFileDistribution | 

    try:
        api_response = api_instance.create(file_file_distribution)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_file_distribution** | [**FileFileDistribution**](FileFileDistribution.md)|  | 

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

# **delete**
> AsyncOperationResponse delete(file_distribution_href, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)



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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_distribution_href = 'file_distribution_href_example' # str | 
base_path = 'base_path_example' # str | base_path (optional)
base_path__contains = 'base_path__contains_example' # str | base_path__contains (optional)
base_path__icontains = 'base_path__icontains_example' # str | base_path__icontains (optional)
base_path__in = 'base_path__in_example' # str | base_path__in (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

    try:
        api_response = api_instance.delete(file_distribution_href, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->delete: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_distribution_href = 'file_distribution_href_example' # str | 
base_path = 'base_path_example' # str | base_path (optional)
base_path__contains = 'base_path__contains_example' # str | base_path__contains (optional)
base_path__icontains = 'base_path__icontains_example' # str | base_path__icontains (optional)
base_path__in = 'base_path__in_example' # str | base_path__in (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

    try:
        api_response = api_instance.delete(file_distribution_href, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_distribution_href** | **str**|  | 
 **base_path** | **str**| base_path | [optional] 
 **base_path__contains** | **str**| base_path__contains | [optional] 
 **base_path__icontains** | **str**| base_path__icontains | [optional] 
 **base_path__in** | **str**| base_path__in | [optional] 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 

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
> InlineResponse2001 list(base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, fields=fields, exclude_fields=exclude_fields)



<!-- User-facing documentation, rendered as html--> FileDistributions host <a href=\"#operation/publications_file_file_list\">File Publications</a> which makes the metadata and the referenced <a href=\"#operation/content_file_files_list\">File Content</a> available to HTTP clients. Additionally, a FileDistribution with an associated FilePublication can be the target url of a <a href=\"#operation/remotes_file_file_list\">File Remote</a> , allowing another instance of Pulp to sync the content.

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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    base_path = 'base_path_example' # str | base_path (optional)
base_path__contains = 'base_path__contains_example' # str | base_path__contains (optional)
base_path__icontains = 'base_path__icontains_example' # str | base_path__icontains (optional)
base_path__in = 'base_path__in_example' # str | base_path__in (optional)
limit = 56 # int | Number of results to return per page. (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.list(base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->list: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    base_path = 'base_path_example' # str | base_path (optional)
base_path__contains = 'base_path__contains_example' # str | base_path__contains (optional)
base_path__icontains = 'base_path__icontains_example' # str | base_path__icontains (optional)
base_path__in = 'base_path__in_example' # str | base_path__in (optional)
limit = 56 # int | Number of results to return per page. (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.list(base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **base_path** | **str**| base_path | [optional] 
 **base_path__contains** | **str**| base_path__contains | [optional] 
 **base_path__icontains** | **str**| base_path__icontains | [optional] 
 **base_path__in** | **str**| base_path__in | [optional] 
 **limit** | **int**| Number of results to return per page. | [optional] 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **offset** | **int**| The initial index from which to return the results. | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

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
> AsyncOperationResponse partial_update(file_distribution_href, patchedfile_file_distribution, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)



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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_distribution_href = 'file_distribution_href_example' # str | 
patchedfile_file_distribution = pulpcore.client.pulp_file.PatchedfileFileDistribution() # PatchedfileFileDistribution | 
base_path = 'base_path_example' # str | base_path (optional)
base_path__contains = 'base_path__contains_example' # str | base_path__contains (optional)
base_path__icontains = 'base_path__icontains_example' # str | base_path__icontains (optional)
base_path__in = 'base_path__in_example' # str | base_path__in (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

    try:
        api_response = api_instance.partial_update(file_distribution_href, patchedfile_file_distribution, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->partial_update: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_distribution_href = 'file_distribution_href_example' # str | 
patchedfile_file_distribution = pulpcore.client.pulp_file.PatchedfileFileDistribution() # PatchedfileFileDistribution | 
base_path = 'base_path_example' # str | base_path (optional)
base_path__contains = 'base_path__contains_example' # str | base_path__contains (optional)
base_path__icontains = 'base_path__icontains_example' # str | base_path__icontains (optional)
base_path__in = 'base_path__in_example' # str | base_path__in (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

    try:
        api_response = api_instance.partial_update(file_distribution_href, patchedfile_file_distribution, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->partial_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_distribution_href** | **str**|  | 
 **patchedfile_file_distribution** | [**PatchedfileFileDistribution**](PatchedfileFileDistribution.md)|  | 
 **base_path** | **str**| base_path | [optional] 
 **base_path__contains** | **str**| base_path__contains | [optional] 
 **base_path__icontains** | **str**| base_path__icontains | [optional] 
 **base_path__in** | **str**| base_path__in | [optional] 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 

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
> FileFileDistributionResponse read(file_distribution_href, fields=fields, exclude_fields=exclude_fields)



<!-- User-facing documentation, rendered as html--> FileDistributions host <a href=\"#operation/publications_file_file_list\">File Publications</a> which makes the metadata and the referenced <a href=\"#operation/content_file_files_list\">File Content</a> available to HTTP clients. Additionally, a FileDistribution with an associated FilePublication can be the target url of a <a href=\"#operation/remotes_file_file_list\">File Remote</a> , allowing another instance of Pulp to sync the content.

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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_distribution_href = 'file_distribution_href_example' # str | 
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.read(file_distribution_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->read: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_distribution_href = 'file_distribution_href_example' # str | 
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.read(file_distribution_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_distribution_href** | **str**|  | 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**FileFileDistributionResponse**](FileFileDistributionResponse.md)

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
> AsyncOperationResponse update(file_distribution_href, file_file_distribution, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)



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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_distribution_href = 'file_distribution_href_example' # str | 
file_file_distribution = pulpcore.client.pulp_file.FileFileDistribution() # FileFileDistribution | 
base_path = 'base_path_example' # str | base_path (optional)
base_path__contains = 'base_path__contains_example' # str | base_path__contains (optional)
base_path__icontains = 'base_path__icontains_example' # str | base_path__icontains (optional)
base_path__in = 'base_path__in_example' # str | base_path__in (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

    try:
        api_response = api_instance.update(file_distribution_href, file_file_distribution, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->update: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
    file_distribution_href = 'file_distribution_href_example' # str | 
file_file_distribution = pulpcore.client.pulp_file.FileFileDistribution() # FileFileDistribution | 
base_path = 'base_path_example' # str | base_path (optional)
base_path__contains = 'base_path__contains_example' # str | base_path__contains (optional)
base_path__icontains = 'base_path__icontains_example' # str | base_path__icontains (optional)
base_path__in = 'base_path__in_example' # str | base_path__in (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

    try:
        api_response = api_instance.update(file_distribution_href, file_file_distribution, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, name=name, name__in=name__in, ordering=ordering)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DistributionsFileApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_distribution_href** | **str**|  | 
 **file_file_distribution** | [**FileFileDistribution**](FileFileDistribution.md)|  | 
 **base_path** | **str**| base_path | [optional] 
 **base_path__contains** | **str**| base_path__contains | [optional] 
 **base_path__icontains** | **str**| base_path__icontains | [optional] 
 **base_path__in** | **str**| base_path__in | [optional] 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 

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

