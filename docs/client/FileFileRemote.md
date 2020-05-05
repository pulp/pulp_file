# FileFileRemote

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pulp_href** | **str** |  | [optional] [readonly] 
**pulp_created** | **datetime** | Timestamp of creation. | [optional] [readonly] 
**name** | **str** | A unique name for this remote. | 
**url** | **str** | The URL of an external content source. | 
**ca_cert** | **str** | A string containing the PEM encoded CA certificate used to validate the server certificate presented by the remote server. All new line characters must be escaped. Returns SHA256 checksum of the certificate file on GET. | [optional] 
**client_cert** | **str** | A string containing the PEM encoded client certificate used for authentication. All new line characters must be escaped. Returns SHA256 checksum of the certificate file on GET. | [optional] 
**client_key** | **str** | A PEM encoded private key used for authentication. Returns SHA256 checksum of the certificate file on GET. | [optional] 
**tls_validation** | **bool** | If True, TLS peer validation must be performed. | [optional] 
**proxy_url** | **str** | The proxy URL. Format: scheme://user:password@host:port | [optional] 
**pulp_last_updated** | **datetime** | Timestamp of the most recent update of the remote. | [optional] [readonly] 
**download_concurrency** | **int** | Total number of simultaneous connections. | [optional] 
**policy** | **str** | The policy to use when downloading content. The possible values include: &#39;immediate&#39;, &#39;on_demand&#39;, and &#39;streamed&#39;. &#39;immediate&#39; is the default. | [optional] [default to 'immediate']

[[Back to Model list]](../client.md#documentation-for-models) [[Back to API list]](../client.md#documentation-for-api-endpoints) [[Back to client]](../client.md)


