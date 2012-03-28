Changelog of lizard-layers
===================================================


0.4.1 (2012-03-28)
------------------

- Changed AreaValue.comment field from TextField to CharField with
  migration.

- Added fields flag and comment to AreaValue admin.


0.4 (2012-03-28)
----------------

- Added flag and comment to AreaValue and migrations.

- Updated sync_layers to update flag and comment as well.


0.3.1 (2012-03-27)
------------------

- Added api and templates dir.


0.3 (2012-03-27)
----------------

- Added view and api for AreaValue as a table.


0.2 (2012-03-20)
----------------

- Add model for internal / external server mappings, including migration.
- Move geoserver external urls from settings to fixture.


0.1.10 (2012-03-19)
-------------------

- Fix bug where sync_task was used instead of dataset


0.1.9 (2012-03-16)
------------------

- Add view SecureLayerView.


0.1.8 (2012-03-09)
------------------

- Add real calculation of judgements.


0.1.7 (2012-03-08)
------------------

- Add model and migration for to map ekr values to parameters
- Have sync_layers use real fews ekr parameters


0.1.6 (2012-03-08)
------------------

- Changed manifest to include files from correct subdir.


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
