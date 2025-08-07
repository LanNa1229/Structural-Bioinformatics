# Tags: AlphaFold3, pymol, measure
# To run in PyMOL:
# run measure_distance_and_angle_csv.py
# measure_distance_and_angle()

from pymol import cmd
import math
import csv

def measure_distance_and_angle(output_file="Sp154-b_measurement_angle-distance.csv"):
    # Prepare a list to collect results
    results = []
    object_list = cmd.get_object_list('all')

    for obj in object_list:
        try:
            # Define atom selections
            atom1 = f"({obj} and segi G and resi 5 and name O4)" # nucleophile
            atom2 = f"({obj} and segi H and name C1')" 
            atom3 = f"({obj} and segi H and name O3B)"
            
            # Get coordinates
            coord1 = cmd.get_atom_coords(atom1)
            coord2 = cmd.get_atom_coords(atom2)
            coord3 = cmd.get_atom_coords(atom3)

            # Calculate distance between atom1 and atom2
            distance = math.dist(coord1, coord2)

            # Calculate angle between (coord1 - coord2 - coord3)
            def vector(p1, p2):
                return [p2[i] - p1[i] for i in range(3)]

            def dot_product(v1, v2):
                return sum([v1[i]*v2[i] for i in range(3)])

            def vector_length(v):
                return math.sqrt(sum([v[i]*v[i] for i in range(3)]))

            v1 = vector(coord2, coord1)
            v2 = vector(coord2, coord3)

            dot = dot_product(v1, v2)
            len1 = vector_length(v1)
            len2 = vector_length(v2)

            cosine_angle = dot / (len1 * len2)
            cosine_angle = min(1.0, max(-1.0, cosine_angle))
            angle = math.degrees(math.acos(cosine_angle))

            # Append result
            results.append([obj, round(distance, 2), round(angle, 2)])

        except Exception as e:
            print(f"Skipping {obj} due to error: {e}")

    # Save results into a CSV file
    with open(output_file, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header
        csvwriter.writerow(["protein_name", "distance (Å)", "angle (°)"])
        # Write data rows
        csvwriter.writerows(results)

    print(f"Results saved to {output_file}")


