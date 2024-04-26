#######################################################
#                                                     #  
#   R script to draw circular barplots in MODELBARK   #
#                                                     #
#######################################################


##REQUIRED INFORMATION (Comment these lines with an initial # to run the test example below )
WD <- "PATH/TO/THE/WORKING/DIRECTORY" #Full route to the working directory storing ModelBark output
modelbark.output <- "OUTPUT-FILE-NAME.csv"
circular.plot.name <-"CIRCULAR-OUTPUT-PLOT-NAME.pdf"

##EXAMPLE (de-comment these lines with an initial # to run the test example)
#WD <- "D:/RMODELBARK" #Full route to the working directory storing ModelBark output
#modelbark.output <- "ModelBark-output-test.csv"
#circular.plot.name <-"ModelBark-output-test-circular_output.pdf"


#Setting the WD
setwd(WD)

############################################
#Load Dependencies
#install.packages("ggplot2", dependencies=TRUE)
library(ggplot2)
#install.packages("tidyverse")
library(tidyverse)
library(tidyr)
library(dplyr)
library(tibble)
########################################################################

#Manipulate ModelBark output to enhance visualization
#Some things to be considered:
#zeros are replaced by 0.1 so as not to be handled as missing data
#Vascular cambium (1) is changed to 30 to enable proper visualization
#Plotting more than 50 radii might be extremely time consuming


system(paste("sed -i 's/,/\t/g'", modelbark.output))
system(paste("sed -i 's/\t1\t/\t30\t/g'", modelbark.output))
system(paste("sed -i 's/\t0/\t0.1/g'", modelbark.output))
system(paste("sed -i 's/^0/0.1/g'", modelbark.output))


########################################################################

#Loading the output of ModelBark after modifications

#Loading modified ModelBark output as a data.frame
data.input <- read.table(modelbark.output,
                      header=FALSE,
                      sep="\t", 
                      dec=".")

# Creating a vector of col names
celdas <- vector(length = length(data.input[1,]), mode = "character")
for (i in 1:length(data.input[1,])) {
  celdas[i] <- paste0("cell", i)
}

# Creating a vector of row names
iterations <- vector(length = length(data.input[,1]), mode = "character")
for (i in 1:length(data.input[,1])) {
  iterations[i] <- paste0("ray", i)
}
#Giving col and row names to the data.frame
row.names(data.input) <- iterations
colnames(data.input) <- celdas

#Converting the data.frame into a matrix
data.input.m <- as.matrix(data.input)

df = data.frame(data.input.m) %>% 
  rownames_to_column("row") %>% 
  pivot_longer(-row) %>%
  mutate(name=factor(name,levels=colnames(data.input.m)),
         row=factor(row,levels=rownames(data.input.m)))

row_num = length(levels(df$row))

#Drawing the circular plot
pdf(circular.plot.name)
g = ggplot(df,aes(x=as.numeric(name),y=as.numeric(row),fill=value))+
  scale_fill_gradient2(low = "#075AFF",
                       mid = "#FFFFCC",
                       high = "black") + 
  xlim(c("",colnames(data.input.m))) + ylim(0,length(data.input$cell1))+
  geom_tile() +
  theme(legend.position = "none", axis.title = element_blank(), axis.text.y = element_blank())
g + coord_polar(theta="y") 
dev.off()
