# R script that plots a file using the following command line arguments :
# - directory
# - file name
# - type (label for the y axe)
# - column (if the file has more than one column)


args<-commandArgs(trailingOnly=TRUE)
directory <- args[1]
fileName <- args[2]
type<-args[3]
column <- as.integer(args[4])
infile<-sprintf("../output/%s/%s",directory,fileName)
outName<-unlist(strsplit(fileName,"[.]"))[1]
if (basename(getwd()) != 'graphs'){ 
outfile<-sprintf("../graphs/%s/%s_%s.pdf",directory,type,outName)
} else{ 
outfile<-sprintf("%s/%s_%s.pdf",directory,type,outName)
}
pdf(outfile)
table<-read.table(infile)
result<-table[[column]]
plot(result,type='l', xlab='Time',ylab=type, col='red')
dev.off()
