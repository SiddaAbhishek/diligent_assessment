SELECT
    o.order_id,
    u.name AS user_name,
    SUM(oi.quantity * p.price) AS total_order_value,
    pay.status AS payment_status
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN payments pay ON pay.order_id = o.order_id
GROUP BY o.order_id, u.name, pay.status;
