INSERT INTO `user` (`id`, `name`)
SELECT '{}', '{}'
WHERE NOT EXISTS(SELECT 1 FROM `user` WHERE `id` = '{}');
