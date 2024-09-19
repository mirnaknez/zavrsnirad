import geopandas as gpd
from geopandas import GeoSeries
import math

def load_coordinates(files):
    all_coords = []
    total_points = 0
    for file in files:
        gdf = gpd.read_file(file)
        if gdf.crs is None:
            gdf = gdf.set_crs("EPSG:4326")
        if gdf.crs != "EPSG:3857":
            gdf = gdf.to_crs("EPSG:3857")
        coords = []
        for geom in gdf.geometry:
            if geom.geom_type == 'MultiPoint':
                coords.extend([point for point in geom.geoms])
            else:
                coords.append(geom)
        all_coords.append(GeoSeries(coords, crs="EPSG:3857"))
        total_points += len(coords)
    return all_coords, total_points


def calculate_direction(point1, point2):
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    return math.degrees(math.atan2(dy, dx)) % 360

def calculate_normal(point1, point2):
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    magnitude = math.sqrt(dx**2 + dy**2)
    return -dy / magnitude, dx / magnitude

def is_right_of_line(vehicle_point, line_start, line_end):
    normal_x, normal_y = calculate_normal(line_start, line_end)
    vector_x = vehicle_point.x - line_start.x
    vector_y = vehicle_point.y - line_start.y
    return (vector_x * normal_x + vector_y * normal_y) > 0

def find_street(point, edges_gdf, distance_threshold=100):
    distances = edges_gdf.geometry.apply(lambda geom: geom.distance(point))
    nearest_edge_idx = distances.idxmin()
    nearest_edge = edges_gdf.loc[nearest_edge_idx]
    min_distance = distances.min()
    if min_distance <= distance_threshold:
        if(nearest_edge['name']):
            return nearest_edge['name']
        elif(nearest_edge['ref']):
            return nearest_edge['ref']
        else:
            return nearest_edge['@id']
    return None


def check_oneway_and_direction(street, edges_gdf):
    row = edges_gdf[edges_gdf['name'] == street].iloc[0]
    if 'oneway' in row and row['oneway'] == 'yes':
        street_geom = row.geometry
        line_start, line_end = street_geom.coords[0], street_geom.coords[-1]
        line_start = GeoSeries.from_xy([line_start[0]], [line_start[1]])
        line_end = GeoSeries.from_xy([line_end[0]], [line_end[1]])
        direction = calculate_direction(line_start.iloc[0], line_end.iloc[0])
        return True, direction
    return False, None

def check_proximity(point1, point1previous, point2, point2previous, point_index, vehicle1, vehicle2, edges_gdf, distance_threshold=10):
    if point1.distance(point2) > 100:
        return None

    street1 = find_street(point1, edges_gdf, distance_threshold)
    street2 = find_street(point2, edges_gdf, distance_threshold)
    if street1 and street2 and street1 == street2:
        oneway, direction = check_oneway_and_direction(street1, edges_gdf)
        if not oneway:
            street_geom = edges_gdf.loc[edges_gdf['name'] == street1, 'geometry'].iloc[0]
            line_start, line_end = street_geom.coords[0], street_geom.coords[-1]
            line_start = GeoSeries.from_xy([line_start[0]], [line_start[1]])
            line_end = GeoSeries.from_xy([line_end[0]], [line_end[1]])
            dir1 = calculate_direction(point1previous, point1)
            dir2 = calculate_direction(point2previous, point2)
            if not((is_right_of_line(point1, line_start.iloc[0], line_end.iloc[0]) and is_right_of_line(point2, line_end.iloc[0], line_start.iloc[0])) or 
                (is_right_of_line(point2, line_start.iloc[0], line_end.iloc[0]) and is_right_of_line(point1, line_end.iloc[0], line_start.iloc[0]))):
                if dir1 != dir2:
                    return f"Vehicles {vehicle1} and {vehicle2} at position {point_index + 1} are in danger of collision on two-way street '{street1}'."
        else:
            dir1 = calculate_direction(point1previous, point1)
            dir2 = calculate_direction(point2previous, point2)
            if (dir1 != direction or dir2 != direction) and dir1 != dir2:
                return f"Vehicles {vehicle1} and {vehicle2} at position {point_index + 1} are in danger of collision on one-way street '{street1}'."
    return None
