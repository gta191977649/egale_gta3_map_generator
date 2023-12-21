# this code handles reading the object.dat
def parse_line(line,game = "VC"):
    # Splitting by commas first
    parts = [part.strip() for part in line.split(',')]

    # Further splitting any parts that contain tabs
    processed_parts = []
    for part in parts:
        sub_parts = part.split('\t')
        processed_parts.extend([sub.strip() for sub in sub_parts if sub.strip()])



    # Parsing each part, assuming each field is separated by a comma or a tab
    try:
        if game == "VC":
            # Check if there are enough parts (at least 13) in the line

            if len(processed_parts) < 11: return False

            return {
                "modelName": processed_parts[0],
                "mass": float(processed_parts[1]),
                "turnMass": float(processed_parts[2]),
                "airResistance": float(processed_parts[3]),
                "elasticity": float(processed_parts[4]),
                "percentSubmerged": float(processed_parts[5]),
                "uprootLimit": float(processed_parts[6]),
                "collisionDamageMultiplier": float(processed_parts[7]),
                "collisionDamageEffect": int(processed_parts[8]),
                "specialCollisionResponse": int(processed_parts[9]),
                # Additional field for camera avoidance
                "cameraAvoid": int(processed_parts[10]) if len(processed_parts) > 10 else 0
            }
        if game == "SA":
            # Check if there are enough parts (at least 13) in the line
            print(len(processed_parts))
            if len(processed_parts) < 13: return None

            return {
                "modelName": processed_parts[0],
                "mass": float(processed_parts[1]),
                "turnMass": float(processed_parts[2]),
                "airResistance": float(processed_parts[3]),
                "elasticity": float(processed_parts[4]),
                "percentSubmerged": float(processed_parts[5]),
                "uprootLimit": float(processed_parts[6]),
                "colDamageMultiplier": float(processed_parts[7]),
                "colDamageEffect": int(processed_parts[8]),
                "specialColResponse": int(processed_parts[9]),
                "cameraAvoid": int(processed_parts[10]),
                "causesExplosion": int(processed_parts[11]),
                "fxType": int(processed_parts[12]),
                # Additional fields (if present)
                "fxOffsetX": float(processed_parts[13]) if len(processed_parts) > 13 else 0.0,
                "fxOffsetY": float(processed_parts[14]) if len(processed_parts) > 14 else 0.0,
                "fxOffsetZ": float(processed_parts[15]) if len(processed_parts) > 15 else 0.0,
                "fxName": processed_parts[16] if len(processed_parts) > 16 else "",
                "smashMultiplier": float(processed_parts[17]) if len(processed_parts) > 17 else 0.0,
                "breakVelocityX": float(processed_parts[18]) if len(processed_parts) > 18 else 0.0,
                "breakVelocityY": float(processed_parts[19]) if len(processed_parts) > 19 else 0.0,
                "breakVelocityZ": float(processed_parts[20]) if len(processed_parts) > 20 else 0.0,
                "breakVelocityRand": float(processed_parts[21]) if len(processed_parts) > 21 else 0.0,
                "gunBreakMode": int(processed_parts[22]) if len(processed_parts) > 22 else 0,
                "sparksOnImpact": int(processed_parts[23]) if len(processed_parts) > 23 else 0
            }
    except ValueError as e:
        # Handle cases where conversion fails
        print(f"Error parsing line: {line}")
        print(e)
        return None
def getObjectDat(file_path):
    object_data = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith(';'):
                object_properties = parse_line(line)
                if object_properties:
                    object_data.append(object_properties)
    return object_data
