
pulpcore.client.pulp_file.ExportersFileExportsApi
=================================================

All URIs are relative to *http://localhost:24817*

.. list-table::
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `\ **create** <ExportersFileExportsApi.md#create>`_
     - **POST** /pulp/api/v3/exporters/file/filesystem/{exporter_pk}/exports/
     - Create an export
   * - `\ **delete** <ExportersFileExportsApi.md#delete>`_
     - **DELETE** {export_href}
     - Delete an export
   * - `\ **list** <ExportersFileExportsApi.md#list>`_
     - **GET** /pulp/api/v3/exporters/file/filesystem/{exporter_pk}/exports/
     - List exports
   * - `\ **read** <ExportersFileExportsApi.md#read>`_
     - **GET** {export_href}
     - Inspect an export


**create**
==============

..

   AsyncOperationResponse create(exporter_pk, data)


Create an export

Trigger an asynchronous task to export a file publication.

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
   api_instance = pulpcore.client.pulp_file.ExportersFileExportsApi(api_client)
   exporter_pk = 'exporter_pk_example' # str | 

data = pulpcore.client.pulp_file.PublicationExport() # PublicationExport | 

.. code-block::

   try:
       # Create an export
       api_response = api_instance.create(exporter_pk, data)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling ExportersFileExportsApi->create: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **exporter_pk** | **str**|  | 
    **data** | [**PublicationExport**](PublicationExport.md)|  | 

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
   > delete(export_href)

   Delete an export

   FileSystemExports provide a history of previous exports.

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
       api_instance = pulpcore.client.pulp_file.ExportersFileExportsApi(api_client)
       export_href = 'export_href_example' # str | URI of Export. e.g.: /pulp/api/v3/exporters/file/filesystem/1/exports/1/

       try:
           # Delete an export
           api_instance.delete(export_href)
       except ApiException as e:
           print("Exception when calling ExportersFileExportsApi->delete: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **export_href**
     - **str**
     - URI of Export. e.g.: /pulp/api/v3/exporters/file/filesystem/1/exports/1/
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

   InlineResponse2003 list(exporter_pk, ordering=ordering, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)


List exports

FileSystemExports provide a history of previous exports.

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
   api_instance = pulpcore.client.pulp_file.ExportersFileExportsApi(api_client)
   exporter_pk = 'exporter_pk_example' # str | 

ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
limit = 56 # int | Number of results to return per page. (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

.. code-block::

   try:
       # List exports
       api_response = api_instance.list(exporter_pk, ordering=ordering, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling ExportersFileExportsApi->list: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **exporter_pk** | **str**|  | 
    **ordering** | **str**| Which field to use when ordering the results. | [optional] 
    **limit** | **int**| Number of results to return per page. | [optional] 
    **offset** | **int**| The initial index from which to return the results. | [optional] 
    **fields** | **str**| A list of fields to include in the response. | [optional] 
    **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

   ### Return type

   [**InlineResponse2003**](InlineResponse2003.md)

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
   > Export read(export_href, fields=fields, exclude_fields=exclude_fields)

   Inspect an export

   FileSystemExports provide a history of previous exports.

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
       api_instance = pulpcore.client.pulp_file.ExportersFileExportsApi(api_client)
       export_href = 'export_href_example' # str | URI of Export. e.g.: /pulp/api/v3/exporters/file/filesystem/1/exports/1/
   fields = 'fields_example' # str | A list of fields to include in the response. (optional)
   exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

       try:
           # Inspect an export
           api_response = api_instance.read(export_href, fields=fields, exclude_fields=exclude_fields)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling ExportersFileExportsApi->read: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **export_href**
     - **str**
     - URI of Export. e.g.: /pulp/api/v3/exporters/file/filesystem/1/exports/1/
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

`\ **Export** <Export.md>`_

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
