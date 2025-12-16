import pathlib
import polars as pl


def prepare_mobile_reviews_data(data_path: str | pathlib.Path):
    """
    Load and prepare the mobile reviews dataset for ChromaDB.

    Returns a dict with:
        - ids:       list[str]
        - documents: list[str]  (enriched text used for embedding)
        - metadatas: list[dict] (all original columns, including review_text)
    """

    data_path = pathlib.Path(data_path)

    dtypes = {
        "review_id": pl.Int64,
        "brand": pl.Utf8,
        "model": pl.Utf8,
        "price_usd": pl.Float64,
        "rating": pl.Float64,
        "review_text": pl.Utf8,
        "sentiment": pl.Utf8,
        "battery_life_rating": pl.Float64,
        "camera_rating": pl.Float64,
        "performance_rating": pl.Float64,
        "design_rating": pl.Float64,
        "display_rating": pl.Float64,
    }

    mobile_reviews = pl.scan_csv(str(data_path), dtypes=dtypes)

    mobile_review_db_data = (
        mobile_reviews
        .select([
            "review_id",
            "brand",
            "model",
            "price_usd",
            "rating",
            "review_text",
            "sentiment",
            "battery_life_rating",
            "camera_rating",
            "performance_rating",
            "design_rating",
            "display_rating",
        ])
        .sort(["brand", "model", "rating"])
        .collect()
    )

    # Build enriched embedding text
    #structured so user queries like "best camera", "under $300", "positive", etc. match well.
    mobile_review_db_data = mobile_review_db_data.with_columns(
        pl.concat_str(
            [
                pl.lit("brand: "),
                pl.col("brand").fill_null(""),
                pl.lit(" | model: "),
                pl.col("model").fill_null(""),
                pl.lit(" | sentiment: "),
                pl.col("sentiment").fill_null(""),
                pl.lit(" | price_usd: "),
                pl.col("price_usd").cast(pl.Utf8).fill_null(""),
                pl.lit(" | rating: "),
                pl.col("rating").cast(pl.Utf8).fill_null(""),
                pl.lit(" | battery_life_rating: "),
                pl.col("battery_life_rating").cast(pl.Utf8).fill_null(""),
                pl.lit(" | camera_rating: "),
                pl.col("camera_rating").cast(pl.Utf8).fill_null(""),
                pl.lit(" | performance_rating: "),
                pl.col("performance_rating").cast(pl.Utf8).fill_null(""),
                pl.lit(" | design_rating: "),
                pl.col("design_rating").cast(pl.Utf8).fill_null(""),
                pl.lit(" | display_rating: "),
                pl.col("display_rating").cast(pl.Utf8).fill_null(""),
                pl.lit(" | review: "),
                pl.col("review_text").fill_null(""),
            ],
            separator="",
        ).alias("embed_text")
    )

    ids = mobile_review_db_data["review_id"].cast(str).to_list()

    # These are the strings that will be embedded
    documents = mobile_review_db_data["embed_text"].to_list()

    # Keep everything else (including raw review_text) as metadata, but drop embed_text to avoid duplication
    metadatas = mobile_review_db_data.drop("embed_text").to_dicts()

    return {"ids": ids, "documents": documents, "metadatas": metadatas}
