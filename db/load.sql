\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Category FROM 'Categories.csv' WITH DELIMITER ',' NULL '' CSV



\COPY Orders FROM 'Order.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_order_id_seq',
                         (SELECT MAX(order_id)+1 FROM Orders),
                         false);

\COPY Seller FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_product_id_seq',
                         (SELECT MAX(product_id)+1 FROM Products),
                         false);
                         
\COPY OrderDetails FROM 'Order_Details.csv' WITH DELIMITER ',' NULL '' CSV


\COPY ReviewProduct FROM 'ProductReviews.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ReviewSeller FROM 'SellerReviews.csv' WITH DELIMITER ',' NULL '' CSV


\COPY Inventory FROM 'Inventorys.csv' WITH DELIMITER ',' NULL '' CSV


\COPY CartItems FROM 'CartItems.csv' WITH DELIMITER ',' NULL '' CSV