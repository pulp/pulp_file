# FileFilePublication

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pulp_href** | **str** |  | [optional] [readonly] 
**pulp_created** | **datetime** | Timestamp of creation. | [optional] [readonly] 
**repository_version** | **str** |  | [optional] 
**repository** | **str** | A URI of the repository to be published. | [optional] 
**distributions** | **list[str]** | This publication is currently hosted as defined by these distributions. | [optional] [readonly] 
**manifest** | **str** | Filename to use for manifest file containing metadata for all the files. | [optional] [default to 'PULP_MANIFEST']

[[Back to Model list]](../client.md#documentation-for-models) [[Back to API list]](../client.md#documentation-for-api-endpoints) [[Back to client]](../client.md)


