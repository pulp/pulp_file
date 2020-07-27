# RepositoryVersionResponse

Base serializer for use with :class:`pulpcore.app.models.Model`  This ensures that all Serializers provide values for the 'pulp_href` field.  The class provides a default for the ``ref_name`` attribute in the ModelSerializers's ``Meta`` class. This ensures that the OpenAPI definitions of plugins are namespaced properly.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pulp_href** | **str** |  | [optional] [readonly] 
**pulp_created** | **datetime** | Timestamp of creation. | [optional] [readonly] 
**number** | **int** |  | [optional] [readonly] 
**base_version** | **str** | A repository version whose content was used as the initial set of content for this repository version | [optional] 
**content_summary** | [**ContentSummaryResponse**](ContentSummaryResponse.md) | Various count summaries of the content in the version and the HREF to view them. | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


