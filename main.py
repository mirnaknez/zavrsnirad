import geopandas as gpd
import safedrive as sd
import time

start_whole = time.time()
start_time = time.time()

files = [
    'vozilo1.geojson', 'vozilo2.geojson', 'vozilo3.geojson', 'vozilo4.geojson',
    'vozilo5.geojson', 'vozilo6.geojson', 'vozilo7.geojson', 'vozilo8.geojson',
    'vozilo9.geojson', 'vozilo10.geojson', 'vozilo11.geojson', 'vozilo12.geojson',
    'vozilo13.geojson', 'vozilo14.geojson', 'vozilo15.geojson', 'vozilo16.geojson',
    'vozilo17.geojson', 'vozilo18.geojson', 'vozilo19.geojson', 'vozilo20.geojson'
]

paths, total_points = sd.load_coordinates(files)
end_time = time.time()

start_map = time.time()
geojson_file = "city_area.geojson"

edges_gdf = gpd.read_file(geojson_file)
edges_gdf = edges_gdf[edges_gdf['highway'].notna()]

if edges_gdf.crs != "EPSG:3857":
    edges_gdf = edges_gdf.to_crs("EPSG:3857")
end_map = time.time()


max_length = max(len(path) for path in paths)
start_time2 = time.time()
for point_index in range(1, max_length):
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            if point_index < len(paths[i]) and point_index < len(paths[j]):
                point1 = paths[i][point_index]
                point2 = paths[j][point_index]
                point1previous = paths[i][point_index - 1]
                point2previous = paths[j][point_index - 1]
                
                message = sd.check_proximity(point1, point1previous, point2, point2previous, point_index, i + 1, j + 1, edges_gdf)
                if message:
                    vehicles_in_radius = set([i + 1, j + 1])
                    nearby_vehicles = set()
                    for k in range(len(paths)):
                        if k != i and k != j and point_index < len(paths[k]):
                            point = paths[k][point_index]
                            if point1.distance(point) <= 100 or point2.distance(point) <= 100:
                                nearby_vehicles.add(k + 1)
                    
                    for vehicle in vehicles_in_radius:
                        print(f"Vehicle {vehicle}: {message}")
                    
                    for vehicle in nearby_vehicles:
                        print(f"Vehicle {vehicle}: {message}")


end_time2 = time.time()
end_whole = time.time()
needed_time_whole = end_whole - start_whole
needed_time = end_time - start_time
needed_time2 = end_time2 - start_time2
needed_map = end_map - start_map
print("\n")
print(f"Number of points: {total_points}")
print(f"Total time needed for testing: {needed_time_whole}s")
print(f"Total time needed for data load - map: {needed_map}s")
print(f"Total time needed for data load - points: {needed_time}s")
load_per_point = needed_time / total_points
print(f"Time for data load per point: {load_per_point}s")
print(f"Total time needed for analizing points: {needed_time2}s")
time_per_point = needed_time2 / total_points
print(f"Time per point: {time_per_point}s")







