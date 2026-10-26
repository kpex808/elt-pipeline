SELECT
  strptime(approach_at, '%Y-%b-%d %H:%M')::DATE AS approach_day,
  COUNT(*) AS n_approaches,
  MIN(dist_au) AS min_dist_au
FROM {{ ref('cad') }}
GROUP BY 1
