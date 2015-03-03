library('FactoMineR')

# CA : Genre of a film vs. age of a user 
genreVSage = read.csv('data/genreVSage', head = TRUE)
rownames(genreVSage) = genreVSage[,1]
genreVSage[,1] = NULL
CA(genreVSage)

# CA : Genre of a film vs. gender of a user 
genreVSgender = read.csv('data/genreVSgender', head = TRUE)
rownames(genreVSgender) = genreVSgender[,1]
genreVSgender[,1] = NULL
CA(genreVSgender)

# CA : Genre of a film vs. occupation of a user 
genreVSoccupation = read.csv('data/genreVSoccupation', head = TRUE)
rownames(genreVSoccupation) = genreVSoccupation[,1]
genreVSoccupation[,1] = NULL
CA(genreVSoccupation)

# CA : Genre of a film vs. state of a user 
genreVSstate = read.csv('data/genreVSstate', head = TRUE)
rownames(genreVSstate) = genreVSstate[,1]
genreVSstate[,1] = NULL
CA(genreVSstate)

# CA : Release date of a film vs. age of a user 
releaseVSage = read.csv('data/releaseVSage', head = TRUE)
rownames(releaseVSage) = releaseVSage[,1]
releaseVSage[,1] = NULL
CA(releaseVSage)

# CA : Release date of a film vs. gender of a user 
releaseVSgender = read.csv('data/releaseVSgender', head = TRUE)
rownames(releaseVSgender) = releaseVSgender[,1]
releaseVSgender[,1] = NULL
CA(releaseVSgender)

# CA : Release date of a film vs. occupation of a user 
releaseVSoccupation = read.csv('data/releaseVSoccupation', head = TRUE)
rownames(releaseVSoccupation) = releaseVSoccupation[,1]
releaseVSoccupation[,1] = NULL
CA(releaseVSoccupation)

# CA : Release date of a film vs. state of a user 
releaseVSstate = read.csv('data/releaseVSstate', head = TRUE)
rownames(releaseVSstate) = releaseVSstate[,1]
releaseVSstate[,1] = NULL
CA(releaseVSstate)

