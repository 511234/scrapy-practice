# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BestwatchscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


class WatchItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    sku = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    watch_spec = scrapy.Field()


# Unused below
class WatchSpecItem(scrapy.Item):
    information = scrapy.Field()
    dial = scrapy.Field()
    case = scrapy.Field()
    band = scrapy.Field()
    movement = scrapy.Field()
    features = scrapy.Field()


class WatchSpecInfoItem(scrapy.Item):
    brand = scrapy.Field()
    series = scrapy.Field()
    model = scrapy.Field()
    gender = scrapy.Field()
    produced = scrapy.Field()
    limited = scrapy.Field()


class WatchSpecDialItem(scrapy.Item):
    dial_type = scrapy.Field()
    dial_color = scrapy.Field()
    finish = scrapy.Field()
    indexes = scrapy.Field()
    hands = scrapy.Field()


class WatchSpecCaseItem(scrapy.Item):
    material = scrapy.Field()
    bezel = scrapy.Field()
    glass = scrapy.Field()
    back = scrapy.Field()
    shape = scrapy.Field()
    diameter = scrapy.Field()
    height = scrapy.Field()
    lug_width = scrapy.Field()


class WatchSpecBandItem(scrapy.Item):
    band_material = scrapy.Field()
    band_color = scrapy.Field()


class WatchSpecMovementItem(scrapy.Item):
    caliber = scrapy.Field()
    type = scrapy.Field()
    diameter = scrapy.Field()
    jewels = scrapy.Field()
    reserve = scrapy.Field()
    frequency = scrapy.Field()
    time = scrapy.Field()
    chronograph = scrapy.Field()
    additionals = scrapy.Field()


class WatchSpecFeatureItem(scrapy.Item):
    water_resistance = scrapy.Field()
    watch_features = scrapy.Field()
