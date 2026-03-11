CREATE SCHEMA product;

-- Отдельная таблица для селлеров
CREATE TABLE supplier (
    id int PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    seller_url VARCHAR(255) GENERATED ALWAYS AS ('https://www.wildberries.ru/seller/' || id) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Отдельная таблица для бренда
CREATE TABLE brand (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product.coat (
    -- Первичный ключ и основные идентификаторы
    id BIGINT PRIMARY KEY,                    -- Артикул товара (он же первичный ключ)
    supplier_id INT NOT NULL,                  -- ID селлера для связи
    
    -- Основная информация (с ограничениями по длине)
    name VARCHAR(500) NOT NULL,                -- Название товара (достаточно 500 символов)
    description TEXT,                          -- Описание (может быть длинным)
    brand_id INT NOT NULL,                     -- Бренд
    
    -- Цены (храним в копейках, чтобы избежать проблем с плавающей точкой)
    price_basic INT,                            -- Базовая цена в копейках
    price_product INT,                          -- Цена со скидкой в копейках
    
    -- Ссылки
    product_url VARCHAR(255) GENERATED ALWAYS AS ('https://www.wildberries.ru/catalog/' || id || '/detail.aspx') STORED,  
    
    -- Изображения (JSON формат для гибкости)
    images TEXT[],                                -- Массив ссылок на изображения
    
    -- Характеристики (вся структура в JSONB для сохранения оригинальной структуры)
    characteristics JSONB NOT NULL DEFAULT '{}'::jsonb, 
    
    -- Размеры и остатки
    sizes TEXT[],                                 -- Массив размеров
    total_quantity INT DEFAULT 0,                 -- Общее количество остатков
    
    -- Рейтинги и отзывы
    rating NUMERIC(3,2),                          -- Рейтинг (до 5.00)
    feedbacks_count INT DEFAULT 0,                -- Количество отзывов
    
    -- Метаданные
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Индексы для быстрого поиска
    CONSTRAINT fk_supplier FOREIGN KEY (supplier_id) REFERENCES supplier(id) ON DELETE SET NULL,
    CONSTRAINT fk_brand FOREIGN KEY (brand_id) REFERENCES brand(id) ON DELETE SET NULL,
    CONSTRAINT rating_range CHECK (rating >= 0 AND rating <= 5),
    CONSTRAINT positive_prices CHECK (price_basic >= 0 AND price_product >= 0)
);

-- Индексы для ускорения запросов
CREATE INDEX idx_coat_supplier ON product.coat(supplier_id);
CREATE INDEX idx_coat_brand ON product.coat(brand_id);
CREATE INDEX idx_coat_rating ON product.coat(rating DESC);
CREATE INDEX idx_coat_price ON product.coat(price_product);
CREATE INDEX idx_coat_feedbacks ON product.coat(feedbacks_count DESC);

-- Gin индекс для поиска по JSONB
CREATE INDEX idx_coat_characteristics ON product.coat USING GIN (characteristics);
CREATE INDEX idx_coat_sizes ON product.coat USING GIN (sizes);

-- Триггер для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_update_product_coat
    BEFORE UPDATE ON product.coat
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Комментарии к колонкам для документации
-- COMMENT ON TABLE product.coat IS 'Товары с Wildberries';
-- COMMENT ON COLUMN product.coat.id IS 'Артикул товара';
-- COMMENT ON COLUMN product.coat.price_basic IS 'Цена в копейках (базовая)';
-- COMMENT ON COLUMN product.coat.price_product IS 'Цена в копейках (со скидкой)';
-- COMMENT ON COLUMN product.coat.images IS 'Массив ссылок на изображения';
-- COMMENT ON COLUMN product.coat.characteristics IS 'Все характеристики товара в оригинальной структуре';
-- COMMENT ON COLUMN product.coat.sizes IS 'Массив доступных размеров';
-- COMMENT ON COLUMN product.coat.sizes_quantity IS 'Детализация остатков по размерам';