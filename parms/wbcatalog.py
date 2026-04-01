import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ─────────── Настройки ───────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
}

BASE_URL = "https://www.wildberries.ru/catalog/0/search.aspx"
session = requests.Session()
session.headers.update(HEADERS)

# ─────────── Получение HTML страницы ───────────
def get_search_page(query, page):
    params = {"search": query, "page": page}
    try:
        response = session.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        print(f"[!] Не удалось получить страницу {page}")
        return ""

# ─────────── Парсинг товаров с HTML ───────────
def parse_products(query, max_pages=3):
    all_products = []

    for page in range(1, max_pages + 1):
        print(f"Парсинг страницы {page}...")
        html = get_search_page(query, page)
        if not html:
            continue

        soup = BeautifulSoup(html, "lxml")
        items = soup.select("div.product-card")  # карточки товаров

        for item in items:
            try:
                # URL
                url_tag = item.select_one("a.ref_goods_n_p")
                url = "https://www.wildberries.ru" + url_tag["href"] if url_tag else ""

                # Название
                name_tag = item.select_one("span.goods-name")
                name = name_tag.get_text(strip=True) if name_tag else ""

                # Цена
                price_tag = item.select_one("span.lower-price")
                price = int(price_tag.get_text(strip=True).replace("₽", "").replace(" ", "")) if price_tag else 0

                # Рейтинг
                rating_tag = item.select_one("span.rating__value")
                rating = float(rating_tag.get_text(strip=True).replace(",", ".")) if rating_tag else 0.0

                # Кол-во отзывов
                reviews_tag = item.select_one("span.reviews-count")
                reviews_count = int(reviews_tag.get_text(strip=True).split()[0]) if reviews_tag else 0

                # Продавец
                seller_tag = item.select_one("a.seller-name")
                seller_name = seller_tag.get_text(strip=True) if seller_tag else ""
                seller_url = "https://www.wildberries.ru" + seller_tag["href"] if seller_tag else ""

                # Размеры
                sizes = ", ".join([s.get_text(strip=True) for s in item.select("div.j-size")])

                # Изображения
                images = ", ".join([img["src"] for img in item.select("img.preview") if img.get("src")])

                # Данные для фильтра
                product_data = {
                    "url": url,
                    "name": name,
                    "price": price,
                    "rating": rating,
                    "reviews_count": reviews_count,
                    "seller_name": seller_name,
                    "seller_url": seller_url,
                    "sizes": sizes,
                    "images": images,
                    "country": "Россия"  # Для теста можно оставить "Россия"
                }

                all_products.append(product_data)
            except Exception as e:
                print(f"[!] Ошибка при обработке товара: {e}")

        time.sleep(0.5)

    return all_products

# ─────────── Сохранение Excel ───────────
def save_to_excel(products):
    df = pd.DataFrame(products)

    # Гарантируем наличие всех нужных колонок
    for col in ["rating", "reviews_count", "price", "country"]:
        if col not in df.columns:
            df[col] = 0 if col != "country" else ""

    df.to_excel("catalog.xlsx", index=False)

    # Фильтрованные товары
    filtered = df[
        (df["rating"] >= 4.5) &
        (df["price"] <= 10000) &
        (df["country"] == "Россия")
    ]
    filtered.to_excel("filtered.xlsx", index=False)
    print(f"Всего товаров после фильтра: {len(filtered)}")

# ─────────── Точка входа ───────────
if __name__ == "__main__":
    query = "пальто из натуральной шерсти"
    products = parse_products(query, max_pages=3)
    save_to_excel(products)
    print("Готово! Файлы catalog.xlsx и filtered.xlsx созданы ✅")
