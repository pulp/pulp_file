# ExportersFilesystemApi

All URIs are relative to *http://localhost:24817*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create**](ExportersFilesystemApi.md#create) | **POST** /pulp/api/v3/exporters/file/filesystem/ | 
[**delete**](ExportersFilesystemApi.md#delete) | **DELETE** {file_filesystem_exporter_href} | 
[**list**](ExportersFilesystemApi.md#list) | **GET** /pulp/api/v3/exporters/file/filesystem/ | 
[**partial_update**](ExportersFilesystemApi.md#partial_update) | **PATCH** {file_filesystem_exporter_href} | 
[**read**](ExportersFilesystemApi.md#read) | **GET** {file_filesystem_exporter_href} | 
[**update**](ExportersFilesystemApi.md#update) | **PUT** {file_filesystem_exporter_href} | 


# **create**
> FileFileFilesystemExporterResponse create(file_file_filesystem_exporter)



FilesystemExporters export content from a publication to a path on the file system.  WARNING: This feature is provided as a tech preview and may change in the future. Backwards compatibility is not guaranteed.

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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_file_filesystem_exporter = pulpcore.client.pulp_file.FileFileFilesystemExporter() # FileFileFilesystemExporter | 

    try:
        api_response = api_instance.create(file_file_filesystem_exporter)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->create: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_file_filesystem_exporter = pulpcore.client.pulp_file.FileFileFilesystemExporter() # FileFileFilesystemExporter | 

    try:
        api_response = api_instance.create(file_file_filesystem_exporter)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_file_filesystem_exporter** | [**FileFileFilesystemExporter**](FileFileFilesystemExporter.md)|  | 

### Return type

[**FileFileFilesystemExporterResponse**](FileFileFilesystemExporterResponse.md)

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
> delete(file_filesystem_exporter_href)



FilesystemExporters export content from a publication to a path on the file system.  WARNING: This feature is provided as a tech preview and may change in the future. Backwards compatibility is not guaranteed.

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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_filesystem_exporter_href = 'file_filesystem_exporter_href_example' # str | 

    try:
        api_instance.delete(file_filesystem_exporter_href)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->delete: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_filesystem_exporter_href = 'file_filesystem_exporter_href_example' # str | 

    try:
        api_instance.delete(file_filesystem_exporter_href)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_filesystem_exporter_href** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list**
> InlineResponse2002 list(limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, fields=fields, exclude_fields=exclude_fields)



FilesystemExporters export content from a publication to a path on the file system.  WARNING: This feature is provided as a tech preview and may change in the future. Backwards compatibility is not guaranteed.

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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    limit = 56 # int | Number of results to return per page. (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.list(limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->list: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    limit = 56 # int | Number of results to return per page. (optional)
name = 'name_example' # str | name (optional)
name__in = 'name__in_example' # str | name__in (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.list(limit=limit, name=name, name__in=name__in, offset=offset, ordering=ordering, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Number of results to return per page. | [optional] 
 **name** | **str**| name | [optional] 
 **name__in** | **str**| name__in | [optional] 
 **offset** | **int**| The initial index from which to return the results. | [optional] 
 **ordering** | **str**| Which field to use when ordering the results. | [optional] 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

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
> FileFileFilesystemExporterResponse partial_update(file_filesystem_exporter_href, patchedfile_file_filesystem_exporter)



FilesystemExporters export content from a publication to a path on the file system.  WARNING: This feature is provided as a tech preview and may change in the future. Backwards compatibility is not guaranteed.

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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_filesystem_exporter_href = 'file_filesystem_exporter_href_example' # str | 
patchedfile_file_filesystem_exporter = pulpcore.client.pulp_file.PatchedfileFileFilesystemExporter() # PatchedfileFileFilesystemExporter | 

    try:
        api_response = api_instance.partial_update(file_filesystem_exporter_href, patchedfile_file_filesystem_exporter)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->partial_update: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_filesystem_exporter_href = 'file_filesystem_exporter_href_example' # str | 
patchedfile_file_filesystem_exporter = pulpcore.client.pulp_file.PatchedfileFileFilesystemExporter() # PatchedfileFileFilesystemExporter | 

    try:
        api_response = api_instance.partial_update(file_filesystem_exporter_href, patchedfile_file_filesystem_exporter)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->partial_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_filesystem_exporter_href** | **str**|  | 
 **patchedfile_file_filesystem_exporter** | [**PatchedfileFileFilesystemExporter**](PatchedfileFileFilesystemExporter.md)|  | 

### Return type

[**FileFileFilesystemExporterResponse**](FileFileFilesystemExporterResponse.md)

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

# **read**
> FileFileFilesystemExporterResponse read(file_filesystem_exporter_href, fields=fields, exclude_fields=exclude_fields)



FilesystemExporters export content from a publication to a path on the file system.  WARNING: This feature is provided as a tech preview and may change in the future. Backwards compatibility is not guaranteed.

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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_filesystem_exporter_href = 'file_filesystem_exporter_href_example' # str | 
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.read(file_filesystem_exporter_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->read: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_filesystem_exporter_href = 'file_filesystem_exporter_href_example' # str | 
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

    try:
        api_response = api_instance.read(file_filesystem_exporter_href, fields=fields, exclude_fields=exclude_fields)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_filesystem_exporter_href** | **str**|  | 
 **fields** | **str**| A list of fields to include in the response. | [optional] 
 **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

### Return type

[**FileFileFilesystemExporterResponse**](FileFileFilesystemExporterResponse.md)

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
> FileFileFilesystemExporterResponse update(file_filesystem_exporter_href, file_file_filesystem_exporter)



FilesystemExporters export content from a publication to a path on the file system.  WARNING: This feature is provided as a tech preview and may change in the future. Backwards compatibility is not guaranteed.

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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_filesystem_exporter_href = 'file_filesystem_exporter_href_example' # str | 
file_file_filesystem_exporter = pulpcore.client.pulp_file.FileFileFilesystemExporter() # FileFileFilesystemExporter | 

    try:
        api_response = api_instance.update(file_filesystem_exporter_href, file_file_filesystem_exporter)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->update: %s\n" % e)
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
    api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
    file_filesystem_exporter_href = 'file_filesystem_exporter_href_example' # str | 
file_file_filesystem_exporter = pulpcore.client.pulp_file.FileFileFilesystemExporter() # FileFileFilesystemExporter | 

    try:
        api_response = api_instance.update(file_filesystem_exporter_href, file_file_filesystem_exporter)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExportersFilesystemApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_filesystem_exporter_href** | **str**|  | 
 **file_file_filesystem_exporter** | [**FileFileFilesystemExporter**](FileFileFilesystemExporter.md)|  | 

### Return type

[**FileFileFilesystemExporterResponse**](FileFileFilesystemExporterResponse.md)

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

