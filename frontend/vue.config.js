let moduleExports = {}

// For HMR to work properly over local network (/etc/hosts).
const devServer = {
  disableHostCheck: true,
  public: process.env.VIRTUAL_HOST
}

if (process.env.NODE_ENV !== 'production') {
  moduleExports.devServer = devServer
}

module.exports = moduleExports
