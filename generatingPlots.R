
library(dplyr)
library(ggplot2)

exp <- read_csv("~/simulationTest/expORG.csv")

exp$param <- as.factor(exp$param)

exp$ev <- factor(exp$evidenceCUMUL, levels=c("no_evidence0", "E_object_is_gone1",
                                                             "E_broken_lock1", "E_disturbed_house1",
                                                             "E_s_spotted_by_house1", "E_s_spotted_with_goodie1",
                                                             "E_private0"))


##### STRONG VIEW ######
prec <- filter(exp, strong == "strong")

# only look at outcome nodes for now

prec_stolen <- filter(prec, hypNode %in% c("successful_stolen" ,"lost_object"))

prec_stolen$distortion <- factor(prec_stolen$distortion, levels=c("K2", "rounded","arbitraryRounded", "normalNoise"))
                                                             

prec_stolen$delta <- abs(as.double(prec_stolen$Probability) - as.double(prec_stolen$K2Probability))
prec_stolen$Probability <- as.double(prec_stolen$Probability)

#prec_stolen <- filter(prec_stolen, distortion == "E_private0") # all evidence is added


prec_stolen$hypNode <- factor(prec_stolen$hypNode, levels=c("successful_stolen", "lost_object"))

for(s in c("K2", "rounded", "arbitraryRounded", "normalNoise")){
  prec_stolen_x <- filter(prec_stolen, (distortion == s))
  title <- paste("Absolute probability of the outcome nodes under", s)
  ggplot(data=prec_stolen_x, aes(x=ev,
                             y= Probability, group=param)) +
  geom_point(aes(color=param, shape=distortion)) + 
    facet_wrap(hypNode~.) +
    geom_line(aes(color=param), position=position_dodge(width=0.2)) + 
  ggtitle(title) +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 30, hjust = 1)) 
    
  f_name <- paste(s, "absolute.png", sep="")
  f_name <- paste("images/", f_name, sep="")
  
  ggsave(f_name, device="png", width=20, height=12, units="cm")

  title <- paste("Difference in probability of the outcome nodes under", s)
  
   ggplot(data=prec_stolen_x, aes(x=ev,
                               y= delta, group=param)) +
     facet_wrap(hypNode~.) +
    geom_point(aes(color=param, shape=distortion)) + 
     geom_line(aes(color=param), position=position_dodge(width=0.2)) + 
    ggtitle(title) + 
     theme_bw() +
     theme(axis.text.x = element_text(angle = 30, hjust = 1)) 
     
    f_name <- paste(s, "delta.png", sep="")
    f_name <- paste("images/", f_name, sep="")
    
    ggsave(f_name, device="png", width=20, height=12, units="cm")
}


#### WEAK VIEW ######

weak <- filter(exp, strong == "weak")
weak_stolen <- filter(weak, hypNode %in% c("successful_stolen" ,"lost_object"))
weak_stolen$hypNode <- factor(weak_stolen$hypNode, levels=c("successful_stolen", "lost_object"))
for(s in c("K2", "rounded", "arbitraryRounded", "normalNoise")){
  weak_stolen_x <- filter(weak_stolen, (distortion == s))
  title <- paste("Winning hypothesis of the outcome nodes under", s)
  ggplot(data=weak_stolen_x, aes(x=ev,
                               y= Probability, group=param)) +
    facet_wrap(hypNode~.) +
  geom_point(aes(color=param, shape=distortion)) + 
    geom_line(aes(color=param), position=position_dodge(width=0.2)) + 
    ggtitle(title) + 
    theme_bw() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) 
  
  f_name <- paste(s, "Weak.png", sep="")
  f_name <- paste("images/", f_name, sep="")
  
  ggsave(f_name, device="png", width=20, height=12, units="cm")

}



#####

spider <- read_csv("~/simulationTest/expSpider.csv")
#spider <- filter(spider, strong == "strong")

spider$param <- as.factor(spider$param)
spider$ev <- factor(spider$evidenceCUMUL, levels=c("no_evidence0", "E_object_is_gone1",
                                             "E_broken_lock1", "E_disturbed_house1",
                                             "E_s_spotted_by_house1", "E_s_spotted_with_goodie1",
                                             "E_private0"))

spider$distortion <- factor(spider$distortion, levels=c("K2", "arbitraryRounded"))
spider$delta <- abs(as.double(spider$Probability) - as.double(spider$K2Probability))
spider$ProbabilityD <- as.double(spider$Probability)

#prec_stolen <- filter(prec_stolen, distortion == "E_private0") # all evidence is added

spider$hypNode <- factor(spider$hypNode, levels=c("successful_stolen", "lost_object"))

s <- "arbitraryRounded"
spider_x <- filter(spider, strong == "strong")


    title <- paste("Spider Absolute probability of the outcome nodes under", s)
    ggplot(data=spider_x, aes(x=ev,y= ProbabilityD, group=param)) +
      geom_point(aes(color=param, shape=distortion)) + 
      facet_grid(distortion ~ hypNode) +
      geom_line(aes(color=param)) + 
      ggtitle(title) +
      theme_bw() +
      theme(axis.text.x = element_text(angle = 30, hjust = 1)) 
    
    f_name <- paste(s, "spider.png", sep="")
    f_name <- paste(x, f_name, sep="")
    f_name <- paste("images/", f_name, sep="")
    
    ggsave(f_name, device="png", width=20, height=12, units="cm")
    
    title <- paste("Difference in probability of the outcome nodes under", s)
    
    ggplot(data=spider_x, aes(x=ev,
                                   y= delta, group=param)) +
      facet_grid(distortion ~ hypNode) +
      geom_point(aes(color=param, shape=distortion)) + 
      geom_line(aes(color=param), position=position_dodge(width=0.2)) + 
      ggtitle(title) + 
      theme_bw() +
      theme(axis.text.x = element_text(angle = 30, hjust = 1)) 
    
    f_name <- paste(s, "deltaSpider.png", sep="")
    f_name <- paste("images/", f_name, sep="")
    
    ggsave(f_name, device="png", width=20, height=12, units="cm")
    

weak <- filter(spider, strong == "weak")
weak_stolen <- filter(weak, hypNode %in% c("successful_stolen" ,"lost_object"))
weak_stolen$hypNode <- factor(weak_stolen$hypNode, levels=c("successful_stolen", "lost_object"))

weak_stolen_x <- filter(weak_stolen, (distortion == s))
title <- paste("Winning hypothesis of the outcome nodes under", s)
ggplot(data=weak_stolen, aes(x=ev,
                               y= Probability, group=param)) +
  facet_grid(distortion ~ hypNode) +
  geom_point(aes(color=param, shape=distortion)) + 
  geom_line(aes(color=param), position=position_dodge(width=0.2)) + 
  ggtitle(title) + 
  theme_bw() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) 

f_name <- paste(s, "WeakSpider.png", sep="")
f_name <- paste("images/", f_name, sep="")

ggsave(f_name, device="png", width=20, height=12, units="cm")
  


####### CREDIBILITY GAME ############

df <- read_csv("~/simulationTest/cred.csv")

df$param <- as.factor(df$param)

df$ev <- factor(df$evidenceCUMUL, levels=c("no_evidence0", "E_0_says_stolen1",
                                                   "E_1_says_stolen1",
                                                   "E_2_says_stolen1",
                                                   "E_3_says_stolen1",
                                                   "E_4_says_stolen1",
                                                   "E_5_says_stolen1",
                                                   "E_6_says_stolen1",
                                                   "E_7_says_stolen1",
                                                   "E_8_says_stolen1"))

df$distortion <- factor(df$distortion, levels=c("K2", "arbitraryRounded"))
df$delta <- abs(as.double(df$Probability) - as.double(df$K2Probability))
df$ProbabilityD <- as.double(df$Probability)


df$hypNode <- factor(df$hypNode, levels=c("agent_steals"))

s <- "arbitraryRounded"
df_x <- filter(df, strong == "strong")


title <- paste("Credibility Game Absolute probability of the outcome nodes under", s)
ggplot(data=df_x, aes(x=ev,y=ProbabilityD, group=param)) +
  geom_point(aes(color=param, shape=distortion)) + 
  facet_grid(distortion ~ hypNode) +
  geom_line(aes(color=param)) + 
  ggtitle(title) +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) 

f_name <- paste(s, "cred.png", sep="")
f_name <- paste(x, f_name, sep="")
f_name <- paste("images/", f_name, sep="")

ggsave(f_name, device="png", width=20, height=12, units="cm")

title <- paste("Credibility Game Difference in probability of the outcome nodes under", s)

ggplot(data=df_x, aes(x=ev,
                          y= delta, group=param)) +
  facet_grid(distortion ~ hypNode) +
  geom_point(aes(color=param, shape=distortion)) + 
  geom_line(aes(color=param), position=position_dodge(width=0.2)) + 
  ggtitle(title) + 
  theme_bw() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) 

f_name <- paste(s, "deltaCred.png", sep="")
f_name <- paste("images/", f_name, sep="")

ggsave(f_name, device="png", width=20, height=12, units="cm")




#####  Other
weak <- filter(df, strong == "weak")
weak_stolen <- filter(weak, hypNode %in% c("agent_steals"))
weak_stolen$hypNode <- factor(weak_stolen$hypNode, levels=c("successful_stolen", "lost_object"))

weak_stolen_x <- filter(weak_stolen, (distortion == s))
title <- paste("Winning hypothesis of the outcome nodes under", s)
ggplot(data=weak_stolen, aes(x=ev,
                             y= Probability, group=param)) +
  facet_grid(distortion ~ hypNode) +
  geom_point(aes(color=param, shape=distortion)) + 
  geom_line(aes(color=param), position=position_dodge(width=0.2)) + 
  ggtitle(title) + 
  theme_bw() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) 

f_name <- paste(s, "WeakSpider.png", sep="")
f_name <- paste("images/", f_name, sep="")

ggsave(f_name, device="png", width=20, height=12, units="cm")




