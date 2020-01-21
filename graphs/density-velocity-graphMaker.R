# R script that plots a file using the following command line arguments :
# - directory
# - number of simulation files that are going to be in the graph
# - number of methods in the graph
# - name of the y axis


args<-commandArgs(trailingOnly=TRUE)
directory <- args[1]
simNumber <- as.integer(args[2])
methodNumber <- as.integer(args[3])
color<-rainbow(methodNumber,s=1,v=1,start=0,end=4/6,alpha=1)
for (j in 1:methodNumber){
  if (j==1){
    method <- 'fixed'
    outfile<-sprintf("../graphs/%s/Density-Velocity.pdf",directory)
    pdf(outfile)
  }
  else if (j==2) method <- 'selforg'
  else if (j==3) method <- 'prevcyc'
  else if (j==4) method <- 'queue'
  for (i in 30:simNumber){
    infile<-sprintf("../output/%s/vehicles_total_%s_%i.txt",directory,method,i-1)
    table<-read.table(infile)
    xtemp<-table[[1]]
    ytemp<-table[[2]]
    if (i==30){
      xvector <- mean(xtemp)
      yvector <- mean(ytemp)
    } else{
      xvector <- c(xvector,mean(xtemp))
      yvector <- c(yvector,mean(ytemp))
    }
  }
  if (j==1){
    plot(xvector,yvector,type='p', xlab='Density',ylab='Velocity', col=color[j], xlim=c(0,0.30), ylim=c(0,8.75))
    if (methodNumber == 1) legend('topright',c('Fixed'))
    if (methodNumber == 2) legend('topright',c('Fixed','Selforg'), col=c(color[1],color[2]), lty=1)
  }
  else points(xvector,yvector,col=color[j])
  print(xvector)
  print(yvector)
}
print(sprintf("Density-Velocity graph created"))