# RepositoryAddRemoveContent

Base serializer for use with :class:`pulpcore.app.models.Model`  This ensures that all Serializers provide values for the 'pulp_href` field.  The class provides a default for the ``ref_name`` attribute in the ModelSerializers's ``Meta`` class. This ensures that the OpenAPI definitions of plugins are namespaced properly.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**add_content_units** | **list[object]** | A list of content units to add to a new repository version. This content is added after remove_content_units are removed. | [optional] 
**remove_content_units** | **list[object]** | A list of content units to remove from the latest repository version. You may also specify &#39;*&#39; as an entry to remove all content. This content is removed before add_content_units are added. | [optional] 
**base_version** | **str** | A repository version whose content will be used as the initial set of content for the new repository version | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


