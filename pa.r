library(tidyverse)
library(lubridate)
library(readxl)

data <- read_excel("Online Retail (1).xlsx")

clean_data <- data %>%
  filter(!is.na(CustomerID)) %>%
  filter(Quantity > 0, UnitPrice > 0) %>%
  distinct()

summary_stats <- clean_data %>%
  summarise(
    mean_qty = mean(Quantity),
    median_qty = median(Quantity),
    sd_qty = sd(Quantity),
    mean_price = mean(UnitPrice),
    median_price = median(UnitPrice),
    sd_price = sd(UnitPrice)
  )
print(summary_stats)

clean_data <- clean_data %>%
  mutate(Revenue = Quantity * UnitPrice)

top_products <- clean_data %>%
  group_by(Description) %>%
  summarise(TotalQty = sum(Quantity)) %>%
  arrange(desc(TotalQty)) %>%
  slice(1:10)
print(top_products)

revenue_per_product <- clean_data %>%
  group_by(Description) %>%
  summarise(TotalRevenue = sum(Revenue)) %>%
  arrange(desc(TotalRevenue))
print(revenue_per_product)

monthly_revenue <- clean_data %>%
  mutate(Month = floor_date(InvoiceDate, "month")) %>%
  group_by(Month) %>%
  summarise(MonthlyRevenue = sum(Revenue))

ggplot(monthly_revenue, aes(x = Month, y = MonthlyRevenue)) +
  geom_line(color = "blue", size = 1) +
  labs(title = "Monthly Revenue Trend", x = "Month", y = "Revenue")

customer_orders <- clean_data %>%
  group_by(CustomerID) %>%
  summarise(Orders = n_distinct(InvoiceNo))

total_customers <- n_distinct(clean_data$CustomerID)
repeat_customers <- sum(customer_orders$Orders > 1)
repeat_pct <- (repeat_customers / total_customers) * 100

cat("Total customers:", total_customers, "\n")
cat("Repeat customers (%):", repeat_pct, "\n")

aov <- clean_data %>%
  group_by(InvoiceNo) %>%
  summarise(OrderValue = sum(Revenue)) %>%
  summarise(AOV = mean(OrderValue))
print(aov)

aov_country <- clean_data %>%
  group_by(Country, InvoiceNo) %>%
  summarise(OrderValue = sum(Revenue)) %>%
  summarise(AvgOrderValue = mean(OrderValue)) %>%
  arrange(desc(AvgOrderValue))
print(aov_country)

country_revenue <- clean_data %>%
  group_by(Country) %>%
  summarise(TotalRevenue = sum(Revenue)) %>%
  arrange(desc(TotalRevenue))
print(country_revenue)

top_countries <- clean_data %>%
  group_by(Country, InvoiceNo) %>%
  summarise(TransactionRevenue = sum(Revenue)) %>%
  summarise(AvgRevenue = mean(TransactionRevenue)) %>%
  arrange(desc(AvgRevenue)) %>%
  slice(1:5)
print(top_countries)

seasonal_performance <- clean_data %>%
  mutate(Month = month(InvoiceDate, label = TRUE)) %>%
  group_by(Month, Description) %>%
  summarise(TotalRevenue = sum(Revenue)) %>%
  arrange(desc(TotalRevenue))

top5_products <- top_products$Description[1:5]
ggplot(seasonal_performance %>% filter(Description %in% top5_products),
       aes(x = Month, y = TotalRevenue, color = Description, group = Description)) +
  geom_line(size = 1) +
  labs(title = "Seasonal Performance of Top 5 Products", x = "Month", y = "Revenue")