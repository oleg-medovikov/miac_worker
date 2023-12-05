select al.*, dubli.[Количество дублей]
from
(
select 
	F.[Медицинская организация],F.[Принадлежность],F.[Тип организации]
	,count(*) as 'Всего записей'
	,count (distinct P.Gid) as 'Уникальных пациентов'
	from robo.v_FedReg F left join cv_Patient P on(F.idPatient = P.idPatient)
group by F.[Медицинская организация],F.[Принадлежность],F.[Тип организации]
) as al
left join (
 select d.[Медицинская организация], count(d.[GID]) as 'Количество дублей'
	from (
	SELECT
		F.[Медицинская организация]
		,10* DATEPART(year, F.[Диагноз установлен]) + DATEPART(q, F.[Диагноз установлен]) as 'квартал'
		,P.[GID]
		,sum(case when F.[СНИЛС] = 'Не идентифицирован' then -1 else 0 end) as 'снилс'
		,count (distinct F.[УНРЗ]) as 'дубли'
		from robo.v_FedReg F left join cv_Patient P on(F.idPatient = P.idPatient)
		GROUP BY 
				F.[Медицинская организация]
				,10* DATEPART(year, F.[Диагноз установлен]) + DATEPART(q, F.[Диагноз установлен])
				,P.[GID] 
		having  (
			sum(case when F.[СНИЛС] = 'Не идентифицирован' then -1 else 0 end) < 0
			and count(distinct F.[УНРЗ]) > 1
			)
		) as d
group by d.[Медицинская организация]
) as dubli
on (al.[Медицинская организация] = dubli.[Медицинская организация] )
