
# Shopify Data Science Intern Challenge (2022)

My submission for Shopify's Data Science Intern challenge.

`question_1.py` contains the solutions for Question 1, and `question_2.txt` contains 
the answers to Question 2. For convenience's sake, the answers are also present below.

## Question 1
> On Shopify, we have exactly 100 sneaker shops, and each of these shops sells only one 
> model of shoe. We want to do some analysis of the average order value (AOV). 
> When we look at orders data over a 30 day window, we naively calculate an AOV of $3145.13. 
> Given that we know these shops are selling sneakers, a relatively affordable item, 
> something seems wrong with our analysis. 

**a) Think about what could be going wrong with our calculation. Think about a better way to evaluate this data.**

When trying to recreate this calculation, it is found that this AOV is naively calculated as the mean of all order values.
This can cause errors with outliers, which are not accounted for in a simple mean function.

A calculation which will more accurately represent the data will have to be performed after removing outliers, and then
calculating the mean. This new value is calculated to be `$302.58`, which is a much more reasonable value.

**b) What metric would you report for this dataset?**

One of the biggest concerns a seller has to deal with is item pricing. There is usually a "sweet spot", a range where an item's price results in the highest revenue generated. Thus, item price vs. revenue data is invaluable to a seller. Since the question is asking for a specific numeric value, the metric reported could be the optimal item pricing.

**c) What is its value?**

After using data smoothing methods, the optimal item price (the one that generated the largest amount of revenue in the dataset) is calculated to be `$155.00`

## Question 2
> For this question you’ll need to use SQL. Follow this link to access the data set required for the challenge. Please use  queries to answer the following questions. Paste your queries along with your final numerical answers below.

**a) How many orders were shipped by Speedy Express in total?**

*SQL query:*
```SQL
SELECT COUNT(*) FROM Orders WHERE ShipperID=(
SELECT ShipperID FROM Shippers WHERE ShipperName="Speedy Express");
```

*Numerical answer:* `54`

**b) What is the last name of the employee with the most orders?**

*SQL query:*
```SQL
SELECT LastName FROM Employees WHERE EmployeeID=(SELECT EmployeeID FROM(
SELECT EmployeeID, COUNT(EmployeeID) as "EmployeeIDCount" FROM
Orders GROUP BY EmployeeID ORDER BY "EmployeeIDCount" DESC) LIMIT 1);
```

*Numerical answer:* `Peacock`

**c) What product was ordered the most by customers in Germany?**

*SQL query:*
```SQL
SELECT ProductName FROM Products WHERE ProductID=(
SELECT ProductID FROM (SELECT ProductID,COUNT(ProductID) as "ProductIDCount" FROM(
SELECT ProductID FROM OrderDetails WHERE OrderID IN(
SELECT OrderID from Orders WHERE CustomerID IN(
SELECT CustomerID from Customers WHERE Country='Germany')))
GROUP BY ProductID ORDER BY "ProductIDCount" DESC) LIMIT 1)
```

*Numerical answer:* `Gorgonzola Telino`
