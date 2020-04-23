
pulpcore.client.pulp_file.ContentFilesApi
=========================================

All URIs are relative to *http://localhost:24817*

.. list-table::
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `\ **create** <ContentFilesApi.md#create>`_
     - **POST** /pulp/api/v3/content/file/files/
     - Create a file content
   * - `\ **list** <ContentFilesApi.md#list>`_
     - **GET** /pulp/api/v3/content/file/files/
     - List file contents
   * - `\ **read** <ContentFilesApi.md#read>`_
     - **GET** {file_content_href}
     - Inspect a file content


**create**
==============

..

   AsyncOperationResponse create(relative_path, artifact=artifact, file=file, repository=repository)


Create a file content

Trigger an asynchronous task to create content,optionally create new repository version.

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
   api_instance = pulpcore.client.pulp_file.ContentFilesApi(api_client)
   relative_path = 'relative_path_example' # str | Path where the artifact is located relative to distributions base_path

artifact = 'artifact_example' # str | Artifact file representing the physical content (optional)
file = '/path/to/file' # file | An uploaded file that should be turned into the artifact of the content unit. (optional)
repository = 'repository_example' # str | A URI of a repository the new content unit should be associated with. (optional)

.. code-block::

   try:
       # Create a file content
       api_response = api_instance.create(relative_path, artifact=artifact, file=file, repository=repository)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling ContentFilesApi->create: %s\n" % e)

.. code-block::


   ### Parameters

   Name | Type | Description  | Notes
   ------------- | ------------- | ------------- | -------------
    **relative_path** | **str**| Path where the artifact is located relative to distributions base_path | 
    **artifact** | **str**| Artifact file representing the physical content | [optional] 
    **file** | **file**| An uploaded file that should be turned into the artifact of the content unit. | [optional] 
    **repository** | **str**| A URI of a repository the new content unit should be associated with. | [optional] 

   ### Return type

   [**AsyncOperationResponse**](AsyncOperationResponse.md)

   ### Authorization

   [Basic](../README.md#Basic)

   ### HTTP request headers

    - **Content-Type**: multipart/form-data, application/x-www-form-urlencoded
    - **Accept**: application/json

   ### HTTP response details
   | Status code | Description | Response headers |
   |-------------|-------------|------------------|
   **202** |  |  -  |

   [[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

   # **list**
   > InlineResponse200 list(ordering=ordering, relative_path=relative_path, sha256=sha256, repository_version=repository_version, repository_version_added=repository_version_added, repository_version_removed=repository_version_removed, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)

   List file contents

    FileContent represents a single file and its metadata, which can be added and removed from repositories.

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
       api_instance = pulpcore.client.pulp_file.ContentFilesApi(api_client)
       ordering = 'ordering_example' # str | Which field to use when ordering the results. (optional)
   relative_path = 'relative_path_example' # str | Filter results where relative_path matches value (optional)
   sha256 = 'sha256_example' # str |  (optional)
   repository_version = 'repository_version_example' # str | Repository Version referenced by HREF (optional)
   repository_version_added = 'repository_version_added_example' # str | Repository Version referenced by HREF (optional)
   repository_version_removed = 'repository_version_removed_example' # str | Repository Version referenced by HREF (optional)
   limit = 56 # int | Number of results to return per page. (optional)
   offset = 56 # int | The initial index from which to return the results. (optional)
   fields = 'fields_example' # str | A list of fields to include in the response. (optional)
   exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

       try:
           # List file contents
           api_response = api_instance.list(ordering=ordering, relative_path=relative_path, sha256=sha256, repository_version=repository_version, repository_version_added=repository_version_added, repository_version_removed=repository_version_removed, limit=limit, offset=offset, fields=fields, exclude_fields=exclude_fields)
           pprint(api_response)
       except ApiException as e:
           print("Exception when calling ContentFilesApi->list: %s\n" % e)

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **ordering**
     - **str**
     - Which field to use when ordering the results.
     - [optional] 
   * -  **relative_path**
     - **str**
     - Filter results where relative_path matches value
     - [optional] 
   * -  **sha256**
     - **str**
     - 
     - [optional] 
   * -  **repository_version**
     - **str**
     - Repository Version referenced by HREF
     - [optional] 
   * -  **repository_version_added**
     - **str**
     - Repository Version referenced by HREF
     - [optional] 
   * -  **repository_version_removed**
     - **str**
     - Repository Version referenced by HREF
     - [optional] 
   * -  **limit**
     - **int**
     - Number of results to return per page.
     - [optional] 
   * -  **offset**
     - **int**
     - The initial index from which to return the results.
     - [optional] 
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

`\ **InlineResponse200** <InlineResponse200.md>`_

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

**read**
============

..

   FileFileContent read(file_content_href, fields=fields, exclude_fields=exclude_fields)


Inspect a file content

 FileContent represents a single file and its metadata, which can be added and removed from repositories.

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
   api_instance = pulpcore.client.pulp_file.ContentFilesApi(api_client)
   file_content_href = 'file_content_href_example' # str | URI of File Content. e.g.: /pulp/api/v3/content/file/files/1/

fields = 'fields_example' # str | A list of fields to include in the response. (optional)
exclude_fields = 'exclude_fields_example' # str | A list of fields to exclude from the response. (optional)

.. code-block::

   try:
       # Inspect a file content
       api_response = api_instance.read(file_content_href, fields=fields, exclude_fields=exclude_fields)
       pprint(api_response)
   except ApiException as e:
       print("Exception when calling ContentFilesApi->read: %s\n" % e)

```

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
     - Notes
   * -  **file_content_href**
     - **str**
     - URI of File Content. e.g.: /pulp/api/v3/content/file/files/1/
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

`\ **FileFileContent** <FileFileContent.md>`_

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
