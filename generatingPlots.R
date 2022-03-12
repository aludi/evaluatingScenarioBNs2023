
library(dplyr)
library(ggplot2)

exp <- read_csv("~/simulationTest/exp.csv")

exp$param <- as.factor(exp$param)

exp$ev <- factor(exp$evidenceCUMUL, levels=c("no_evidence0", "E_object_is_gone1",
                                                             "E_broken_lock1", "E_disturbed_house1",
                                                             "E_s_spotted_by_house1", "E_s_spotted_with_goodie1",
                                                             "E_private0"))


##### STRONG VIEW ######
prec <- filter(exp, strong == "strong")

# only look at outcome nodes for now
prec_lost <- filter(prec, hypNode == "lost_object")
prec_stolen <- filter(prec, hypNode == "successful_stolen")
#prec_stolen <- filter(prec_stolen, (distortion != "arbitraryRounded"))
#prec_stolen <- filter(prec_stolen, (distortion != "normalNoise"))
#prec_stolen <- filter(prec_stolen, (distortion == "normalNoise"))


#prec_stolen <- na.omit(prec_stolen)

prec_stolen$distortion <- factor(prec_stolen$distortion, levels=c("K2", "rounded","arbitraryRounded", "normalNoise"))
                                                             

prec_stolen$delta <- abs(as.double(prec_stolen$Probability) - as.double(prec_stolen$K2Probability))
prec_stolen$Probability <- as.double(prec_stolen$Probability)

View(prec_stolen)
#prec_stolen <- filter(prec_stolen, distortion == "E_private0") # all evidence is added



for(s in c("K2", "rounded", "arbitraryRounded", "normalNoise")){
  prec_stolen_x <- filter(prec_stolen, (distortion == s))
  title <- paste("Absolute probability of the successfull stolen node under", s)
  ggplot(data=prec_stolen_x, aes(x=ev,
                             y= Probability, group=param)) +
  geom_point(aes(color=param, shape=distortion)) + geom_line(aes(color=param)) + 
  ggtitle(title) +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 30, hjust = 1)) 
    
  f_name <- paste(s, "absolute.png", sep="")
  f_name <- paste("images/", f_name, sep="")
  
  ggsave(f_name, device="png", width=20, height=12, units="cm")

  title <- paste("Difference in probability of the successfull stolen node under", s)
  
   ggplot(data=prec_stolen_x, aes(x=ev,
                               y= delta, group=param)) +
    geom_point(aes(color=param, shape=distortion)) + geom_line(aes(color=param)) + 
    ggtitle(title) + 
     theme_bw() +
     theme(axis.text.x = element_text(angle = 30, hjust = 1)) 
     
    f_name <- paste(s, "delta.png", sep="")
    f_name <- paste("images/", f_name, sep="")
    
    ggsave(f_name, device="png", width=20, height=12, units="cm")
}


#### WEAK VIEW ######

weak <- filter(exp, strong == "weak")
weak_stolen <- filter(weak, hypNode == "successful_stolen")

for(s in c("K2", "rounded", "arbitraryRounded", "normalNoise")){
  weak_stolen_x <- filter(weak_stolen, (distortion == s))
  title <- paste("Winning hypothesis of the successfull stolen node under", s)
  ggplot(data=weak_stolen_x, aes(x=ev,
                               y= Probability, group=param)) +
  geom_point(aes(color=param, shape=distortion)) + geom_line(aes(color=param)) + 
    ggtitle(title) + 
    theme_bw() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) 
  
  f_name <- paste(s, "Weak.png", sep="")
  f_name <- paste("images/", f_name, sep="")
  
  ggsave(f_name, device="png", width=20, height=12, units="cm")

}



#####
ggplot(data=prec_stolen, aes(x=ev,
                           y= delta, group=param)) +
   facet_grid(distortion~., scales = "free_x") + 
   geom_point(aes(color=distortion)) + geom_line(aes(color=param)) + 
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) +
  ggtitle("absolute difference in probabiltiy for successfull_stolen
          node between noisy and K2 BN.")

View(prec_stolen)

ggplot(data=prec_lost, aes(x=param,
                           y= Probability, group=distortion)) +
  facet_wrap(distortion ~ ., scales = "free_x") + 
  geom_point(aes(color=param))
