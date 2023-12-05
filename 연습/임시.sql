-- 두개 사이거리 구하기
-- 아파트와 학교 사이가 500미터 이하인 아파트찾기

SELECT A.SCHOOLNM, B.APTNM, sqrt(Power((A.T_X - B.T_X), 2) + Power((A.T_y - B.T_y), 2)) AS distance 
FROM TB_SCHOOCL_JOB A, TB_APTLIST_JOB B
WHERE A.T_X - B.T_X BETWEEN -500 AND 500
  AND A.T_y - B.T_y BETWEEN -500 AND 500
  AND Power((A.T_X - B.T_X), 2) + Power((A.T_y - B.T_y), 2) <= 250000
