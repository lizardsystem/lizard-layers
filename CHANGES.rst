Changelog of lizard-layers
===================================================


0.1.5 (2012-03-08)
------------------

- Add dependency to migration.

- Add models, migrations and sql for geoserver views

- Add management command for syncing ekr layers


0.1.4 (2012-02-28)
------------------

- Redesigned GeoserverLayer view, to support different styles of
  multiple layer specification in url.


0.1.3 (2012-02-28)
------------------

- Reworked Geoserverlayer view to support already present cql


0.1.2 (2012-02-22)
------------------

- Improve buildout config

- Change geoserver_layer view to class-based one

- Support multiple layers in geoserver_layer view

- Add some lines in README

- Add a test and a doctest


0.1.1 (2012-02-21)
------------------

- Add MANIFEST.in to make packages actually work.


0.1 (2012-02-21)
----------------

- Initial library skeleton created by nensskel.

- Add wms view that adds cql filter based on user
  permissions (see lizard_security)

- Change configuration to make tests work.
