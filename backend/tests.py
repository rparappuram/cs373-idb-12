import unittest
from typing import Any
from urllib.parse import urlencode

from pyuca import Collator

from app import app
from sort_method_data import region_sort_methods

collator = Collator()

JsonObject = dict[str, Any]

app.testing = True


def create_url(url: str, params: JsonObject | None = None):
    if params is None:
        return url
    return f"{url}?{urlencode(params,True)}"


def is_alphabetical_order(reverse: bool, *elements: str) -> bool:
    return sorted(elements, key=collator.sort_key, reverse=reverse) == list(elements)


class WineAllTests(unittest.TestCase):
    endpoint = "/wines"

    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test_status_code_200(self):
        res = self.client.get(WineAllTests.endpoint)
        self.assertEqual(res.status_code, 200)

    def test_unspecified_param(self):
        res = self.client.get(create_url(WineAllTests.endpoint, {"this_is_not_defined": 0}))
        self.assertEqual(res.status_code, 200)

    def test_invalid_formatted_param(self):
        res = self.client.get(
            create_url(
                WineAllTests.endpoint,
                {
                    "page": "this should be a number",
                    "startRating": "this should also be a number",
                },
            )
        )

        self.assertEqual(res.status_code, 200)

    def test_format(self):
        res = self.client.get(WineAllTests.endpoint).get_json()

        self.assertEqual(type(res["length"]), int)
        self.assertEqual(type(res["list"]), list)
        self.assertEqual(type(res["page"]), int)
        self.assertEqual(type(res["totalPages"]), int)
        self.assertEqual(type(res["totalInstances"]), int)

        regions: list = res["list"]
        self.assertGreater(len(regions), 0)

    def test_min_clamp_page(self):
        page_num = -1
        res = self.client.get(create_url(WineAllTests.endpoint, {"page": page_num})).get_json()
        self.assertNotEqual(res["page"], page_num)
        self.assertEqual(res["page"], 1)

    def test_max_clamp_page(self):
        page_num = 39485
        res = self.client.get(create_url(WineAllTests.endpoint, {"page": page_num})).get_json()
        self.assertNotEqual(res["page"], page_num)
        self.assertEqual(res["page"], res["totalPages"])

    def test_length(self):
        res = self.client.get(WineAllTests.endpoint).get_json()
        self.assertEqual(res["length"], len(res["list"]))

    def test_page(self):
        page_num = 2
        res_1 = self.client.get(WineAllTests.endpoint).get_json()
        res_2 = self.client.get(create_url(WineAllTests.endpoint, {"page": page_num})).get_json()

        self.assertEqual(res_2["page"], page_num)
        self.assertNotEqual(res_1["list"][0]["id"], res_2["list"][0]["id"])

    def test_name(self):
        name_query = "os"
        res = self.client.get(create_url(WineAllTests.endpoint, {"name": name_query})).get_json()

        wines: list[JsonObject] = res["list"]
        self.assertGreater(len(wines), 0)

        for wine in wines:
            name: str = wine["name"].lower()
            self.assertTrue(name_query in name)

    def test_country(self):
        country_query = ["United States", "Portugal"]
        res = self.client.get(create_url(WineAllTests.endpoint, {"country": country_query})).get_json()

        wines: list[JsonObject] = res["list"]
        self.assertGreater(len(wines), 0)

        country_set = set(country_query)
        for wine in wines:
            country: str = wine["country"]
            self.assertTrue(country in country_set)


class WineIdTests(unittest.TestCase):
    endpoint = "/wines"

    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test_status_code_200(self):
        res = self.client.get(f"{WineIdTests.endpoint}/1")
        self.assertEqual(res.status_code, 200)

    def test_status_code_404(self):
        res = self.client.get(f"{WineIdTests.endpoint}/0")
        self.assertEqual(res.status_code, 404)

    def test_format(self):
        res = self.client.get(f"{WineIdTests.endpoint}/1").get_json()

        self.assertEqual(type(res["country"]), str)
        self.assertEqual(type(res["id"]), int)
        self.assertEqual(type(res["image"]), str)
        self.assertEqual(type(res["name"]), str)
        self.assertEqual(type(res["rating"]), float)
        self.assertEqual(type(res["redditPosts"]), list)
        self.assertEqual(type(res["related"]), dict)
        self.assertEqual(type(res["reviews"]), int)
        self.assertEqual(type(res["type"]), str)
        self.assertEqual(type(res["winery"]), str)

        redditPosts: list = res["redditPosts"]
        for post in redditPosts:
            self.assertEqual(type(post), str)

        related: dict = res["related"]
        self.assertEqual(type(related["regions"]), list)
        self.assertEqual(type(related["vineyards"]), list)


class VineyardAllTests(unittest.TestCase):
    endpoint = "/vineyards"

    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test_status_code_200(self):
        res = self.client.get(VineyardAllTests.endpoint)
        self.assertEqual(res.status_code, 200)

    def test_unspecified_param(self):
        res = self.client.get(create_url(VineyardAllTests.endpoint, {"this_is_not_defined": 0}))
        self.assertEqual(res.status_code, 200)

    def test_invalid_formatted_param(self):
        res = self.client.get(
            create_url(
                VineyardAllTests.endpoint,
                {
                    "page": "this should be a number",
                    "startRating": "this should also be a number",
                },
            )
        )

        self.assertEqual(res.status_code, 200)

    def test_format(self):
        res = self.client.get(VineyardAllTests.endpoint).get_json()

        self.assertEqual(type(res["length"]), int)
        self.assertEqual(type(res["list"]), list)
        self.assertEqual(type(res["page"]), int)
        self.assertEqual(type(res["totalPages"]), int)
        self.assertEqual(type(res["totalInstances"]), int)

        regions: list = res["list"]
        self.assertGreater(len(regions), 0)

    def test_min_clamp_page(self):
        page_num = -1
        res = self.client.get(create_url(VineyardAllTests.endpoint, {"page": page_num})).get_json()
        self.assertNotEqual(res["page"], page_num)
        self.assertEqual(res["page"], 1)

    def test_max_clamp_page(self):
        page_num = 39485
        res = self.client.get(create_url(VineyardAllTests.endpoint, {"page": page_num})).get_json()
        self.assertNotEqual(res["page"], page_num)
        self.assertEqual(res["page"], res["totalPages"])

    def test_length(self):
        res = self.client.get(VineyardAllTests.endpoint).get_json()
        self.assertEqual(res["length"], len(res["list"]))

    def test_page(self):
        page_num = 2
        res_1 = self.client.get(VineyardAllTests.endpoint).get_json()
        res_2 = self.client.get(create_url(VineyardAllTests.endpoint, {"page": page_num})).get_json()

        self.assertEqual(res_2["page"], page_num)
        self.assertNotEqual(res_1["list"][0]["id"], res_2["list"][0]["id"])

    def test_name(self):
        name_query = "os"
        res = self.client.get(create_url(VineyardAllTests.endpoint, {"name": name_query})).get_json()

        vineyards: list[JsonObject] = res["list"]
        self.assertGreater(len(vineyards), 0)

        for vineyard in vineyards:
            name: str = vineyard["name"].lower()
            self.assertTrue(name_query in name)

    def test_country(self):
        country_query = ["United States", "Portugal"]
        res = self.client.get(create_url(VineyardAllTests.endpoint, {"country": country_query})).get_json()

        vineyards: list[JsonObject] = res["list"]
        self.assertGreater(len(vineyards), 0)

        country_set = set(country_query)
        for vineyard in vineyards:
            country: str = vineyard["country"]
            self.assertTrue(country in country_set)


class VineyardIdTests(unittest.TestCase):
    endpoint = "/vineyards"

    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test_status_code_200(self):
        res = self.client.get(f"{VineyardIdTests.endpoint}/1")
        self.assertEqual(res.status_code, 200)

    def test_status_code_404(self):
        res = self.client.get(f"{VineyardIdTests.endpoint}/0")
        self.assertEqual(res.status_code, 404)

    def test_format(self):
        res = self.client.get(f"{VineyardIdTests.endpoint}/1").get_json()

        self.assertEqual(type(res["coordinates"]), dict)
        self.assertEqual(type(res["country"]), str)
        self.assertEqual(type(res["id"]), int)
        self.assertEqual(type(res["image"]), str)
        self.assertEqual(type(res["name"]), str)
        self.assertEqual(type(res["price"]), int)
        self.assertEqual(type(res["rating"]), float)
        self.assertEqual(type(res["related"]), dict)
        self.assertEqual(type(res["reviews"]), int)
        self.assertEqual(type(res["url"]), str)

        coordinates: dict = res["coordinates"]
        self.assertEqual(type(coordinates["latitude"]), float)
        self.assertEqual(type(coordinates["longitude"]), float)

        related: dict = res["related"]
        self.assertEqual(type(related["regions"]), list)
        self.assertEqual(type(related["wines"]), list)


class RegionAllTests(unittest.TestCase):
    endpoint = "/regions"

    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test_status_code_200(self):
        res = self.client.get(RegionAllTests.endpoint)
        self.assertEqual(res.status_code, 200)

    def test_unspecified_param(self):
        res = self.client.get(create_url(RegionAllTests.endpoint, {"this_is_not_defined": 0}))
        self.assertEqual(res.status_code, 200)

    def test_invalid_formatted_param(self):
        res = self.client.get(
            create_url(
                RegionAllTests.endpoint,
                {
                    "page": "this should be a number",
                    "startRating": "this should also be a number",
                },
            )
        )

        self.assertEqual(res.status_code, 200)

    def test_format(self):
        res = self.client.get(RegionAllTests.endpoint).get_json()

        self.assertEqual(type(res["length"]), int)
        self.assertEqual(type(res["list"]), list)
        self.assertEqual(type(res["page"]), int)
        self.assertEqual(type(res["totalPages"]), int)
        self.assertEqual(type(res["totalInstances"]), int)

        regions: list = res["list"]
        self.assertGreater(len(regions), 0)

    def test_min_clamp_page(self):
        page_num = -1
        res = self.client.get(create_url(RegionAllTests.endpoint, {"page": page_num})).get_json()
        self.assertNotEqual(res["page"], page_num)
        self.assertEqual(res["page"], 1)

    def test_max_clamp_page(self):
        page_num = 39485
        res = self.client.get(create_url(RegionAllTests.endpoint, {"page": page_num})).get_json()
        self.assertNotEqual(res["page"], page_num)
        self.assertEqual(res["page"], res["totalPages"])

    def test_length(self):
        res = self.client.get(RegionAllTests.endpoint).get_json()
        self.assertEqual(res["length"], len(res["list"]))

    def test_page(self):
        page_num = 2
        res_1 = self.client.get(RegionAllTests.endpoint).get_json()
        res_2 = self.client.get(create_url(RegionAllTests.endpoint, {"page": page_num})).get_json()

        self.assertEqual(res_2["page"], page_num)
        self.assertNotEqual(res_1["list"][0]["id"], res_2["list"][0]["id"])

    def test_name(self):
        name_query = "os"
        res = self.client.get(create_url(RegionAllTests.endpoint, {"name": name_query})).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        for region in regions:
            name: str = region["name"].lower()
            self.assertTrue(name_query in name)

    def test_country(self):
        country_query = ["United States", "Portugal"]
        res = self.client.get(create_url(RegionAllTests.endpoint, {"country": country_query})).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        country_set = set(country_query)
        for region in regions:
            country: str = region["country"]
            self.assertTrue(country in country_set)

    def test_rating(self):
        start_rating = 4.5
        end_rating = 4.9

        res = self.client.get(
            create_url(
                RegionAllTests.endpoint,
                {
                    "startRating": start_rating,
                    "endRating": end_rating,
                },
            )
        ).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        for region in regions:
            rating: float = region["rating"]
            self.assertTrue(start_rating <= rating <= end_rating)

    def test_reviews(self):
        start_reviews = 2
        end_reviews = 50

        res = self.client.get(
            create_url(
                RegionAllTests.endpoint,
                {
                    "startReviews": start_reviews,
                    "endReviews": end_reviews,
                },
            )
        ).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        for region in regions:
            reviews: int = region["reviews"]
            self.assertTrue(start_reviews <= reviews <= end_reviews)

    def test_tags(self):
        tags_query = ["Sights & Landmarks", "Spas & Wellness"]
        res = self.client.get(create_url(RegionAllTests.endpoint, {"tags": tags_query})).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        for region in regions:
            tags: set[str] = set(region["tags"])

            for tag in tags_query:
                self.assertTrue(tag in tags)

    def test_trip_types(self):
        trip_types_query = ["Solo travel", "Couples"]
        res = self.client.get(create_url(RegionAllTests.endpoint, {"tripTypes": trip_types_query})).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        for region in regions:
            trip_types: set[str] = set(region["tripTypes"])

            for trip_type in trip_types_query:
                self.assertTrue(trip_type in trip_types)

    def test_sort(self):
        res = self.client.get(create_url(RegionAllTests.endpoint, {"sort": "name_asc"})).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        for i in range(len(regions) - 1):
            cur_name: str = regions[i]["name"].lower()
            next_name: str = regions[i + 1]["name"].lower()
            self.assertTrue(is_alphabetical_order(False, cur_name, next_name))

    def test_sort_reverse(self):
        res = self.client.get(create_url(RegionAllTests.endpoint, {"sort": "name_desc"})).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        for i in range(len(regions) - 1):
            cur_name: str = regions[i]["name"].lower()
            next_name: str = regions[i + 1]["name"].lower()
            self.assertTrue(is_alphabetical_order(True, cur_name, next_name))

    def test_mix_1(self):
        country_query = ["United States", "Portugal"]
        trip_types_query = ["Couples"]
        tags_query = ["Tours"]
        end_rating = 4.7
        start_reviews = 50

        params: dict[str, Any] = {
            "country": country_query,
            "tripTypes": trip_types_query,
            "tags": tags_query,
            "endRating": end_rating,
            "startReviews": start_reviews,
            "sort": "rating_desc",
        }

        res = self.client.get(create_url(RegionAllTests.endpoint, params)).get_json()

        regions: list[JsonObject] = res["list"]
        self.assertGreater(len(regions), 0)

        country_set = set(country_query)
        for region in regions:
            rating: float = region["rating"]
            reviews: int = region["reviews"]
            country: str = region["country"]
            tags: set[str] = set(region["tags"])
            trip_types: set[str] = set(region["tripTypes"])

            self.assertTrue(rating <= end_rating)
            self.assertTrue(reviews >= start_reviews)
            self.assertTrue(country in country_set)

            for tag in tags_query:
                self.assertTrue(tag in tags)

            for trip_type in trip_types_query:
                self.assertTrue(trip_type in trip_types)

        # checking sort
        for i in range(len(regions) - 1):
            cur_rating: float = regions[i]["rating"]
            next_rating: float = regions[i + 1]["rating"]
            self.assertTrue(cur_rating >= next_rating)


class RegionIdTests(unittest.TestCase):
    endpoint = "/regions"

    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test_status_code_200(self):
        res = self.client.get(f"{RegionIdTests.endpoint}/1")
        self.assertEqual(res.status_code, 200)

    def test_status_code_404(self):
        res = self.client.get(f"{RegionIdTests.endpoint}/0")
        self.assertEqual(res.status_code, 404)

    def test_format(self):
        res = self.client.get(f"{RegionIdTests.endpoint}/1").get_json()

        self.assertEqual(type(res["coordinates"]), dict)
        self.assertEqual(type(res["country"]), str)
        self.assertEqual(type(res["id"]), int)
        self.assertEqual(type(res["image"]), dict)
        self.assertEqual(type(res["name"]), str)
        self.assertEqual(type(res["rating"]), float)
        self.assertEqual(type(res["related"]), dict)
        self.assertEqual(type(res["reviews"]), int)
        self.assertEqual(type(res["tags"]), list)
        self.assertEqual(type(res["tripTypes"]), list)
        self.assertEqual(type(res["url"]), str)

        coordinates: dict = res["coordinates"]
        self.assertEqual(type(coordinates["latitude"]), float)
        self.assertEqual(type(coordinates["longitude"]), float)

        image: dict = res["image"]
        self.assertEqual(type(image["height"]), int)
        self.assertEqual(type(image["width"]), int)
        self.assertEqual(type(image["url"]), str)

        related: dict = res["related"]
        self.assertEqual(type(related["vineyards"]), list)
        self.assertEqual(type(related["wines"]), list)

        tags: list = res["tags"]
        self.assertGreater(len(tags), 0)
        self.assertEqual(type(tags[0]), str)

        trip_types: list = res["tripTypes"]
        self.assertGreater(len(trip_types), 0)
        self.assertEqual(type(trip_types[0]), str)


class RegionLimitTests(unittest.TestCase):
    endpoint = "/regions/limits"

    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test_status_code_200(self):
        res = self.client.get(RegionLimitTests.endpoint)
        self.assertEqual(res.status_code, 200)

    def test_format(self):
        res: JsonObject = self.client.get(RegionLimitTests.endpoint).get_json()

        self.assertEqual(type(res["rating"]), dict)
        self.assertEqual(type(res["reviews"]), dict)
        self.assertEqual(type(res["tripTypes"]), list)
        self.assertEqual(type(res["tags"]), list)
        self.assertEqual(type(res["countries"]), list)
        self.assertEqual(type(res["sorts"]), list)

        self.assertEqual(type(res["rating"]["min"]), float)
        self.assertEqual(type(res["rating"]["max"]), float)
        self.assertEqual(type(res["reviews"]["min"]), int)

        trip_types: list[str] = res["tripTypes"]
        self.assertGreater(len(trip_types), 0)
        self.assertEqual(type(trip_types[0]), str)
        for i in range(len(trip_types) - 1):
            self.assertTrue(is_alphabetical_order(False, trip_types[i], trip_types[i + 1]))

        tags: list[str] = res["tags"]
        self.assertGreater(len(tags), 0)
        self.assertEqual(type(tags[0]), str)
        for i in range(len(tags) - 1):
            self.assertTrue(is_alphabetical_order(False, tags[i], tags[i + 1]))

        countries: list[str] = res["countries"]
        self.assertGreater(len(countries), 0)
        self.assertEqual(type(countries[0]), str)
        for i in range(len(countries) - 1):
            self.assertTrue(is_alphabetical_order(False, countries[i], countries[i + 1]))

        sort_methods: list[dict] = res["sorts"]
        self.assertGreater(len(sort_methods), 0)
        self.assertEqual(type(sort_methods[0]), dict)
        for i in range(len(sort_methods) - 1):
            self.assertTrue(sort_methods[i]["id"] <= sort_methods[i + 1]["id"])

    def test_values(self):
        res: JsonObject = self.client.get(RegionLimitTests.endpoint).get_json()

        self.assertEqual(res["rating"]["min"], 0.0)
        self.assertEqual(res["rating"]["max"], 5.0)
        self.assertEqual(res["reviews"]["min"], 0)

        sort_methods: list[JsonObject] = res["sorts"]
        for sort_method in sort_methods:
            self.assertTrue(sort_method["id"] in region_sort_methods)


if __name__ == "__main__":
    unittest.main()
