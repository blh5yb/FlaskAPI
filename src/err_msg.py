from collections import namedtuple

error_msg = namedtuple("ErrorMessage", "msg err_code status_code")

DB_INSERTION_ERROR = error_msg("Failed when inserting object to %s collection", 1, 500)

DB_UPDATE_ERROR = error_msg("Failed when updating object to %s collection", 2, 500)

DB_SEARCH_ERROR = error_msg("Failed when searching %s collection", 3, 404)

INVALID_VARIANT_ERROR = error_msg("The requests data is not valid", 4, 500)

MISSING_QUERY_PARAMETER = error_msg("The requests query parameter, %s, was not provided", 5, 500)

BAD_REQUEST = error_msg("The requests query parameter, %s, or body was not provided", 6, 400)
