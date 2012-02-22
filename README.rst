lizard-layers
==========================================

This is a Django app for management of all kinds of map layers.

- Remote WMS servers and their available layers (query feature)

- Lizard maplayers (registered from the lizard apps)

- Storage of workspaces and theme maps

- Generic and personal lists of maplayers that can be shared

- Communication with remote servers using getFeatureInfo to serve in the desired format

- Layer can have multiple 'legend' classes

Usage, etc.

Geoserver layer view
--------------------
/wms/ supports wms requests, which are sent to a local geoserver at
settings.GEOSERVER_URL. On the fly, lizard_security-based cql-filters
are added to filter objects on the geoserver based on group permissions.

