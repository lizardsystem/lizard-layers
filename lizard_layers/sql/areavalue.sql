/*
  This script can be used to generate some views for geoserver on the
  production database.

  TODO replace this stuff by some PL that is more dry.
*/

-- renaming columns sometimes not compatible with CREATE OR REPLACE.
DROP VIEW IF EXISTS krw_waterbody_linestring;
CREATE VIEW krw_waterbody_linestring AS
(
  SELECT 
    lizard_area_area.data_set_id, 
    lizard_area_area.is_active, 
    lizard_geo_geoobject.ident, 
    lizard_geo_geoobject.geometry, 
    lizard_area_area.area_class, 
    lizard_area_area.area_type, 
    lizard_area_communique."name",
    (lizard_geo_geoobject.id % 10) / 10.0 as random,
    (lizard_geo_geoobject.id % 10) / 10.0 as random1,
    (lizard_geo_geoobject.id % 10) / 10.0 as random2,
    (lizard_geo_geoobject.id % 10) / 10.0 as random3,
    (lizard_geo_geoobject.id % 10) / 10.0 as random4,
    (lizard_geo_geoobject.id % 5) - 2 as doel_result_map
  FROM 
    public.lizard_area_area, 
    public.lizard_area_communique, 
    public.lizard_geo_geoobject
  WHERE 
    lizard_area_area.communique_ptr_id = lizard_area_communique.geoobject_ptr_id AND
    lizard_area_communique.geoobject_ptr_id = lizard_geo_geoobject.id AND
    lizard_area_area.area_class = 1 AND
    GeometryType(lizard_geo_geoobject.geometry) in ('LINESTRING', 'MULTILINESTRING')
);


DROP VIEW IF EXISTS krw_waterbody_polygon;
CREATE VIEW krw_waterbody_polygon AS
(
  SELECT 
    lizard_area_area.data_set_id, 
    lizard_area_area.is_active, 
    lizard_geo_geoobject.ident, 
    lizard_geo_geoobject.geometry, 
    lizard_area_area.area_class, 
    lizard_area_area.area_type, 
    lizard_area_communique."name",
    (lizard_geo_geoobject.id % 10) / 10.0 as random,
    (lizard_geo_geoobject.id % 10) / 10.0 as random1,
    (lizard_geo_geoobject.id % 10) / 10.0 as random2,
    (lizard_geo_geoobject.id % 10) / 10.0 as random3,
    (lizard_geo_geoobject.id % 10) / 10.0 as random4,
    (lizard_geo_geoobject.id % 5) - 2 as doel_result_map
  FROM 
    public.lizard_area_area, 
    public.lizard_area_communique, 
    public.lizard_geo_geoobject
  WHERE 
    lizard_area_area.communique_ptr_id = lizard_area_communique.geoobject_ptr_id AND
    lizard_area_communique.geoobject_ptr_id = lizard_geo_geoobject.id AND
    lizard_area_area.area_class = 1 AND
    GeometryType(lizard_geo_geoobject.geometry) in ('POLYGON', 'MULTIPOLYGON')
);

DROP VIEW IF EXISTS area_polygon;
CREATE VIEW area_polygon AS
(
  SELECT 
    lizard_area_area.data_set_id, 
    lizard_area_area.is_active, 
    lizard_geo_geoobject.ident, 
    lizard_geo_geoobject.geometry, 
    lizard_area_area.area_class, 
    lizard_area_area.area_type, 
    lizard_area_communique."name",
    (lizard_geo_geoobject.id % 10) / 10.0 as random,
    (lizard_geo_geoobject.id % 10) / 10.0 as random1,
    (lizard_geo_geoobject.id % 10) / 10.0 as random2,
    (lizard_geo_geoobject.id % 10) / 10.0 as random3,
    (lizard_geo_geoobject.id % 10) / 10.0 as random4,
    (lizard_geo_geoobject.id % 5) - 2 as doel_result_map
  FROM 
    public.lizard_area_area, 
    public.lizard_area_communique, 
    public.lizard_geo_geoobject
  WHERE 
    lizard_area_area.communique_ptr_id = lizard_area_communique.geoobject_ptr_id AND
    lizard_area_communique.geoobject_ptr_id = lizard_geo_geoobject.id AND
    lizard_area_area.area_class = 2 AND
    GeometryType(lizard_geo_geoobject.geometry) in ('POLYGON', 'MULTIPOLYGON')
);

DROP VIEW IF EXISTS fews_locations;
CREATE VIEW fews_locations AS
(
  SELECT 
    geo.id, 
    geo.ident as geo_ident, 
    geo.geometry, 
    loc.data_set_id, 
    loc.fews_norm_source_id, 
    loc.shortname, 
    loc."name", 
    loc.icon, 
    loc.tooltip, 
    loc.active,
    par.ident as par_ident,
    (geo.id % 10) / 10.0 as random,
    (geo.id % 10) / 10.0 as random1,
    (geo.id % 10) / 10.0 as random2,
    (geo.id % 10) / 10.0 as random3,
    (geo.id % 10) / 10.0 as random4,
    (geo.id % 5) - 2 as doel_result_map
  FROM 
    public.lizard_geo_geoobject geo, 
    public.lizard_fewsnorm_geolocationcache loc, 
    public.lizard_fewsnorm_timeseriescache ser, 
    public.lizard_fewsnorm_parametercache par
  WHERE 
    loc.geoobject_ptr_id = geo.id AND
    ser.geolocationcache_id = loc.geoobject_ptr_id AND
    ser.parametercache_id = par.id
);

DROP VIEW IF EXISTS track_records;
CREATE VIEW track_records AS
(
  SELECT 
    * 
  FROM 
    public.lizard_geo_geoobject geo, 
    public.lizard_fewsnorm_trackrecordcache tra
  WHERE 
    tra.geoobject_ptr_id = geo.id
);

DROP VIEW IF EXISTS ekr_vis;
CREATE VIEW ekr_vis AS
(
  SELECT 
    avl."value", 
    geo.geometry,
    are.data_set_id
  FROM 
    public.lizard_area_area are, 
    public.lizard_geo_geoobject geo, 
    public.lizard_area_communique com, 
    public.lizard_layers_areavalue avl, 
    public.lizard_layers_valuetype vty
  WHERE 
    are.communique_ptr_id = com.geoobject_ptr_id AND
    geo.id = com.geoobject_ptr_id AND
    avl.area_id = are.communique_ptr_id AND
    avl.value_type_id = vty.id AND
    vty.name = 'EKR-VIS'
);

DROP VIEW IF EXISTS ekr_ovwflora;
CREATE VIEW ekr_ovwflora AS
(
  SELECT 
    avl."value", 
    geo.geometry,
    are.data_set_id
  FROM 
    public.lizard_area_area are, 
    public.lizard_geo_geoobject geo, 
    public.lizard_area_communique com, 
    public.lizard_layers_areavalue avl, 
    public.lizard_layers_valuetype vty
  WHERE 
    are.communique_ptr_id = com.geoobject_ptr_id AND
    geo.id = com.geoobject_ptr_id AND
    avl.area_id = are.communique_ptr_id AND
    avl.value_type_id = vty.id AND
    vty.name = 'EKR-OVWFLORA'
);

DROP VIEW IF EXISTS ekr_fytopl;
CREATE VIEW ekr_fytopl AS
(
  SELECT 
    avl."value", 
    geo.geometry,
    are.data_set_id
  FROM 
    public.lizard_area_area are, 
    public.lizard_geo_geoobject geo, 
    public.lizard_area_communique com, 
    public.lizard_layers_areavalue avl, 
    public.lizard_layers_valuetype vty
  WHERE 
    are.communique_ptr_id = com.geoobject_ptr_id AND
    geo.id = com.geoobject_ptr_id AND
    avl.area_id = are.communique_ptr_id AND
    avl.value_type_id = vty.id AND
    vty.name = 'EKR-FYTOPL'
);

DROP VIEW IF EXISTS ekr_mafauna;
CREATE VIEW ekr_mafauna AS
(
  SELECT 
    avl."value", 
    geo.geometry,
    are.data_set_id
  FROM 
    public.lizard_area_area are, 
    public.lizard_geo_geoobject geo, 
    public.lizard_area_communique com, 
    public.lizard_layers_areavalue avl, 
    public.lizard_layers_valuetype vty
  WHERE 
    are.communique_ptr_id = com.geoobject_ptr_id AND
    geo.id = com.geoobject_ptr_id AND
    avl.area_id = are.communique_ptr_id AND
    avl.value_type_id = vty.id AND
    vty.name = 'EKR-MAFAUNA'
);
