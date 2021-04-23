DROP TABLE IF EXISTS survey;

CREATE TABLE survey AS SELECT siren, Email AS mail, NomdelentrepriseLatinalphabet AS name, SUBSTRING(activitePrincipaleEtablissement, 1, 2) as division
FROM (
  SELECT *
  FROM Orbis_2021_02_18
  INNER JOIN Insee_StockEtablissement_Filtered
  ON Orbis_2021_02_18.AutreNdegdidentificationdelentreprise = Insee_StockEtablissement_Filtered.siren
  ORDER BY siren ASC, etablissementSiege DESC
) AS t
WHERE Email NOT LIKE ''
GROUP BY siren;

ALTER TABLE survey ADD COLUMN (
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

UPDATE Survey
SET token = MD5(RAND());
