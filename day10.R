
input <- c(79L,
           142L,
           139L,
           33L,
           56L,
           133L,
           138L,
           61L,
           125L,
           88L,
           158L,
           123L,
           65L,
           69L,
           105L,
           6L,
           81L,
           31L,
           60L,
           70L,
           159L,
           114L,
           71L,
           15L,
           13L,
           72L,
           118L,
           14L,
           9L,
           93L,
           162L,
           140L,
           165L,
           1L,
           80L,
           148L,
           32L,
           53L,
           102L,
           5L,
           68L,
           101L,
           111L,
           85L,
           45L,
           25L,
           16L,
           59L,
           131L,
           23L,
           91L,
           92L,
           115L,
           103L,
           166L,
           22L,
           145L,
           161L,
           108L,
           155L,
           135L,
           55L,
           86L,
           34L,
           37L,
           78L,
           28L,
           75L,
           7L,
           104L,
           121L,
           24L,
           153L,
           167L,
           95L,
           87L,
           94L,
           134L,
           154L,
           84L,
           151L,
           124L,
           62L,
           49L,
           38L,
           39L,
           54L,
           109L,
           128L,
           19L,
           2L,
           98L,
           122L,
           132L,
           141L,
           168L,
           8L,
           160L,
           50L,
           42L,
           46L,
           110L,
           12L,
           152L)


library(tidyverse)

# Part 1
input_diffs <- input %>%
  sort() %>%
  {c(0, . , tail(., 1) + 3)} %>%
  diff()

input_diffs %>% {sum(. == 1) * sum(. == 3)}

# Part 2

groups_of_ones <- input_diffs %>%
  as.character() %>%
  paste0(collapse = "") %>%
  str_split("3") %>%
  flatten_chr() %>%
  map_dbl(~str_length(.x))

groups_of_ones %>%
  {.[!(. == 0)]} %>% # remove the groups with zero ones
  {.[!(. == 1)]} %>% # remove the groups with one ones (can't be removed)
  {. - 1} %>% # can't remove the last one in a group, so subtract 1 to leave the removeable ones
  {2^. - ((.-2))*((.-2)+1)/2} %>% # see comment below
  prod() %>%
  formatC(format = "f", digits = 0)
  
# all the ones left you can remove or not as you wish (so 2^n combinations for each group
# BUT need a correction for when there are three or more ones together - you can't remove
# three ones in a row.  The number of ways of arranging three the sum of numbers up to n-2
# (I can show this graphically on paper, but hard to explain in a comment!). Since sum of 
# numbers up to m is m*(m+1)/2 then the correction is (n-2)*(n-1)/2

