select count(t.id) from teachers t
LEFT JOIN assignments a ON t.id = a.teacher_id
WHERE a.grade = 'A' AND a.state = 'GRADED' AND a.teacher_id = '{teacher_id}'
GROUP BY t.id 