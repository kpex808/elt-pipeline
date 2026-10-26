SELECT
  COUNT(*) AS n_approaches,
  MIN(dist_au) AS min_dist_au,
  ROUND(MIN(dist_au) * 149597870.7, 0) AS min_dist_km,
  MAX(v_rel_kms) AS max_speed_kms
FROM {{ ref('cad') }}
