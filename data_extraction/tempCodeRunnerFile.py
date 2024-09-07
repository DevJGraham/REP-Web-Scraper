except TimeoutException as e:
        print(f"Page {page_index} took too long to load for property index {property_index}: {e}")
        return None