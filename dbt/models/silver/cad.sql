SELECT
  json_extract_string(flyby, '$[0]') AS designation,
  json_extract_string(flyby, '$[3]') AS approach_at,
  json_extract(flyby, '$[4]')::DOUBLE AS dist_au,
  json_extract(flyby, '$[7]')::DOUBLE AS v_rel_kms
FROM {{ source('bronze', 'cad_raw') }} AS raw,
  UNNEST(CAST(json_extract(raw.payload, '$.data') AS JSON[])) AS u(flyby)
