import scrapy

class MoboSpider(scrapy.Spider):
    name = "mobo"
    allowed_domains = ["versus.com"]

    # all_links = ["https://versus.com" + link for link in response.css('.List__item___7Ul-S a ::attr(href)').getall()]
    start_urls = []

    def parse(self, response):
        mem = response.css('#group_memory')
        connectors_div = response.css('#group_connectors')
        expansion_slots = response.css('#group_expansion_slots')
        general_info = response.css('#group_general_info')
        yield {
            'brand': "Gigabyte",
            'name': response.css('.nameContainer p::text').get().replace("Gigabyte", "").strip(),
            'socket': general_info.css('.Group__propertiesContainer___3-B5C > div')[0].css('.Number__number___Mp4lk::text').get(),
            'chipset': general_info.css('.Group__propertiesContainer___3-B5C > div')[1].css('.Number__number___Mp4lk::text').get(),
            'formfactor': general_info.css('.Group__propertiesContainer___3-B5C > div')[2].css('.Number__number___Mp4lk::text').get(),
            'height_mm': '',
            'width_mm': '',
            'memory_capacity_gb': int(mem.css('.Group__propertiesContainer___3-B5C > div')[0].css('.Number__number___Mp4lk::text').get().replace('GB', '')),
            'ram_speed': int(mem.css('.Group__propertiesContainer___3-B5C > div')[1].css('.Number__number___Mp4lk::text').get().replace("MHz", "")),
            'ram_slots': int(mem.css('.Group__propertiesContainer___3-B5C > div')[3].css('.Number__number___Mp4lk::text').get()),
            'ram_type': mem.css('.Group__propertiesContainer___3-B5C > div')[4].css('.Number__number___Mp4lk::text').get(),
            'm2_slots': int(connectors_div.css('.Group__propertiesContainer___3-B5C > div')[6].css('.Number__number___Mp4lk::text').get()),
            'sata_ports': int(connectors_div.css('.Group__propertiesContainer___3-B5C > div')[3].css('.Number__number___Mp4lk::text').get()),
            'pci_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[4].css('.Number__number___Mp4lk::text').get(),
            'pcie_x1_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[3].css('.Number__number___Mp4lk::text').get(),
            'pcie_x4_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[6].css('.Number__number___Mp4lk::text').get(),
            'pcie_x8_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[7].css('.Number__number___Mp4lk::text').get(),
            'pcie_2.0_x16_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[5].css('.Number__number___Mp4lk::text').get(),
            'pcie_3.0_x16_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[2].css('.Number__number___Mp4lk::text').get(),
            'pcie_4.0_x16_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[0].css('.Number__number___Mp4lk::text').get(),
            'pcie_5.0_x16_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[1].css('.Number__number___Mp4lk::text').get(),
            'pcie_x16_slot': expansion_slots.css('.Group__propertiesContainer___3-B5C > div')[0].css('.Number__number___Mp4lk::text').get(),
        }
