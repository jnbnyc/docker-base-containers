#! groovy

node('docker') {
  checkout scm
  ansiColor('xterm') {
    try {
      load 'scripts/cibuild'
    } catch (Throwable e) {
      echo("See the previous stage for where this Error was thrown!\n\n${e}")
      throw e
    }
  }
}
