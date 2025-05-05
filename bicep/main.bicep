param location string = resourceGroup().location
param postgresAdmin string
@secure()
param postgresPassword string
param appName string
param sku string = 'B1'

resource plan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: '${appName}-plan'
  location: location
  sku: {
    name: sku
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: plan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
    }
  }
}

resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2022-01-20-preview' = {
  name: '${appName}-psql'
  location: location
  properties: {
    administratorLogin: postgresAdmin
    administratorLoginPassword: postgresPassword
    version: '13'
    storage: {
      storageSizeGB: 32
    }
    sku: {
      name: 'B1ms'
      tier: 'Burstable'
      capacity: 1
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
  }
}

output webAppName string = webApp.name
output postgresHost string = postgres.properties.fullyQualifiedDomainName
