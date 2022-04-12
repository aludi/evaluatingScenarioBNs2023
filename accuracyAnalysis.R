library(dplyr)
library(readr)
a_cg <- read_csv("simulationTest/CredibilityGameAccuracy.csv")
a_cg$experiment <- "CredibilityGame"
a_gm <- read_csv("simulationTest/GroteMarktAccuracy.csv")
a_gm$experiment <- "GroteMarkt"
a_sl <- read_csv("simulationTest/StolenLaptopAccuracy.csv")
a_sl$experiment <- "StolenLaptop"


df_a <- rbind(a_cg, a_gm)
df_a <- rbind(df_a, a_sl)

df_a$name <- gsub(".*0", "", df_a$network)
df_a$name <- gsub(".net", "", df_a$name)

b <- df_a %>%
  group_by(name, experiment) %>%
  summarize(acc = mean(matching), rms=mean(RMS), sdrms = sd(RMS),n = n())

View(b)