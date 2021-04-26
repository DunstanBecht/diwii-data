CREATE TABLE TableC LIKE insee_StockEtablissement;

ALTER TABLE TableC ADD COLUMN (
mail VARCHAR(256),
name VARCHAR(200),
phone VARCHAR(20),
token VARCHAR(128),
lastSend DATETIME,
answerDate DATETIME,
opened DATETIME,
need VARCHAR(1),
unsubscribed VARCHAR(1),

answer1a VARCHAR(1),
answer1b VARCHAR(1),
answer1c VARCHAR(1),
answer1d VARCHAR(1),

answer2a VARCHAR(1),
answer2b VARCHAR(1),
answer2c VARCHAR(1),
answer2d VARCHAR(1),
answer2e VARCHAR(1),
answer2f VARCHAR(1),
answer2g VARCHAR(1),
answer2h VARCHAR(1),
answer2i VARCHAR(300),

answer3a VARCHAR(1),
answer3b VARCHAR(1),
answer3c VARCHAR(1),
answer3d VARCHAR(1),
answer3e VARCHAR(1),
answer3f VARCHAR(1),

answer4a VARCHAR(1),
answer4b VARCHAR(1),
answer4c VARCHAR(1),
answer4d VARCHAR(1),
answer4e VARCHAR(1),
answer4f VARCHAR(1),

answer5 VARCHAR(1),

answer6a VARCHAR(1),
answer6b VARCHAR(1),

answer7 VARCHAR(100)
);
