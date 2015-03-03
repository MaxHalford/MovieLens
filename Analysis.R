library('FactoMineR')

# CA : Age of a user vs. release date of a film
ageVSgenre = read.csv('data/ageVSrelease', head = TRUE)
rownames(ageVSgenre) = ageVSgenre[,1]
ageVSgenre[,1] = NULL
CA(ageVSgenre)

# CA : Occupation of a user vs. genre of a film 
occupationVSgenre = read.csv('data/occupationVSgenre', head = TRUE)
rownames(occupationVSgenre) = occupationVSgenre[,1]
occupationVSgenre[,1] = NULL
CA(occupationVSgenre)

# MCA : all the data
data = read.csv('data/categorized', head = TRUE)
a=MCA(data)
