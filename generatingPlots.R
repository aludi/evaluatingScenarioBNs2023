exp <- read_csv("~/simulationTest/exp.csv")
library(dplyr)
library(ggplot2)


prec <- filter(exp, strong == "strong")

# only look at outcome nodes for now
prec_lost <- filter(prec, hypNode == "lost_object")
prec_stolen <- filter(prec, hypNode == "successful_stolen")
#prec_stolen <- filter(prec_stolen, (distortion != "arbitraryRounded"))
#prec_stolen <- filter(prec_stolen, (distortion != "normalNoise"))
prec_stolen <- filter(prec_stolen, (distortion == "normalNoise"))

prec_stolen$param <- as.factor(prec_stolen$param)
                                            
prec_stolen$ev <- factor(prec_stolen$evidenceCUMUL, levels=c("no_evidence0", "E_object_is_gone1",
                                                             "E_broken_lock1", "E_disturbed_house1",
                                                             "E_s_spotted_by_house1", "E_s_spotted_with_goodie1",
                                                             "E_private0"))
#prec_stolen <- na.omit(prec_stolen)

prec_stolen$delta <- abs(as.double(prec_stolen$Probability) - as.double(prec_stolen$K2Probability))
View(prec_stolen)
#prec_stolen <- filter(prec_stolen, distortion == "E_private0") # all evidence is added




ggplot(data=prec_stolen, aes(x=ev,
                           y= delta, group=param)) +
   #facet_grid(distortion~., scales = "free_x") + 
   geom_point(aes(color=param)) + geom_line(aes(color=param)) + 
  theme(axis.text.x = element_text(angle = 60, hjust = 1)) +
  ggtitle("absolute difference in probabiltiy for successfull_stolen
          node between noisy and K2 BN.")

View(prec_stolen)

ggplot(data=prec_lost, aes(x=param,
                           y= Probability, group=distortion)) +
  facet_wrap(distortion ~ ., scales = "free_x") + 
  geom_point(aes(color=param))
