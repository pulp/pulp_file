# FileFileDistribution

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pulp_href** | **str** |  | [optional] [readonly] 
**pulp_created** | **datetime** | Timestamp of creation. | [optional] [readonly] 
**base_path** | **str** | The base (relative) path component of the published url. Avoid paths that                     overlap with other distribution base paths (e.g. \&quot;foo\&quot; and \&quot;foo/bar\&quot;) | 
**base_url** | **str** | The URL for accessing the publication as defined by this distribution. | [optional] [readonly] 
**content_guard** | **str** | An optional content-guard. | [optional] 
**name** | **str** | A unique name. Ex, &#x60;rawhide&#x60; and &#x60;stable&#x60;. | 
**publication** | **str** | Publication to be served | [optional] 

[[Back to Model list]](../client.md#documentation-for-models) [[Back to API list]](../client.md#documentation-for-api-endpoints) [[Back to client]](../client.md)


