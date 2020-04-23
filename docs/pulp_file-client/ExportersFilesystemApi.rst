
pulpcore.client.pulp_file.ExportersFilesystemApi
================================================

All URIs are relative to *http://localhost:24817*

.. list-table::
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `\ **create** <ExportersFilesystemApi.md#create>`_
     - **POST** /pulp/api/v3/exporters/file/filesystem/
     - Create a file file system exporter
   * - `\ **delete** <ExportersFilesystemApi.md#delete>`_
     - **DELETE** {file_file_system_exporter_href}
     - Delete a file file system exporter
   * - `\ **list** <ExportersFilesystemApi.md#list>`_
     - **GET** /pulp/api/v3/exporters/file/filesystem/
     - List file file system exporters
   * - `\ **partial_update** <ExportersFilesystemApi.md#partial_update>`_
     - **PATCH** {file_file_system_exporter_href}
     - Partially update a file file system exporter
   * - `\ **read** <ExportersFilesystemApi.md#read>`_
     - **GET** {file_file_system_exporter_href}
     - Inspect a file file system exporter
   * - `\ **update** <ExportersFilesystemApi.md#update>`_
     - **PUT** {file_file_system_exporter_href}
     - Update a file file system exporter


**create**
==============

..

   FileFileFileSystemExporter create(data)


Create a file file system exporter

FileSystemExporters export content from a publication to a path on the file system.

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
   api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
   data = pulpcore.client.pulp_file.FileFileFileSystemExporter() # FileFileFileSystemExporter | 

   try:
       # Create a file file system exporter
       api_response = api_instance.create(data)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling ExportersFilesystemApi->create: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **data** | [**FileFileFileSystemExporter**](FileFileFileSystemExporter.md)|  | 

   ### Return type

   [**FileFileFileSystemExporter**](FileFileFileSystemExporter.md)

   ### Authorization

   [Basic](../README.md#Basic)

   ### HTTP request headers

    - **Content-Type**: application/json
    - **Accept**: application/json

   ### HTTP response details
   | Status code | Description | Response headers |
   |-------------|-------------|------------------|
   **201** |  |  -  |

   [[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

   # **delete**
   > delete(file_file_system_exporter_href)

   Delete a file file system exporter

   FileSystemExporters export content from a publication to a path on the file system.

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
       api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
       file_file_system_exporter_href = 'file_file_system_exporter_href_example' # str | URI of File File System Exporter. e.g.: /pulp/api/v3/exporters/file/filesystem/1/

       try:
           # Delete a file file system exporter
           api_instance.delete(file_file_system_exporter_href)
       except ApiException as e:
           print("Exception when calling ExportersFilesystemApi->delete: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_file_system_exporter_href**
     - **str**
     - URI of File File System Exporter. e.g.: /pulp/api/v3/exporters/file/filesystem/1/
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

   InlineResponse2002 list(ordering=ordering, name=name, name\ **in=name**\ in, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)


List file file system exporters

FileSystemExporters export content from a publication to a path on the file system.

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
   api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
   ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

name = 'name_example' # str |  (optional)
name\ **in = 'name**\ in_example' # str | Filter results where name is in a comma-separated list of values (optional)
limit = 56 # int | Number of results to return per page. (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

.. code-block::

   try:
       # List file file system exporters
       api_response = api_instance.list(ordering=ordering, name=name, name__in=name__in, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling ExportersFilesystemApi->list: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **ordering** | **str**| Which field to use when ordering the results. | [optional] 
    **name** | **str**|  | [optional] 
    **name__in** | **str**| Filter results where name is in a comma-separated list of values | [optional] 
    **limit** | **int**| Number of results to return per page. | [optional] 
    **offset** | **int**| The initial index from which to return the results. | [optional] 
    **fields** | **str**| A list of fields to include in the response. | [optional] 
    **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

   ### Return type

   [**InlineResponse2002**](InlineResponse2002.md)

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
   > FileFileFileSystemExporter partial_update(file_file_system_exporter_href, data)

   Partially update a file file system exporter

   FileSystemExporters export content from a publication to a path on the file system.

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
       api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
       file_file_system_exporter_href = 'file_file_system_exporter_href_example' # str | URI of File File System Exporter. e.g.: /pulp/api/v3/exporters/file/filesystem/1/
   data = pulpcore.client.pulp_file.FileFileFileSystemExporter() # FileFileFileSystemExporter | 

       try:
           # Partially update a file file system exporter
           api_response = api_instance.partial_update(file_file_system_exporter_href, data)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling ExportersFilesystemApi->partial_update: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_file_system_exporter_href**
     - **str**
     - URI of File File System Exporter. e.g.: /pulp/api/v3/exporters/file/filesystem/1/
     - 
   * -  **data**
     - `\ **FileFileFileSystemExporter** <FileFileFileSystemExporter.md>`_
     - 
     - 


Return type
^^^^^^^^^^^

`\ **FileFileFileSystemExporter** <FileFileFileSystemExporter.md>`_

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


**200** |  |  -  |

`[Back to top] <#>`_ `[Back to API list] <../README.md#documentation-for-api-endpoints>`_ `[Back to Model list] <../README.md#documentation-for-models>`_ `[Back to README] <../README.md>`_

**read**
============

..

   FileFileFileSystemExporter read(file_file_system_exporter_href, fields=fields, exclude_fields=exclude_fields)


Inspect a file file system exporter

FileSystemExporters export content from a publication to a path on the file system.

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
   api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
   file_file_system_exporter_href = 'file_file_system_exporter_href_example' # str | URI of File File System Exporter. e.g.: /pulp/api/v3/exporters/file/filesystem/1/

fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

.. code-block::

   try:
       # Inspect a file file system exporter
       api_response = api_instance.read(file_file_system_exporter_href, fields=fields, exclude_fields=exclude_fields)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling ExportersFilesystemApi->read: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **file_file_system_exporter_href** | **str**| URI of File File System Exporter. e.g.: /pulp/api/v3/exporters/file/filesystem/1/ | 
    **fields** | **str**| A list of fields to include in the response. | [optional] 
    **exclude_fields** | **str**| A list of fields to exclude from the response. | [optional] 

   ### Return type

   [**FileFileFileSystemExporter**](FileFileFileSystemExporter.md)

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
   > FileFileFileSystemExporter update(file_file_system_exporter_href, data)

   Update a file file system exporter

   FileSystemExporters export content from a publication to a path on the file system.

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
       api_instance = pulpcore.client.pulp_file.ExportersFilesystemApi(api_client)
       file_file_system_exporter_href = 'file_file_system_exporter_href_example' # str | URI of File File System Exporter. e.g.: /pulp/api/v3/exporters/file/filesystem/1/
   data = pulpcore.client.pulp_file.FileFileFileSystemExporter() # FileFileFileSystemExporter | 

       try:
           # Update a file file system exporter
           api_response = api_instance.update(file_file_system_exporter_href, data)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling ExportersFilesystemApi->update: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_file_system_exporter_href**
     - **str**
     - URI of File File System Exporter. e.g.: /pulp/api/v3/exporters/file/filesystem/1/
     - 
   * -  **data**
     - `\ **FileFileFileSystemExporter** <FileFileFileSystemExporter.md>`_
     - 
     - 


Return type
^^^^^^^^^^^

`\ **FileFileFileSystemExporter** <FileFileFileSystemExporter.md>`_

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


**200** |  |  -  |

`[Back to top] <#>`_ `[Back to API list] <../README.md#documentation-for-api-endpoints>`_ `[Back to Model list] <../README.md#documentation-for-models>`_ `[Back to README] <../README.md>`_
