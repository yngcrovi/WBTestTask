SELECT 
    -- Основная информация
    p.product_url as link_product,
    p.id AS atricul,
    p.name AS product_name,

    -- Цены 
    p.price_basic AS price_basic_rub,
    p.price_product AS price_current_rub,

    p.description as description,

    array_to_string(p.images, ', ') AS images,
    
    p.characteristics as characteristics,

    -- Продавец
    COALESCE(s.name, 'Неизвестный продавец') AS supplier_name,
    s.seller_url as seller_url,

    array_to_string(p.sizes, ', ') AS sizes,

  -- Остатки
    p.total_quantity,
    ARRAY_LENGTH(p.sizes, 1) AS sizes_count,

    -- Рейтинги и отзывы
    p.rating::float,
    p.feedbacks_count
    
FROM product.coat p
LEFT JOIN brand b ON p.brand_id = b.id
LEFT JOIN supplier s ON p.supplier_id = s.id
WHERE p.rating > 4.5 AND p.price_product < 10000
ORDER BY p.feedbacks_count DESC, p.rating DESC