/*------- FIRST STEP (inserting objects fields as PARENT) -------*/

INSERT INTO `object`(`entry`, `scale_x`)
SELECT entry, scale_x FROM `world`.`creature` c

INNER JOIN `wowdb_world`.`unit_template` u ON c.id = u.entry

WHERE position_x <= (SELECT x1 FROM `wowdb_world`.`region` WHERE region_id = 141) AND position_x >= (SELECT x2 FROM `wowdb_world`.`region` WHERE region_id = 141) AND position_y <= (SELECT y1 FROM `wowdb_world`.`region` WHERE region_id = 141) AND
position_y >= (SELECT y2 FROM `wowdb_world`.`region` WHERE region_id = 141)

AND

c.id IN ( 883, 890, 1984, 1985, 1986, 1988, 1989, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2004, 2008, 2009, 2010, 2021, 2022, 2025, 2030, 2031, 2032, 2033, 2034, 2038, 2039, 2041, 2042, 2043, 2077, 2078, 2079, 2080, 2083, 2150, 2151, 2152, 2155, 2166, 2852, 3514, 3515, 3517, 3519, 3567, 3568, 3569, 3592, 3593, 3595, 3596, 3597, 3598, 3599, 3601, 3602, 3603, 3604, 3605, 3606, 3607, 3608, 3613, 3614, 3681, 4262, 4265, 6094, 6128, 6286, 6287, 6736, 6909, 7234, 7235, 7313, 7317, 7318, 7319, 7916, 8583, 8584, 10051, 10118, 11942, 12429, 25009, 25010, 25011, 25014, 25050, 25051, 25053, 25962, 26401 )

ORDER BY `c`.`id` ASC;

/*------- SECOND STEP (inserting basic stats for UNITS) -------*/
INSERT INTO `wowdb_realm`.`unit`(id, unit_flags, display_id, native_display_id, faction_template, min_damage, max_damage, resistance_fire, resistance_nature, resistance_frost, resistance_shadow, resistance_arcane, armor, attack_power, unit_template_id, region_id)

SELECT o.id, unit_flags, display_id_1 as display_id, display_id_1 as native_display_id, faction_template, min_damage, max_damage, resistance_fire, resistance_nature, resistance_frost, resistance_shadow, resistance_arcane, armor, melee_attack_power as attack_power, u.id as unit_template_id, (select id from `wowdb_world`.`region` WHERE region_id = 141) as region_id from `wowdb_realm`.`object` o

INNER JOIN `wowdb_world`.`unit_template` u ON o.entry = u.entry

WHERE o.id >= LAST_INSERT_ID();

/*------- THIRD STEP (updating coords and rest of stats for UNITS) -------*/
INSERT INTO `wowdb_realm`.`unit` (id, health, max_health, base_health, mana, max_mana, base_mana, level, x, y, z, orientation, map_id)

SELECT @rownum := @rownum + 1 as 'id', health, health as max_health, health as base_health, mana, mana as max_mana, mana as base_mana, level, position_x as x, position_y as y, position_z as z, orientation, map as map_id FROM `world`.`creature` c

INNER JOIN
(SELECT entry, FLOOR(min_health + RAND() * max_health) as health,
    FLOOR(min_mana + RAND() * max_mana) as mana,
    FLOOR(min_level + RAND() * max_level) as level FROM `wowdb_world`.`unit_template`) ut ON c.id = ut.entry, (select @rownum := LAST_INSERT_ID()) r

WHERE position_x <= (SELECT x1 FROM `wowdb_world`.`region` WHERE region_id = 141) AND position_x >= (SELECT x2 FROM `wowdb_world`.`region` WHERE region_id = 141) AND position_y <= (SELECT y1 FROM `wowdb_world`.`region` WHERE region_id = 141) AND
position_y >= (SELECT y2 FROM `wowdb_world`.`region` WHERE region_id = 141)

AND

c.id IN ( SELECT entry FROM `wowdb_realm`.`object` WHERE id >= LAST_INSERT_ID() )

ON DUPLICATE KEY UPDATE health=VALUES(health), max_health=VALUES(max_health), base_health=VALUES(base_health), mana=VALUES(mana), max_mana=VALUES(max_mana), base_mana=VALUES(base_mana), level=VALUES(level), x=VALUES(x), y=VALUES(y), z=VALUES(z), orientation=VALUES(orientation), map_id=VALUES(map_id)