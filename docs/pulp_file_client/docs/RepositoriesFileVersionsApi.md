# RepositoriesFileVersionsApi

All URIs are relative to *http://localhost:24817*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete**](RepositoriesFileVersionsApi.md#delete) | **DELETE** {file_repository_version_href} | 
[**list**](RepositoriesFileVersionsApi.md#list) | **GET** {file_repository_version_href}versions/ | 
[**read**](RepositoriesFileVersionsApi.md#read) | **GET** {file_repository_version_href} | 
[**repair**](RepositoriesFileVersionsApi.md#repair) | **POST** {file_repository_version_href}repair/ | 


# **delete**
> AsyncOperationResponse delete(file_repository_version_href, content=content, content__in=content__in, number=number, number__gt=number__gt, number__gte=number__gte, number__lt=number__lt, number__lte=number__lte, number__range=number__range, ordering=ordering, pulp_created=pulp_created, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__range=pulp_created__range)



Trigger an asynchronous task to delete a repositroy version.

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
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | 
content = 'content_example' # str | content (optional)
content__in = 'content__in_example' # str | content__in (optional)
number = 'number_example' # str | number (optional)
number__gt = 'number__gt_example' # str | number__gt (optional)
number__gte = 'number__gte_example' # str | number__gte (optional)
number__lt = 'number__lt_example' # str | number__lt (optional)
number__lte = 'number__lte_example' # str | number__lte (optional)
number__range = 'number__range_example' # str | number__range (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_created = 'pulp_created_example' # str | pulp_created (optional)
pulp_created__gt = 'pulp_created__gt_example' # str | pulp_created__gt (optional)
pulp_created__gte = 'pulp_created__gte_example' # str | pulp_created__gte (optional)
pulp_created__lt = 'pulp_created__lt_example' # str | pulp_created__lt (optional)
pulp_created__lte = 'pulp_created__lte_example' # str | pulp_created__lte (optional)
pulp_created__range = 'pulp_created__range_example' # str | pulp_created__range (optional)

    try:
        api_response = api_instance.delete(file_repository_version_href, content=content, content__in=content__in, number=number, number__gt=number__gt, number__gte=number__gte, number__lt=number__lt, number__lte=number__lte, number__range=number__range, ordering=ordering, pulp_created=pulp_created, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__range=pulp_created__range)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->delete: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | 
content = 'content_example' # str | content (optional)
content__in = 'content__in_example' # str | content__in (optional)
number = 'number_example' # str | number (optional)
number__gt = 'number__gt_example' # str | number__gt (optional)
number__gte = 'number__gte_example' # str | number__gte (optional)
number__lt = 'number__lt_example' # str | number__lt (optional)
number__lte = 'number__lte_example' # str | number__lte (optional)
number__range = 'number__range_example' # str | number__range (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_created = 'pulp_created_example' # str | pulp_created (optional)
pulp_created__gt = 'pulp_created__gt_example' # str | pulp_created__gt (optional)
pulp_created__gte = 'pulp_created__gte_example' # str | pulp_created__gte (optional)
pulp_created__lt = 'pulp_created__lt_example' # str | pulp_created__lt (optional)
pulp_created__lte = 'pulp_created__lte_example' # str | pulp_created__lte (optional)
pulp_created__range = 'pulp_created__range_example' # str | pulp_created__range (optional)

    try:
        api_response = api_instance.delete(file_repository_version_href, content=content, content__in=content__in, number=number, number__gt=number__gt, number__gte=number__gte, number__lt=number__lt, number__lte=number__lte, number__range=number__range, ordering=ordering, pulp_created=pulp_created, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__range=pulp_created__range)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_repository_version_href** | **str**|  | 
 **content** | **str**| content | [optional] 
 **content__in** | **str**| content__in | [optional] 
 **number** | **str**| number | [optional] 
 **number__gt** | **str**| number__gt | [optional] 
 **number__gte** | **str**| number__gte | [optional] 
 **number__lt** | **str**| number__lt | [optional] 
 **number__lte** | **str**| number__lte | [optional] 
 **number__range** | **str**| number__range | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **pulp_created** | **str**| pulp_created | [optional] 
 **pulp_created__gt** | **str**| pulp_created__gt | [optional] 
 **pulp_created__gte** | **str**| pulp_created__gte | [optional] 
 **pulp_created__lt** | **str**| pulp_created__lt | [optional] 
 **pulp_created__lte** | **str**| pulp_created__lte | [optional] 
 **pulp_created__range** | **str**| pulp_created__range | [optional] 

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
> InlineResponse2007 list(file_repository_version_href, content=content, content__in=content__in, limit=limit, number=number, number__gt=number__gt, number__gte=number__gte, number__lt=number__lt, number__lte=number__lte, number__range=number__range, offset=offset, ordering=ordering, pulp_created=pulp_created, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__range=pulp_created__range, fields=fields, exclude_fields=exclude_fields)



<!-- User-facing documentation, rendered as html--> FileRepositoryVersion represents a single file repository version.

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
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | 
content = 'content_example' # str | content (optional)
content__in = 'content__in_example' # str | content__in (optional)
limit = 56 # int | Number of results to return per page. (optional)
number = 'number_example' # str | number (optional)
number__gt = 'number__gt_example' # str | number__gt (optional)
number__gte = 'number__gte_example' # str | number__gte (optional)
number__lt = 'number__lt_example' # str | number__lt (optional)
number__lte = 'number__lte_example' # str | number__lte (optional)
number__range = 'number__range_example' # str | number__range (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_created = 'pulp_created_example' # str | pulp_created (optional)
pulp_created__gt = 'pulp_created__gt_example' # str | pulp_created__gt (optional)
pulp_created__gte = 'pulp_created__gte_example' # str | pulp_created__gte (optional)
pulp_created__lt = 'pulp_created__lt_example' # str | pulp_created__lt (optional)
pulp_created__lte = 'pulp_created__lte_example' # str | pulp_created__lte (optional)
pulp_created__range = 'pulp_created__range_example' # str | pulp_created__range (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.list(file_repository_version_href, content=content, content__in=content__in, limit=limit, number=number, number__gt=number__gt, number__gte=number__gte, number__lt=number__lt, number__lte=number__lte, number__range=number__range, offset=offset, ordering=ordering, pulp_created=pulp_created, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__range=pulp_created__range, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->list: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | 
content = 'content_example' # str | content (optional)
content__in = 'content__in_example' # str | content__in (optional)
limit = 56 # int | Number of results to return per page. (optional)
number = 'number_example' # str | number (optional)
number__gt = 'number__gt_example' # str | number__gt (optional)
number__gte = 'number__gte_example' # str | number__gte (optional)
number__lt = 'number__lt_example' # str | number__lt (optional)
number__lte = 'number__lte_example' # str | number__lte (optional)
number__range = 'number__range_example' # str | number__range (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
pulp_created = 'pulp_created_example' # str | pulp_created (optional)
pulp_created__gt = 'pulp_created__gt_example' # str | pulp_created__gt (optional)
pulp_created__gte = 'pulp_created__gte_example' # str | pulp_created__gte (optional)
pulp_created__lt = 'pulp_created__lt_example' # str | pulp_created__lt (optional)
pulp_created__lte = 'pulp_created__lte_example' # str | pulp_created__lte (optional)
pulp_created__range = 'pulp_created__range_example' # str | pulp_created__range (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.list(file_repository_version_href, content=content, content__in=content__in, limit=limit, number=number, number__gt=number__gt, number__gte=number__gte, number__lt=number__lt, number__lte=number__lte, number__range=number__range, offset=offset, ordering=ordering, pulp_created=pulp_created, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__range=pulp_created__range, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_repository_version_href** | **str**|  | 
 **content** | **str**| content | [optional] 
 **content__in** | **str**| content__in | [optional] 
 **limit** | **int**| Number of results to return per page. | [optional] 
 **number** | **str**| number | [optional] 
 **number__gt** | **str**| number__gt | [optional] 
 **number__gte** | **str**| number__gte | [optional] 
 **number__lt** | **str**| number__lt | [optional] 
 **number__lte** | **str**| number__lte | [optional] 
 **number__range** | **str**| number__range | [optional] 
 **offset** | **int**| The initial index from which to return the results. | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **pulp_created** | **str**| pulp_created | [optional] 
 **pulp_created__gt** | **str**| pulp_created__gt | [optional] 
 **pulp_created__gte** | **str**| pulp_created__gte | [optional] 
 **pulp_created__lt** | **str**| pulp_created__lt | [optional] 
 **pulp_created__lte** | **str**| pulp_created__lte | [optional] 
 **pulp_created__range** | **str**| pulp_created__range | [optional] 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**InlineResponse2007**](InlineResponse2007.md)

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

# **read**
> RepositoryVersionResponse read(file_repository_version_href, fields=fields, exclude_fields=exclude_fields)



<!-- User-facing documentation, rendered as html--> FileRepositoryVersion represents a single file repository version.

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
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | 
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.read(file_repository_version_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->read: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | 
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.read(file_repository_version_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_repository_version_href** | **str**|  | 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**RepositoryVersionResponse**](RepositoryVersionResponse.md)

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

# **repair**
> AsyncOperationResponse repair(file_repository_version_href, repository_version)



Trigger an asynchronous task to repair a repositroy version.

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
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | 
repository_version = pulpcore.client.pulp_file.RepositoryVersion() # RepositoryVersion | 

    try:
        api_response = api_instance.repair(file_repository_version_href, repository_version)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->repair: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.RepositoriesFileVersionsApi(api_client)
    file_repository_version_href = 'file_repository_version_href_example' # str | 
repository_version = pulpcore.client.pulp_file.RepositoryVersion() # RepositoryVersion | 

    try:
        api_response = api_instance.repair(file_repository_version_href, repository_version)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepositoriesFileVersionsApi->repair: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_repository_version_href** | **str**|  | 
 **repository_version** | [**RepositoryVersion**](RepositoryVersion.md)|  | 

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

