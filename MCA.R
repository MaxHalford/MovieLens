library('FactoMineR')
library('ggplot2')

# MCA on all the data
data = read.csv('data/categorized', head = TRUE)
# Only keep the relevant data
data = data[,c('gender', 'occupation', 'ageCategory', 'releaseDecade', 'region', 'genre')]
# Randomly sample the data (an MCA is a heavy calculation)
###data = data[sample(nrow(data), 2000),]
# Extract each category with the siez of its space
categories = apply(data, 2, function(x) nlevels(as.factor(x)))
# Compute the MCA
mca = MCA(data, graph = FALSE)
# Extract variables coordinates
variables = data.frame(mca$var$coord, Variable = rep(names(categories), categories))
# Extract observations coordinates
observations = data.frame(mca$ind$coord)
# Plot!
ggplot(observations,  aes(Dim.1, Dim.2)) +
  geom_hline(yintercept = 0, colour = "gray") +
  geom_vline(xintercept = 0, colour = "gray") +
  geom_point(colour = 'gray50', alpha = 0.7) +
  geom_density2d(colour = 'gray80') +
  geom_text(data = variables, aes(Dim.1, Dim.2, label = rownames(variables), colour = Variable)) +
  ggtitle("MCA plot")
#ggsave(file = "plots/mca.pdf")
