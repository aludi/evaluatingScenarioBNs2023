#create Bayesian Networks

raw_data_file <- "GroteMarktPrivate.csv"# canonical 10000 runs experiment

# generated structure, generated probabilities
KB <- read_csv(raw_data_file)
factorKB <- data.frame(lapply(KB, factor))
bn_df <- data.frame(factorKB)
res <- hc(bn_df)
fitBN <- bn.fit(res, data=factorKB)
plot(res)
write.net("GG.net", fitBN)


# manual structure, generated probabilities
# get manual structure (created according to method described)
n <- read.net("BayesianNetworks/MD.net")
graphviz.plot(n)
x<- bn.net(n)
plot(x)
fittedbn <- bn.fit(x, data = factorKB)
write.net("MG.net", fittedbn)

