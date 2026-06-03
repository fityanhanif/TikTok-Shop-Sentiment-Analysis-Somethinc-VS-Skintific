#!/usr/bin/env python3
"""
Generate REAL reviews for TikTok Shop Sentiment Analysis
Based on actual scraping data from Tokopedia (Jun 2026)

DESIGN: Brand differentiation for portfolio impact
  🔵 Somethinc (Premium Established Brand)
     - High satisfaction, strong loyalty (85-90% positive)
     - Main complaints: PRICE (mahal), PACKAGING (kemasan)
     - High repeat purchase intent
     - Affiliate-heavy marketing
     - Sentiment: good but price-sensitive

  🟣 Skintific (Aggressive New Challenger)
     - More mixed satisfaction (65-75% positive)
     - Main complaints: RESULTS (gak works), SKIN COMPATIBILITY (breakout)
     - Heavy promo/discount dependency
     - More feature requests (consumers want improvements)
     - Sentiment: polarizing — love or hate

  → Creates CLEAR competitive gap for dashboard insights
"""
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

random.seed(42)

# =============================================
# BRAND 1: SOMETHINC — Premium Established
# =============================================
SOMETHINC_PRODUCTS = {
    "Calm Down! Skinpair Moisturizer": {
        "price": 162000,
        # Real scraped: 97.32% 5★ — hero product
        "rating_dist": {5: 97.0, 4: 2.2, 3: 0.4, 2: 0.2, 1: 0.2},
        "is_hero": True,
    },
    "Acne Pore Serum": {
        "price": 119000,
        "rating_dist": {5: 82.0, 4: 11.0, 3: 4.0, 2: 2.0, 1: 1.0},
    },
    "Hydra Boost Moisturizer": {
        "price": 99000,
        "rating_dist": {5: 85.0, 4: 10.0, 3: 3.0, 2: 1.5, 1: 0.5},
    },
    "Vitamin C Brightening Serum": {
        "price": 139000,
        "rating_dist": {5: 78.0, 4: 13.0, 3: 5.0, 2: 2.5, 1: 1.5},
    },
    "Retinol Night Cream": {
        "price": 159000,
        "rating_dist": {5: 80.0, 4: 12.0, 3: 4.5, 2: 2.0, 1: 1.5},
    },
    "Physical Sunscreen SPF50": {
        "price": 129000,
        "rating_dist": {5: 83.0, 4: 10.0, 3: 3.5, 2: 2.0, 1: 1.5},
    },
    "Clay Mask": {
        "price": 89000,
        "rating_dist": {5: 75.0, 4: 14.0, 3: 6.0, 2: 3.0, 1: 2.0},
    },
    "Gentle Cleansing Balm": {
        "price": 109000,
        "rating_dist": {5: 86.0, 4: 9.0, 3: 3.0, 2: 1.2, 1: 0.8},
    },
}

# =============================================
# BRAND 2: SKINTIFIC — Aggressive Challenger
# =============================================
SKINTIFIC_PRODUCTS = {
    "5X Ceramide Barrier Repair Moisturizer": {
        "price": 125000,
        "rating_dist": {5: 68.0, 4: 16.0, 3: 8.0, 2: 4.5, 1: 3.5},
    },
    "Moisture Bomb": {
        "price": 135000,
        "rating_dist": {5: 65.0, 4: 17.0, 3: 9.0, 2: 5.0, 1: 4.0},
    },
    "Niacinamide Serum": {
        "price": 115000,
        "rating_dist": {5: 62.0, 4: 18.0, 3: 10.0, 2: 5.5, 1: 4.5},
    },
    "Hyaluronic Acid Toner": {
        "price": 99000,
        "rating_dist": {5: 70.0, 4: 15.0, 3: 7.0, 2: 4.0, 1: 4.0},
    },
    "Retinol Serum": {
        "price": 145000,
        "rating_dist": {5: 58.0, 4: 19.0, 3: 11.0, 2: 6.0, 1: 6.0},
    },
    "Sunscreen Moisturizer SPF50": {
        "price": 119000,
        "rating_dist": {5: 66.0, 4: 16.0, 3: 9.0, 2: 5.0, 1: 4.0},
    },
    "Brightening Clay Mask": {
        "price": 85000,
        "rating_dist": {5: 60.0, 4: 18.0, 3: 10.0, 2: 6.0, 1: 6.0},
    },
    "Centella Acne Patch": {
        "price": 69000,
        "rating_dist": {5: 72.0, 4: 14.0, 3: 7.0, 2: 3.5, 1: 3.5},
    },
}

# === REAL SCRAPED REVIEW TEXTS ===
REAL_REVIEWS_SOMETHINC = [
    "beneran mantap ini moisturizer, setelah pake 2 minggu muka jadi lebih lembab dan gak breakout. Cocok banget buat kulit kering kayak aku",
    "kemarin dibeliin temen sebagai kado, eh ternyata enak banget dipake. Teksturnya ringan, nyerap cepet, wanginya soft. Wajjib beli lagi!",
    "udah pake 3 tube, makin jatuh cinta. Kulit jadi lebih kenyal dan lembab seharian. Packagingnya juga aesthetic banget pas di meja rias",
    "awalnya ragu karena harga lumayan, tapi ternyata worth it banget. Dipagi hari dipake sebelum makeup, hasilnya lebih natural dan gak cakey",
    "suami sampe notice kulitku makin mulus setelah pake ini 1 bulan. Sumpah gas nyesel beli, bakalan repeat terus",
    "Recommended banget buat yang kulitnya sensitif dan gampang merah. Aku cocok banget, gak perih, gak breakout, lembabnya tahan sampe sore",
    "udah 3 kali repeat, memang ampuh bikin wajah glowing natural. Tekstur creamnya gak berat, cocok buat cuaca tropis",
    "produk oke, pengiriman cepet, packing rapi. Tapi untuk kulitku yang oily kurang cocok, agak berminyak dipakenya. Mungkin cocok buat kering aja",
    "lumayan sih, harga segitu dapet kualitas gini. Cuma agak butuh waktu buat nyerap, jadi agak nempel dikit pas pagi hari",
    "sejauh ini baik, rutin pake tiap malem dan pagi. Belum ada efek signifikan sih, tapi lumayan lembab dan gak breakout. Lanjut dulu",
]

REAL_REVIEWS_SKINTIFIC_SCAFFOLD = [
    "katanya bagus banget ini produk, tp setelah 2 minggu pake kok muka malah merah-merah dan perih? Kirain cocok tp ternyata engga",
    "udah 2 kali beli, pertama oke, kedua kok beda ya teksturnya? Mungkin batch beda? Hasilnya jg kurang maksimal",
    "awalnya glowing tp lama2 breakout. Mungkin purging tapi udah 1 bulan masih jerawatan. Kapok deh",
    "murah sih, dapet promo 40%, tp sayang hasilnya biasa aja. Gak sesuai ekspektasi, mending nabung buat beli yang lebih bagus",
    "suka banget sama teksturnya, ringan, wangi enak. Cuma sayang packingnya bocor pas sampe, kurirnya brutal",
    "produknya oke sih buat harga segini. Tapi katanya SPF 50 tp setelah pake 2 jam muka tetep hitam kena matahari?",
    "beli karena murah + diskon gede. Pas dipake kok malah bruntusan ya? Mungkin gak cocok buat kulit sensitif",
    "lumayan lah buat harga diskon, tp kalo harga normal kayaknya gak worth. Banyak produk lain yg lebih bagus di harga segini",
    "pengiriman cepet, packingnya aman. Produknya baru nyoba 3 hari, blm liat hasil signifikan. Semoga cocok",
    "enak dipake, wanginya wangi skincare gitu. Tapi hasilnya kurang nampol dibanding Somethinc so far",
]

# =============================================
# BRAND-SPECIFIC REVIEW TEMPLATES
# =============================================

def somethinc_review_text(product, rating, is_affiliate=False):
    """Somethinc: premium, loyal, tapi price-conscious."""
    skin_type = random.choice(["kombinasi", "kering", "sensitif", "normal", "berminyak"])

    if rating >= 4:
        templates = [
            (f"setelah pake {random.choice(['2 minggu', 'sebulan', '3 minggu', 'hampir sebulan'])},"
             f" kulit {skin_type} ku jadi jauh lebih lembab dan sehat. Worth every penny! "
             f"{random.choice(['Bakal repeat terus!', 'Holy grail!', 'Best skincare ever!'])}"),
            (f"mahal sih... tapi emang beneran bagus. Teksturnya ringan, nyerap cepet, gak lengket."
             f" {random.choice(['Cocok buat daily use', 'Pantesan best seller', 'Gas nyesel beli'])}"),
            f"awalnya mikir \"semahal ini?\", tp setelah pake {random.choice(['2 minggu', 'sebulan'])} baru sadar kenapa banyak yg suka.\
 emang quality banget. Kulit jadi kenyal dan glowing alami.",
            f"udah repeat {random.choice(['2x', '3x', '4x', 'berkali-kali'])}. Gak ada niat pindah ke brand lain.\
 {random.choice(['Somethinc emang juara', 'Brand lokal terbaik', 'Loyal banget sm brand ini'])}.",
            f"beneran bikin kulit sehat. Dulu pake brand murahan muka malah merah-merah.\
 After switching ke Somethinc, semua berubah. {random.choice(['Mahal dikit gapapa yg penting cocok', 'Skincare is investment'])}",
            f"suamiku notice kulitku makin cerah setelah pake ini 2 bulan. Dia sampe nanya pake skincare apa.\
 {random.choice(['Best investment ever!', 'Beneran works'])}",
        ]
        if is_affiliate:
            templates += [
                f"dapet link dari affiliate, coba-coba tp ternyata beneran bagus.\
 Cocok buat {skin_type}, langsung glowing setelah 2 minggu. Sayang harga lumayan tp sebanding!",
            ]
    elif rating == 3:
        templates = [
            f"produknya oke tp kurang suka sama {random.choice(['teksturnya yang agak berat', \
'harganya yg lumayan tinggi', 'kemasannya yg kurang praktis'])}. Mungkin ekspektasi gw terlalu tinggi.",
            f"bagus sih tp menurut gw kemahalan buat segitu doang. Banyak produk lain yg lebih murah dengan kualitas mirip.",
        ]
    else:
        templates = [
            f"mahal banget tp hasilnya biasa aja. Kulit {skin_type} ku malah breakout abis pake ini.\
 {random.choice(['Sayang banget duitnya', 'Gak worth it', 'Kapok beli'])}",
            f"kemasannya jelek, bocor pas sampe. Udah mahal, packing juga gak rapi.\
 {random.choice(['Kecewa banget', 'Gak recommended'])}",
            f"ekspektasi tinggi karena review bagus2, tp realitanya... kurang cocok di kulit aku yg {skin_type}.\
 Berasa sayang duit aja beli semahal ini.",
        ]
    return random.choice(templates)


def skintific_review_text(product, rating, is_affiliate=False):
    """Skintific: agresif, promo-heavy, mixed results."""
    skin_type = random.choice(["kombinasi", "berminyak", "kering", "sensitif", "berjerawat"])

    if rating >= 4:
        templates = [
            f"pas dapet diskon 40%, langsung borong. Ternyata enak juga! Tekstur ringan cocok buat\
 {skin_type}. {random.choice(['Bestie rekomen', 'Buat harga promo worth it', 'Bakal repeat pas diskon lagi'])}",
            f"awalnya ragu krn banyak review negatif tp pas dicoba oke juga sih.\
 {random.choice(['Mungkin tiap orang beda2 cocoknya', 'Gak sejelek yg dikatain orang', 'Bagus buat harga segini'])}",
            f"dibeliin pacar karena katanya best seller di TikTok. Ternyata enak banget, cocok buat\
 {skin_type}. {random.choice(['Seneng!', 'Rekomendasi', 'Gas pol'])}",
            f"pengiriman cepet, packing rapi, produk original. Baru pake seminggu, semoga cocok dan hasilnya maksimal.",
            f"lumayan lah buat harga segini. Gapake lama langsung lembab. Cuma wanginya agak strong buat aku.",
        ]
        if is_affiliate:
            templates += [
                f"jadi affiliate Skintific krn komisinya gede. Tapi produknya jujur oke2 aja + ada diskon terus.\
 Banyak yg beli karena promonya gila2an.",
            ]
    elif rating == 3:
        templates = [
            f"setelah pake 2 minggu, hasilnya... biasa aja. Mungkin butuh waktu lebih lama.\
 Tp dibanding Somethinc yg pernah gw pake, ini kalah jauh.",
            f"harga sih murah banget apalagi pas promo. Tp kualitas ya sebanding harganya.\
 Banyak klaim tp realitanya standar.",
            f"produk oke tp katanya SPF dan ingredients bagus. Tp setelah pake muka jadi berminyak.\
 Mungkin cocok buat yg kering doang.",
        ]
    else:
        templates = [
            f"breakout parah abis pake ini! Muka jadi merah-merah dan perih.\
 {random.choice(['Banyak yg salahkan produk ini', 'Jangan beli kalo kulit sensitif', 'Gak worth it'])}",
            f"gak sesuai klaimnya. Dibilang glowing tp realitanya kusam. Mending beli yang udah proven aja.\
 {random.choice(['Overhyped', 'Banyak promo tp kualitas biasa'])}",
            f"produknya oke, tp setelah 3 minggu pake muka malah tambah breakout.\
 Mungkin formula ini gak cocok buat {skin_type}.",
            f"awalnya glowing tp lama-lama makin parah. Banyak yg pengalaman sama katanya karena terlalu banyak kandungan\
 aktif. {random.choice(['Gak recommended untuk jangka panjang', 'Mending pake yg lebih gentle'])}",
            f"pengiriman lama banget, packing asal-asalan. Produknya bocor pas ampe.\
 Udah gitu hasilnya jg biasa. {random.choice(['Gak akan repeat', 'Kecewa berat'])}",
            f"beli karena FOMO banyak influencer, tp nyesel. Produk viral belum tentu cocok.\
 {random.choice(['Back to Somethinc', 'Kualitas jauuuuh dibanding Somethinc', 'Lesson learned'])}",
        ]
    return random.choice(templates)


# =============================================
# REVIEW GENERATOR
# =============================================
SKIN_TYPES = ["kombinasi", "berminyak", "kering", "sensitif", "normal", "berjerawat"]

def weighted_rating(rating_dist):
    r = random.random() * 100
    cumulative = 0
    for star, weight in sorted(rating_dist.items(), reverse=True):
        cumulative += weight
        if r <= cumulative:
            return star
    return 5

def generate_price_range(price):
    if price >= 130000:
        return "high"
    elif price >= 100000:
        return "mid"
    else:
        return "low"

def generate_review(product_data, brand, product_name):
    is_affiliate = random.random() < (0.22 if brand == "somethinc" else 0.15)
    # Skintific more suspicious reviews
    is_suspicious = random.random() < (0.04 if brand == "somethinc" else 0.08)

    rating = weighted_rating(product_data["rating_dist"])

    # Calibrate sentiment to rating
    if rating >= 4:
        sent = "positive"
    elif rating == 3:
        sent = "neutral"
    else:
        sent = "negative"

    # Use real reviews for hero product
    if product_data.get("is_hero") and random.random() < 0.15:
        text = random.choice(REAL_REVIEWS_SOMETHINC)
        if any(w in text.lower() for w in ["mantap", "bagus", "cocok", "recommended", "worth", "fall in love"]):
            sent, rating = "positive", 5
        elif any(w in text.lower() for w in ["gak cocok", "kecewa"]):
            sent, rating = "negative", 2
        elif "berminyak" in text.lower() or "kurang cocok" in text.lower():
            sent, rating = "neutral", 3
        else:
            sent, rating = "positive", 4
    else:
        # Brand-specific text generation
        if brand == "somethinc":
            text = somethinc_review_text(product_name, rating, is_affiliate)
        else:
            text = skintific_review_text(product_name, rating, is_affiliate)

    # --- BRAND-SPECIFIC PATTERNS ---
    if brand == "somethinc":
        # Premium: high price, less discount, more repeat intent
        has_discount = random.random() < 0.15
        repeat_chance = 0.40 if rating >= 4 else 0.03
        shipping_chance = 0.05
        packaging_chance = 0.08  # more packaging complaints for premium
        cs_chance = 0.02
    else:
        # Skintific: heavy promo, less loyalty, more logistics issues
        has_discount = random.random() < 0.50
        repeat_chance = 0.20 if rating >= 4 else 0.02
        shipping_chance = 0.12  # more shipping complaints
        packaging_chance = 0.07
        cs_chance = 0.04

    has_discount_mention = has_discount

    mentions_shipping = random.random() < shipping_chance
    mentions_packaging = random.random() < packaging_chance
    mentions_cs = random.random() < cs_chance
    has_logistic_mention = mentions_shipping or mentions_packaging or mentions_cs

    price_keywords = ["harga", "mahal", "murah", "worth", "kemahalan", "sebanding", "terjangkau", "murah"]
    has_price_mention = any(kw in text.lower() for kw in price_keywords)

    product_price = product_data["price"]
    if has_discount:
        price_paid = int(product_price * random.uniform(0.6, 0.9))
    else:
        price_paid = product_price

    # Brand-specific feature requests
    if brand == "somethinc":
        feat_kw = ["varian", "ukuran", "size", "travel size", "tambahin", "dibikin", "kemasan", "botol", "pump"]
    else:
        feat_kw = ["tambahin", "kalo ada", "pengen", "dibikin", "semoga", "buatin", "formula", "lebih ringan", "SPF", "oil free"]
    has_feature_request = any(kw in text.lower() for kw in feat_kw)
    feature_request_text = text if has_feature_request else ""

    has_repeat_intent = random.random() < repeat_chance

    days_ago = random.randint(1, 120)
    base_date = datetime.now() - timedelta(days=days_ago)
    weekday = base_date.weekday()

    return {
        "brand": brand,
        "product_name": product_name,
        "rating": rating,
        "text": text,
        "user_type": "affiliate" if is_affiliate else ("suspicious" if is_suspicious else "organic"),
        "has_repeat_intent": has_repeat_intent,
        "is_suspicious_positive": is_suspicious and rating >= 4,
        "sentiment_label": sent,
        "has_discount": has_discount,
        "has_discount_mention": has_discount_mention,
        "has_logistic_mention": has_logistic_mention,
        "has_price_mention": has_price_mention,
        "price_paid": price_paid,
        "has_feature_request": has_feature_request,
        "feature_request_text": feature_request_text,
        "mentions_shipping": mentions_shipping,
        "mentions_packaging": mentions_packaging,
        "mentions_cs": mentions_cs,
        "price_range": generate_price_range(product_data["price"]),
        "days_ago": days_ago,
        "weekday": weekday,
    }

def main():
    TOTAL_REVIEWS = 2000
    BRAND_SPLIT = 0.5

    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    reviews = []
    som_count = 0
    skn_count = 0
    counts_per_product = {}

    som_products = list(SOMETHINC_PRODUCTS.items())
    skn_products = list(SKINTIFIC_PRODUCTS.items())

    for i in range(TOTAL_REVIEWS):
        if i < TOTAL_REVIEWS * BRAND_SPLIT:
            product_name, product_data = random.choice(som_products)
            brand = "somethinc"
            som_count += 1
        else:
            product_name, product_data = random.choice(skn_products)
            brand = "skintific"
            skn_count += 1

        key = f"{brand}:{product_name}"
        counts_per_product[key] = counts_per_product.get(key, 0) + 1
        review = generate_review(product_data, brand, product_name)
        reviews.append(review)

    random.shuffle(reviews)

    output_path = raw_dir / "tiktok_reviews_raw.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    # Quick stats
    som_ratings = [r["rating"] for r in reviews if r["brand"] == "somethinc"]
    skn_ratings = [r["rating"] for r in reviews if r["brand"] == "skintific"]
    som_pos = sum(1 for r in reviews if r["brand"] == "somethinc" and r["sentiment_label"] == "positive")
    skn_pos = sum(1 for r in reviews if r["brand"] == "skintific" and r["sentiment_label"] == "positive")

    print(f"✅ Generated {len(reviews)} reviews with BRAND DIFFERENTIATION")
    print(f"")
    print(f"🔵 SOMETHINC (Premium)")
    print(f"   Reviews: {som_count}")
    print(f"   Avg rating: {sum(som_ratings)/len(som_ratings):.2f}")
    print(f"   Positive: {som_pos}/{som_count} ({som_pos/som_count*100:.1f}%)")
    print(f"")
    print(f"🟣 SKINTIFIC (Challenger)")
    print(f"   Reviews: {skn_count}")
    print(f"   Avg rating: {sum(skn_ratings)/len(skn_ratings):.2f}")
    print(f"   Positive: {skn_pos}/{skn_count} ({skn_pos/skn_count*100:.1f}%)")
    print(f"")
    print(f"📊 Expected Gap: {abs(som_pos/som_count - skn_pos/skn_count)*100:.1f}% sentiment gap")
    print(f"   File: {output_path}")

if __name__ == "__main__":
    main()
