# R script that plots a file using the following command line arguments :
# - directory
# - file name type (edges,intersections,vehicles,etc)
# - number of simulation files that are going to be in the graph
# - number of methods in the graph
# - column (if the file has more than one column)
# - name of the y axis


args<-commandArgs(trailingOnly=TRUE)
directory <- args[1]
fileType <- args[2]
simNumber <- as.integer(args[3])
methodNumber <- as.integer(args[4])
column <- as.integer(args[5])
yName <- args[6]
color<-rainbow(methodNumber,s=1,v=1,start=0,end=4/6,alpha=1)
foo <- seq(simNumber,1,by=-1)
for (j in 1:methodNumber){
  if (j==1) method <- 'fixed'
  else if (j==2) method <- 'selforg'
  else if (j==3) method <- 'prevcyc'
  else if (j==4) method <- 'queue'
  for (i in foo){
    if (i==simNumber && j==1){
      outfile<-sprintf("../graphs/%s/%s.pdf",directory,yName)
      pdf(outfile)
      infile<-sprintf("../output/%s/%s_%s_%i.txt",directory,fileType,method,i-1)
      table<-read.table(infile)
      result<-table[[column]]
      ymax <- max(result)*1.2
      xmax <- length(result)
      plot(result,type='l', xlab='Time',ylab=yName, col=color[j], ylim=c(0,ymax), xlim=c(0,xmax))
      if (methodNumber == 1) legend('topright',c('Fixed'))
      if (methodNumber == 2) legend('topright',c('Fixed','Selforg'), col=c(color[1],color[2]), lty=1)
    }
    infile<-sprintf("../output/%s/%s_%s_%i.txt",directory,fileType,method,i-1)
    table<-read.table(infile)
    result<-table[[column]]
    lines(result,col=color[j])
  }
}
print(sprintf("%s graph created",yName))