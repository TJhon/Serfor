pacman::p_load(
  tidyverse, here
)

setwd("E:\\All\\Serfor\\data")

infractores = read_csv("raw/infractores_historial.csv", show_col_types = F)
infractores %>% 
  distinct(infractor, documento_identidad)
infractores_identificacion <- 
  infractores %>% 
  mutate(
    first_digit = str_sub(documento_identidad, 1, 1),
    len_doc = str_length(documento_identidad),
    is_ruc = as.integer(len_doc == 11),
    is_ruc_empresa = ifelse(first_digit == 2 & len_doc == 11, 1, 0),
    is_ruc_persona = ifelse(first_digit == 1 & len_doc == 11, 1, 0)
  ) %>% 
  arrange(desc(len_doc)) %>%
  # filter(is_ruc_persona == 1) %>%
  distinct(documento_identidad, infractor, len_doc, is_ruc,  is_ruc_empresa, is_ruc_persona) 

infractores_identificacion %>% 
  arrange(len_doc, infractor) %>% 
  write_csv("raw/infractores_unicos_identificados.csv")
infractores_identificacion %>% 
  filter(is_ruc_empresa==1)

infractores_identificacion %>% 
  filter(documento_identidad == '20477682632')
