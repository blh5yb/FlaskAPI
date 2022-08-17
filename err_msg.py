from collections import namedtuple

error_msg = namedtuple("ErrorMessage", "msg err_code status_code")

DB_INSERTION_ERROR = error_msg("Failed when insert to variant collection", 1, 500)

DB_SEARCH_ERROR = error_msg("Failed when search variant collection", 2, 500)

INVALID_VARIANT_SAVE_ERROR = error_msg("The requests data is not valid", 3, 500)

