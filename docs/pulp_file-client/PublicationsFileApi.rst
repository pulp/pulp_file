
pulpcore.client.pulp_file.PublicationsFileApi
=============================================

All URIs are relative to *http://localhost:24817*

.. list-table::
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `\ **create** <PublicationsFileApi.md#create>`_
     - **POST** /pulp/api/v3/publications/file/file/
     - Create a file publication
   * - `\ **delete** <PublicationsFileApi.md#delete>`_
     - **DELETE** {file_publication_href}
     - Delete a file publication
   * - `\ **list** <PublicationsFileApi.md#list>`_
     - **GET** /pulp/api/v3/publications/file/file/
     - List file publications
   * - `\ **read** <PublicationsFileApi.md#read>`_
     - **GET** {file_publication_href}
     - Inspect a file publication


**create**
==============

..

   AsyncOperationResponse create(data)


Create a file publication

Trigger an asynchronous task to publish file content.

Example
^^^^^^^


* Basic Authentication (Basic):
  ```python
  from **future** import print_function
  import time
  import pulpcore.client.pulp_file
  from pulpcore.client.pulp_file.rest import ApiException
  from pprint import pprint
  configuration = pulpcore.client.pulp_file.Configuration()
  # Configure HTTP basic authorization: Basic
  configuration.username = 'YOUR_USERNAME'
  configuration.password = 'YOUR_PASSWORD'

Defining host is optional and default to http://localhost:24817
===============================================================

configuration.host = "http://localhost:24817"

Enter a context with an instance of the API client
==================================================

with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:

.. code-block::

   # Create an instance of the API class
   api_instance = pulpcore.client.pulp_file.PublicationsFileApi(api_client)
   data = pulpcore.client.pulp_file.FileFilePublication() # FileFilePublication | 

   try:
       # Create a file publication
       api_response = api_instance.create(data)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling PublicationsFileApi->create: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **data** | [**FileFilePublication**](FileFilePublication.md)|  | 

   ### Return type

   [**AsyncOperationResponse**](AsyncOperationResponse.md)

   ### Authorization

   [Basic](../README.md#Basic)

   ### HTTP request headers

    - **Content-Type**: application/json
    - **Accept**: application/json

   ### HTTP response details
   | Status code | Description | Response headers |
   |-------------|-------------|------------------|
   **202** |  |  -  |

   [[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

   # **delete**
   > delete(file_publication_href)

   Delete a file publication

    A FilePublication contains metadata about all the File Content in a particular File Repository Version. Once a FilePublication has been created, it can be hosted using the File Distribution API.

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
       api_instance = pulpcore.client.pulp_file.PublicationsFileApi(api_client)
       file_publication_href = 'file_publication_href_example' # str | URI of File Publication. e.g.: /pulp/api/v3/publications/file/file/1/

       try:
           # Delete a file publication
           api_instance.delete(file_publication_href)
       except ApiException as e:
           print("Exception when calling PublicationsFileApi->delete: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_publication_href**
     - **str**
     - URI of File Publication. e.g.: /pulp/api/v3/publications/file/file/1/
     - 


Return type
^^^^^^^^^^^

void (empty response body)

Authorization
^^^^^^^^^^^^^

`Basic <../README.md#Basic>`_

HTTP request headers
^^^^^^^^^^^^^^^^^^^^


* **Content-Type**\ : Not defined
* **Accept**\ : Not defined

HTTP response details
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Status code
     - Description
     - Response headers
   * - 


**204** |  |  -  |

`[Back to top] <#>`_ `[Back to API list] <../README.md#documentation-for-api-endpoints>`_ `[Back to Model list] <../README.md#documentation-for-models>`_ `[Back to README] <../README.md>`_

**list**
============

..

   InlineResponse2004 list(ordering=ordering, repository_version=repository_version, pulp_created\ **lt=pulp_created**\ lt, pulp_created\ **lte=pulp_created**\ lte, pulp_created\ **gt=pulp_created**\ gt, pulp_created\ **gte=pulp_created**\ gte, pulp_created\ **range=pulp_created**\ range, pulp_created=pulp_created, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)


List file publications

 A FilePublication contains metadata about all the File Content in a particular File Repository Version. Once a FilePublication has been created, it can be hosted using the File Distribution API.

Example
^^^^^^^


* Basic Authentication (Basic):
  ```python
  from **future** import print_function
  import time
  import pulpcore.client.pulp_file
  from pulpcore.client.pulp_file.rest import ApiException
  from pprint import pprint
  configuration = pulpcore.client.pulp_file.Configuration()
  # Configure HTTP basic authorization: Basic
  configuration.username = 'YOUR_USERNAME'
  configuration.password = 'YOUR_PASSWORD'

Defining host is optional and default to http://localhost:24817
===============================================================

configuration.host = "http://localhost:24817"

Enter a context with an instance of the API client
==================================================

with pulpcore.client.pulp_file.ApiClient(configuration) as api_client:

.. code-block::

   # Create an instance of the API class
   api_instance = pulpcore.client.pulp_file.PublicationsFileApi(api_client)
   ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

repository_version = 'repository_version_example' # str | Repository Version referenced by HREF (optional)
pulp_created\ **lt = 'pulp_created**\ lt_example' # str | Filter results where pulp_created is less than value (optional)
pulp_created\ **lte = 'pulp_created**\ lte_example' # str | Filter results where pulp_created is less than or equal to value (optional)
pulp_created\ **gt = 'pulp_created**\ gt_example' # str | Filter results where pulp_created is greater than value (optional)
pulp_created\ **gte = 'pulp_created**\ gte_example' # str | Filter results where pulp_created is greater than or equal to value (optional)
pulp_created\ **range = 'pulp_created**\ range_example' # str | Filter results where pulp_created is between two comma separated values (optional)
pulp_created = 'pulp_created_example' # str | ISO 8601 formatted dates are supported (optional)
limit = 56 # int | Number of results to return per page. (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

.. code-block::

   try:
       # List file publications
       api_response = api_instance.list(ordering=ordering, repository_version=repository_version, pulp_created__lt=pulp_created__lt, pulp_created__lte=pulp_created__lte, pulp_created__gt=pulp_created__gt, pulp_created__gte=pulp_created__gte, pulp_created__range=pulp_created__range, pulp_created=pulp_created, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling PublicationsFileApi->list: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **ordering** | **str**| Which field to use when ordering the results. | [optional] 
    **repository_version** | **str**| Repository Version referenced by HREF | [optional] 
    **pulp_created__lt** | **str**| Filter results where pulp_created is less than value | [optional] 
    **pulp_created__lte** | **str**| Filter results where pulp_created is less than or equal to value | [optional] 
    **pulp_created__gt** | **str**| Filter results where pulp_created is greater than value | [optional] 
    **pulp_created__gte** | **str**| Filter results where pulp_created is greater than or equal to value | [optional] 
    **pulp_created__range** | **str**| Filter results where pulp_created is between two comma separated values | [optional] 
    **pulp_created** | **str**| ISO 8601 formatted dates are supported | [optional] 
    **limit** | **int**| Number of results to return per page. | [optional] 
    **offset** | **int**| The initial index from which to return the results. | [optional] 
    **fields** | **str**| A list of fields to include in the response. | [optional] 
    **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

   ### Return type

   [**InlineResponse2004**](InlineResponse2004.md)

   ### Authorization

   [Basic](../README.md#Basic)

   ### HTTP request headers

    - **Content-Type**: Not defined
    - **Accept**: application/json

   ### HTTP response details
   | Status code | Description | Response headers |
   |-------------|-------------|------------------|
   **200** |  |  -  |

   [[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

   # **read**
   > FileFilePublication read(file_publication_href, fields=fields, exclude_fields=exclude_fields)

   Inspect a file publication

    A FilePublication contains metadata about all the File Content in a particular File Repository Version. Once a FilePublication has been created, it can be hosted using the File Distribution API.

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
       api_instance = pulpcore.client.pulp_file.PublicationsFileApi(api_client)
       file_publication_href = 'file_publication_href_example' # str | URI of File Publication. e.g.: /pulp/api/v3/publications/file/file/1/
   fields = 'fields_example' # str | A list of fields to include in the response. (optional)
   exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

       try:
           # Inspect a file publication
           api_response = api_instance.read(file_publication_href, fields=fields, exclude_fields=exclude_fields)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling PublicationsFileApi->read: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_publication_href**
     - **str**
     - URI of File Publication. e.g.: /pulp/api/v3/publications/file/file/1/
     - 
   * -  **fields**
     - **str**
     - A list of fields to include in the response.
     - [optional] 
   * -  **exclude_fields**
     - **str**
     - A list of fields to exclude from the response.
     - [optional] 


Return type
^^^^^^^^^^^

`\ **FileFilePublication** <FileFilePublication.md>`_

Authorization
^^^^^^^^^^^^^

`Basic <../README.md#Basic>`_

HTTP request headers
^^^^^^^^^^^^^^^^^^^^


* **Content-Type**\ : Not defined
* **Accept**\ : application/json

HTTP response details
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Status code
     - Description
     - Response headers
   * - 


**200** |  |  -  |

`[Back to top] <#>`_ `[Back to API list] <../README.md#documentation-for-api-endpoints>`_ `[Back to Model list] <../README.md#documentation-for-models>`_ `[Back to README] <../README.md>`_
