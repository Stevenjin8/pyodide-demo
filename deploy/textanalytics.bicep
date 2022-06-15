param name string

resource textAnalytics 'Microsoft.CognitiveServices/accounts@2022-03-01' = {
  name: name
  location: 'eastus'
  kind: 'TextAnalytics'
  identity: {
    type: 'SystemAssigned'
  }
  sku:{
    name: 'S'
  }
  properties: {
    apiProperties: {}
    customSubDomainName: name
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'
  }
}

output endpoint string = textAnalytics.properties.endpoint
output keys string = textAnalytics.listKeys()['key1']
