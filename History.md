
v0.1.4 / 2020-06-13
===================

  * listeners: run vet only if vet.run_on_post_save is true
  * errors: remove dedupe for now
  * conf: add vet.run_on_post_save flag
  * staticcheck: fix typo
  * listeners: remove annoying log.debug call
  * listeners: run static_check on post-save
  * add staticcheck command
  * dev: reload staticcheck
  * conf: add static_check
  * listeners: async completion for STv4
  * gocode: >=4070 as v4

v0.1.3 / 2020-04-18
===================

  * errors: show maximum of 1 error per view/line
  * gocode: add sublime v4 support
  * gocode: fix an issue with completion item exception

v0.1.2 / 2020-04-08
===================

  * commands: adjust to match the realpath of default settings
  * scripts/package: match PC zip structure

v0.1.1 / 2020-04-05
===================

  * exec: use root when picking up go env
  * settings: add optional root setting
  * commands: adjust settings default value
  * settings: add sublime menu to configure the plugin
  * exec: import startupinfo on windows only (@piotrkubisa)
  * exec: Do not show Windows cmd.exe on command execution (@piotrkubisa)
  * vet,lint: Properly discover linted file by go-vet (@piotrkubisa)
  * vet: Run on a package, not on a directoryc (@piotrkubisa)

v0.0.6 / 2019-11-13
===================

  * buffer: ocd
  * buffer: never complete on the 1st line
  * gocode: escape {} in completion template
  * make: add deps target
  * guru: fix invalid type handling
  * add go1.13
  * lint: strip filename
  * lint: go 1.13 fixes

v0.0.5 / 2019-08-31
===================

  * gocode: complete only when necessary
  * listeners: check if view is dirty
  * commands: add settings command

v0.0.4 / 2019-08-25
===================

  * completion: fix gocode edge-cases
  * config: rename to match other plugins
  * commands: add coverage to show inline test coverage

v0.0.3 / 2019-08-24
===================

  * tags: improve parsing and add preview
  * exec: automatically add GOPATH to PATH
  * gocode: add returns to completion preview
  * gocode: fix completion for funcs with no arguments

v0.0.2 / 2019-08-19
===================

  * commands: better naming
  * package-control support
  * decorators: cleanup

v0.0.1 / 2019-08-18
===================

  * Initial release
