from flask_query_builder.filters import Filter


class BookPriceFilter(Filter):
    def filter(self, query, model, filter_name, values):
        try:
            if filter_name == "price_gt":
                query = query.filter(getattr(model, "price") > values[0])
            if filter_name == "price_lt":
                query = query.filter(getattr(model, "price") < values[0])
            if filter_name == "price":
                query = query.filter(getattr(model, "price") == values[0])
            return query
        except Exception:
            return query
