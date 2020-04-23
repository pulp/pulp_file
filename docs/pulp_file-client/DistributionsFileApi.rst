
pulpcore.client.pulp_file.DistributionsFileApi
==============================================

All URIs are relative to *http://localhost:24817*

.. list-table::
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `\ **create** <DistributionsFileApi.md#create>`_
     - **POST** /pulp/api/v3/distributions/file/file/
     - Create a file distribution
   * - `\ **delete** <DistributionsFileApi.md#delete>`_
     - **DELETE** {file_distribution_href}
     - Delete a file distribution
   * - `\ **list** <DistributionsFileApi.md#list>`_
     - **GET** /pulp/api/v3/distributions/file/file/
     - List file distributions
   * - `\ **partial_update** <DistributionsFileApi.md#partial_update>`_
     - **PATCH** {file_distribution_href}
     - Partially update a file distribution
   * - `\ **read** <DistributionsFileApi.md#read>`_
     - **GET** {file_distribution_href}
     - Inspect a file distribution
   * - `\ **update** <DistributionsFileApi.md#update>`_
     - **PUT** {file_distribution_href}
     - Update a file distribution


**create**
==============

..

   AsyncOperationResponse create(data)


Create a file distribution

Trigger an asynchronous create task

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
   api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
   data = pulpcore.client.pulp_file.FileFileDistribution() # FileFileDistribution | 

   try:
       # Create a file distribution
       api_response = api_instance.create(data)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling DistributionsFileApi->create: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **data** | [**FileFileDistribution**](FileFileDistribution.md)|  | 

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
   > AsyncOperationResponse delete(file_distribution_href)

   Delete a file distribution

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
       api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
       file_distribution_href = 'file_distribution_href_example' # str | URI of File Distribution. e.g.: /pulp/api/v3/distributions/file/file/1/

       try:
           # Delete a file distribution
           api_response = api_instance.delete(file_distribution_href)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling DistributionsFileApi->delete: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_distribution_href**
     - **str**
     - URI of File Distribution. e.g.: /pulp/api/v3/distributions/file/file/1/
     - 


Return type
^^^^^^^^^^^

`\ **AsyncOperationResponse** <AsyncOperationResponse.md>`_

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


**202** |  |  -  |

`[Back to top] <#>`_ `[Back to API list] <../README.md#documentation-for-api-endpoints>`_ `[Back to Model list] <../README.md#documentation-for-models>`_ `[Back to README] <../README.md>`_

**list**
============

..

   InlineResponse2001 list(ordering=ordering, name=name, name\ **in=name**\ in, base_path=base_path, base_path\ **contains=base_path**\ contains, base_path\ **icontains=base_path**\ icontains, base_path\ **in=base_path**\ in, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)


List file distributions

 FileDistributions host File Publications which makes the metadata and the referenced File Content available to HTTP clients. Additionally, a FileDistribution with an associated FilePublication can be the target url of a File Remote , allowing another instance of Pulp to sync the content.

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
   api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
   ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

name = 'name_example' # str |  (optional)
name\ **in = 'name**\ in_example' # str | Filter results where name is in a comma-separated list of values (optional)
base_path = 'base_path_example' # str |  (optional)
base_path\ **contains = 'base_path**\ contains_example' # str | Filter results where base_path contains value (optional)
base_path\ **icontains = 'base_path**\ icontains_example' # str | Filter results where base_path contains value (optional)
base_path\ **in = 'base_path**\ in_example' # str | Filter results where base_path is in a comma-separated list of values (optional)
limit = 56 # int | Number of results to return per page. (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

.. code-block::

   try:
       # List file distributions
       api_response = api_instance.list(ordering=ordering, name=name, name__in=name__in, base_path=base_path, base_path__contains=base_path__contains, base_path__icontains=base_path__icontains, base_path__in=base_path__in, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling DistributionsFileApi->list: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **ordering** | **str**| Which field to use when ordering the results. | [optional] 
    **name** | **str**|  | [optional] 
    **name__in** | **str**| Filter results where name is in a comma-separated list of values | [optional] 
    **base_path** | **str**|  | [optional] 
    **base_path__contains** | **str**| Filter results where base_path contains value | [optional] 
    **base_path__icontains** | **str**| Filter results where base_path contains value | [optional] 
    **base_path__in** | **str**| Filter results where base_path is in a comma-separated list of values | [optional] 
    **limit** | **int**| Number of results to return per page. | [optional] 
    **offset** | **int**| The initial index from which to return the results. | [optional] 
    **fields** | **str**| A list of fields to include in the response. | [optional] 
    **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

   ### Return type

   [**InlineResponse2001**](InlineResponse2001.md)

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

   # **partial_update**
   > AsyncOperationResponse partial_update(file_distribution_href, data)

   Partially update a file distribution

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
       api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
       file_distribution_href = 'file_distribution_href_example' # str | URI of File Distribution. e.g.: /pulp/api/v3/distributions/file/file/1/
   data = pulpcore.client.pulp_file.FileFileDistribution() # FileFileDistribution | 

       try:
           # Partially update a file distribution
           api_response = api_instance.partial_update(file_distribution_href, data)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling DistributionsFileApi->partial_update: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_distribution_href**
     - **str**
     - URI of File Distribution. e.g.: /pulp/api/v3/distributions/file/file/1/
     - 
   * -  **data**
     - `\ **FileFileDistribution** <FileFileDistribution.md>`_
     - 
     - 


Return type
^^^^^^^^^^^

`\ **AsyncOperationResponse** <AsyncOperationResponse.md>`_

Authorization
^^^^^^^^^^^^^

`Basic <../README.md#Basic>`_

HTTP request headers
^^^^^^^^^^^^^^^^^^^^


* **Content-Type**\ : application/json
* **Accept**\ : application/json

HTTP response details
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Status code
     - Description
     - Response headers
   * - 


**202** |  |  -  |

`[Back to top] <#>`_ `[Back to API list] <../README.md#documentation-for-api-endpoints>`_ `[Back to Model list] <../README.md#documentation-for-models>`_ `[Back to README] <../README.md>`_

**read**
============

..

   FileFileDistribution read(file_distribution_href, fields=fields, exclude_fields=exclude_fields)


Inspect a file distribution

 FileDistributions host File Publications which makes the metadata and the referenced File Content available to HTTP clients. Additionally, a FileDistribution with an associated FilePublication can be the target url of a File Remote , allowing another instance of Pulp to sync the content.

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
   api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
   file_distribution_href = 'file_distribution_href_example' # str | URI of File Distribution. e.g.: /pulp/api/v3/distributions/file/file/1/

fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

.. code-block::

   try:
       # Inspect a file distribution
       api_response = api_instance.read(file_distribution_href, fields=fields, exclude_fields=exclude_fields)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling DistributionsFileApi->read: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **file_distribution_href** | **str**| URI of File Distribution. e.g.: /pulp/api/v3/distributions/file/file/1/ | 
    **fields** | **str**| A list of fields to include in the response. | [optional] 
    **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

   ### Return type

   [**FileFileDistribution**](FileFileDistribution.md)

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

   # **update**
   > AsyncOperationResponse update(file_distribution_href, data)

   Update a file distribution

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
       api_instance = pulpcore.client.pulp_file.DistributionsFileApi(api_client)
       file_distribution_href = 'file_distribution_href_example' # str | URI of File Distribution. e.g.: /pulp/api/v3/distributions/file/file/1/
   data = pulpcore.client.pulp_file.FileFileDistribution() # FileFileDistribution | 

       try:
           # Update a file distribution
           api_response = api_instance.update(file_distribution_href, data)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling DistributionsFileApi->update: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_distribution_href**
     - **str**
     - URI of File Distribution. e.g.: /pulp/api/v3/distributions/file/file/1/
     - 
   * -  **data**
     - `\ **FileFileDistribution** <FileFileDistribution.md>`_
     - 
     - 


Return type
^^^^^^^^^^^

`\ **AsyncOperationResponse** <AsyncOperationResponse.md>`_

Authorization
^^^^^^^^^^^^^

`Basic <../README.md#Basic>`_

HTTP request headers
^^^^^^^^^^^^^^^^^^^^


* **Content-Type**\ : application/json
* **Accept**\ : application/json

HTTP response details
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Status code
     - Description
     - Response headers
   * - 


**202** |  |  -  |

`[Back to top] <#>`_ `[Back to API list] <../README.md#documentation-for-api-endpoints>`_ `[Back to Model list] <../README.md#documentation-for-models>`_ `[Back to README] <../README.md>`_
