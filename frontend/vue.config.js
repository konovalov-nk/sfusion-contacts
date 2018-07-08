let module_exports = {}

// For HMR to work properly over local network (/etc/hosts).
const devServer = {
  disableHostCheck: true,
  public: process.env.VIRTUAL_HOST
}

if (process.env.NODE_ENV !== 'production') {
  module_exports.devServer = devServer
}

module.exports = module_exports