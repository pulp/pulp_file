
pulpcore.client.pulp_file.RepositoriesFileApi
=============================================

All URIs are relative to *http://localhost:24817*

.. list-table::
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `\ **create** <RepositoriesFileApi.md#create>`_
     - **POST** /pulp/api/v3/repositories/file/file/
     - Create a file repository
   * - `\ **delete** <RepositoriesFileApi.md#delete>`_
     - **DELETE** {file_repository_href}
     - Delete a file repository
   * - `\ **list** <RepositoriesFileApi.md#list>`_
     - **GET** /pulp/api/v3/repositories/file/file/
     - List file repositorys
   * - `\ **modify** <RepositoriesFileApi.md#modify>`_
     - **POST** {file_repository_href}modify/
     - Modify Repository Content
   * - `\ **partial_update** <RepositoriesFileApi.md#partial_update>`_
     - **PATCH** {file_repository_href}
     - Partially update a file repository
   * - `\ **read** <RepositoriesFileApi.md#read>`_
     - **GET** {file_repository_href}
     - Inspect a file repository
   * - `\ **sync** <RepositoriesFileApi.md#sync>`_
     - **POST** {file_repository_href}sync/
     - 
   * - `\ **update** <RepositoriesFileApi.md#update>`_
     - **PUT** {file_repository_href}
     - Update a file repository


**create**
==============

..

   FileFileRepository create(data)


Create a file repository

 FileRepository represents a single file repository, to which content can be synced, added, or removed.

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
   api_instance = pulpcore.client.pulp_file.RepositoriesFileApi(api_client)
   data = pulpcore.client.pulp_file.FileFileRepository() # FileFileRepository | 

   try:
       # Create a file repository
       api_response = api_instance.create(data)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling RepositoriesFileApi->create: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **data** | [**FileFileRepository**](FileFileRepository.md)|  | 

   ### Return type

   [**FileFileRepository**](FileFileRepository.md)

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
   > AsyncOperationResponse delete(file_repository_href)

   Delete a file repository

   Trigger an asynchronous task to delete a repository.

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
       api_instance = pulpcore.client.pulp_file.RepositoriesFileApi(api_client)
       file_repository_href = 'file_repository_href_example' # str | URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/

       try:
           # Delete a file repository
           api_response = api_instance.delete(file_repository_href)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling RepositoriesFileApi->delete: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_repository_href**
     - **str**
     - URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/
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

   InlineResponse2006 list(ordering=ordering, name=name, name\ **in=name**\ in, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)


List file repositorys

 FileRepository represents a single file repository, to which content can be synced, added, or removed.

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
   api_instance = pulpcore.client.pulp_file.RepositoriesFileApi(api_client)
   ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)

name = 'name_example' # str |  (optional)
name\ **in = 'name**\ in_example' # str | Filter results where name is in a comma-separated list of values (optional)
limit = 56 # int | Number of results to return per page. (optional)
offset = 56 # int | The initial index from which to return the results. (optional)
fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

.. code-block::

   try:
       # List file repositorys
       api_response = api_instance.list(ordering=ordering, name=name, name__in=name__in, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling RepositoriesFileApi->list: %s\n" % e)

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

   [**InlineResponse2006**](InlineResponse2006.md)

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

   # **modify**
   > AsyncOperationResponse modify(file_repository_href, data)

   Modify Repository Content

   Trigger an asynchronous task to create a new repository version.

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
       api_instance = pulpcore.client.pulp_file.RepositoriesFileApi(api_client)
       file_repository_href = 'file_repository_href_example' # str | URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/
   data = pulpcore.client.pulp_file.RepositoryAddRemoveContent() # RepositoryAddRemoveContent | 

       try:
           # Modify Repository Content
           api_response = api_instance.modify(file_repository_href, data)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling RepositoriesFileApi->modify: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_repository_href**
     - **str**
     - URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/
     - 
   * -  **data**
     - `\ **RepositoryAddRemoveContent** <RepositoryAddRemoveContent.md>`_
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

**partial_update**
======================

..

   FileFileRepository partial_update(file_repository_href, data)


Partially update a file repository

 FileRepository represents a single file repository, to which content can be synced, added, or removed.

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
   api_instance = pulpcore.client.pulp_file.RepositoriesFileApi(api_client)
   file_repository_href = 'file_repository_href_example' # str | URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/

data = pulpcore.client.pulp_file.FileFileRepository() # FileFileRepository | 

.. code-block::

   try:
       # Partially update a file repository
       api_response = api_instance.partial_update(file_repository_href, data)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling RepositoriesFileApi->partial_update: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **file_repository_href** | **str**| URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/ | 
    **data** | [**FileFileRepository**](FileFileRepository.md)|  | 

   ### Return type

   [**FileFileRepository**](FileFileRepository.md)

   ### Authorization

   [Basic](../README.md#Basic)

   ### HTTP request headers

    - **Content-Type**: application/json
    - **Accept**: application/json

   ### HTTP response details
   | Status code | Description | Response headers |
   |-------------|-------------|------------------|
   **200** |  |  -  |

   [[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

   # **read**
   > FileFileRepository read(file_repository_href, fields=fields, exclude_fields=exclude_fields)

   Inspect a file repository

    FileRepository represents a single file repository, to which content can be synced, added, or removed.

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
       api_instance = pulpcore.client.pulp_file.RepositoriesFileApi(api_client)
       file_repository_href = 'file_repository_href_example' # str | URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/
   fields = 'fields_example' # str | A list of fields to include in the response. (optional)
   exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

       try:
           # Inspect a file repository
           api_response = api_instance.read(file_repository_href, fields=fields, exclude_fields=exclude_fields)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling RepositoriesFileApi->read: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_repository_href**
     - **str**
     - URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/
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

`\ **FileFileRepository** <FileFileRepository.md>`_

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

**sync**
============

..

   AsyncOperationResponse sync(file_repository_href, data)


Trigger an asynchronous task to sync file content.

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
   api_instance = pulpcore.client.pulp_file.RepositoriesFileApi(api_client)
   file_repository_href = 'file_repository_href_example' # str | URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/

data = pulpcore.client.pulp_file.RepositorySyncURL() # RepositorySyncURL | 

.. code-block::

   try:
       api_response = api_instance.sync(file_repository_href, data)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling RepositoriesFileApi->sync: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **file_repository_href** | **str**| URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/ | 
    **data** | [**RepositorySyncURL**](RepositorySyncURL.md)|  | 

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

   # **update**
   > AsyncOperationResponse update(file_repository_href, data)

   Update a file repository

   Trigger an asynchronous task to update a repository.

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
       api_instance = pulpcore.client.pulp_file.RepositoriesFileApi(api_client)
       file_repository_href = 'file_repository_href_example' # str | URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/
   data = pulpcore.client.pulp_file.FileFileRepository() # FileFileRepository | 

       try:
           # Update a file repository
           api_response = api_instance.update(file_repository_href, data)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling RepositoriesFileApi->update: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_repository_href**
     - **str**
     - URI of File Repository. e.g.: /pulp/api/v3/repositories/file/file/1/
     - 
   * -  **data**
     - `\ **FileFileRepository** <FileFileRepository.md>`_
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
