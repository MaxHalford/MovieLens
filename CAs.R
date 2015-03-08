library('FactoMineR')
library('ggplot2')

maxCA = function(tableName) {
  # Open the file
  pathToFile = paste('data', tableName, sep = '/')
  data = read.csv(pathToFile, head = TRUE)
  # Take the first column as the index
  rownames(data) = data[,1]
  data[,1] = NULL
  # Calculate the CA
  cA = CA(data, graph = FALSE)
  # Extract the cartesian coordinates of the CA for both variables
  obs1 = data.frame(cA$col$coord)
  obs2 = data.frame(cA$row$coord)
  # Plot the two first columns (contains most information)
  ggplot() +
    geom_text(data = obs1, aes(Dim.1, Dim.2), label = rownames(obs1), col = 'purple', hjust = 0, vjust = 0) +
    geom_point(data = obs1, aes(Dim.1, Dim.2), col = 'purple') +
    geom_text(data = obs2, aes(Dim.1, Dim.2), label = rownames(obs2), col = 'darkgreen', hjust = 0, vjust = 0) +
    geom_point(data = obs2, aes(Dim.1, Dim.2), col = 'darkgreen') +
    geom_hline(yintercept = 0, col = 'gray') +
    geom_vline(xintercept = 0, col = 'gray') +
    ggtitle(tableName)
  ggsave(file = paste('rapport/images', paste(tableName, 'png', sep = '.'), sep = '/'))
}   
# CA : Genre of a film vs. age of a user 
maxCA('M_genreVSage')
maxCA('F_genreVSage')
# CA : Genre of a film vs. occupation of a user 
maxCA('M_genreVSoccupation')
maxCA('F_genreVSoccupation')
# CA : Genre of a film vs. region of a user 
maxCA('M_genreVSregion')
maxCA('F_genreVSregion')
# CA : Release date of a film vs. age of a user 
maxCA('M_releaseVSage')
maxCA('F_releaseVSage')
# CA : Release date of a film vs. occupation of a user 
maxCA('M_releaseVSoccupation')
maxCA('F_releaseVSoccupation')
# CA : Release date of a film vs. region of a user 
maxCA('M_releaseVSregion')
maxCA('F_releaseVSregion')