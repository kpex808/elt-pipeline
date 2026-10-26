SELECT
  designation,
  approach_at,
  dist_au,
  ROUND(dist_au * 149597870.7, 0) AS dist_km,
  v_rel_kms,
  CASE
    WHEN dist_au < 0.01 THEN 'very close'
    WHEN dist_au < 0.03 THEN 'close'
    ELSE 'moderate'
  END AS closeness
FROM {{ ref('cad') }}
