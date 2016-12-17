require("RPostgreSQL")
require("wordcloud")
require("reshape2")

# Establish Connection to Robin using RPostgreSQL
drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname = "analytics", host="10.223.192.6", port = "5432", user = "etl", password = "s0.Much.Data")

# Get Google Vision Labels
ga_labels <- dbGetQuery(con, "SELECT * FROM JT.Image_Label_Scores;")

# Get all Labels
ga_desc <- rbind(ga_labels$desc_one, ga_labels$desc_two, ga_labels$desc_three, ga_labels$desc_four, ga_labels$desc_five, ga_labels$desc_six, ga_labels$desc_seven, ga_labels$desc_eight, ga_labels$desc_nine, ga_labels$desc_ten)

# Wordcloud
wordcloud(ga_desc, max.words = 100, random.order = FALSE)


#wordcloud(, max.words = 100, random.order = FALSE)

# Disconnect from Robin
dbDisconnect(con)