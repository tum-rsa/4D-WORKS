from pystac import Catalog

cat = Catalog.from_file("demo/Isar/catalog.json")

print(cat)

# or

# from stac4d.stac_point_cloud import PCCatalog

# cat = PCCatalog(path="demo/Isar/catalog.json")

item = cat.get_child("uav-photogrammetry").get_items()[0]
print(item.properties.get("native_crs"))

root = [it.id for it in cat.get_all_items() if it.get_parent().id == cat.id]
print("Root-level items:", root)