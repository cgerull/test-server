param location string = 'westeurope'

// resource group 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  
//   name: 'rg_clgr_testserver_dev'
//   location: location
// }

resource appServicePlan 'Microsoft.Web/serverFarms@2022-03-01' = {
  name: 'testserver-dev-plan'
  location: location
  sku: {
    name: 'F1'
  }
}

resource appServiceApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'testserver-dev-launch-1'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
  }
}
