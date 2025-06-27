from flask_query_builder.filters import Filter


class BookReleaseDateFilter(Filter):
    def filter(self, query, model, filter_name, values):
        try:
            if filter_name == "release_date_gt":
                query = query.filter(getattr(model, "release_date") > values[0])
            if filter_name == "release_date_lt":
                query = query.filter(getattr(model, "release_date") < values[0])
            if filter_name == "release_date":
                query = query.filter(getattr(model, "release_date") == values[0])
            return query
        except Exception:
            return query
